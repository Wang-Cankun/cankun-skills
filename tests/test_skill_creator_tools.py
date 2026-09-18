"""Exercise portable validation and the optional static output viewer."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/ck-skill-creator"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


validator = module("creator_validator", SKILL / "scripts/validate_skill.py")
viewer = module("creator_viewer", SKILL / "eval-viewer/generate_review.py")


class CreatorToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def make_skill(self, description="Useful description"):
        skill = self.base / "sample-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            f"---\nname: sample-skill\ndescription: {description}\n---\n"
            "Read [details](references/details.md).\n", encoding="utf-8")
        (skill / "references").mkdir()
        (skill / "references/details.md").write_text("Run the actual command.\n")
        return skill

    def test_real_skill_and_nested_resource_checks(self):
        self.assertEqual(validator.validate(SKILL), [])
        skill = self.make_skill()
        self.assertEqual(validator.validate(skill), [])
        (skill / "references/details.md").write_text("See [fixture](missing.json).\n")
        self.assertTrue(any("missing resource" in e for e in validator.validate(skill)))

    def test_invalid_metadata_and_nonportable_link_fail_cli(self):
        skill = self.make_skill('""')
        self.assertTrue(any("description" in e for e in validator.validate(skill)))
        (skill / "SKILL.md").write_text("---\nname: wrong\ndescription: fine\n---\n[outside](../other.md)\n")
        errors = validator.validate(skill)
        self.assertTrue(any("differs" in e for e in errors))
        self.assertTrue(any("leaves" in e for e in errors))
        run = subprocess.run([sys.executable, str(SKILL / "scripts/validate_skill.py"), str(skill)], capture_output=True)
        self.assertNotEqual(run.returncode, 0)

    def test_code_examples_do_not_create_false_resource_failures(self):
        skill = self.make_skill()
        with (skill / "SKILL.md").open("a") as stream:
            stream.write("```md\n[example](uncreated.md)\n```\n")
        self.assertEqual(validator.validate(skill), [])

    def make_run(self, name, text):
        run = self.base / "review" / name
        (run / "outputs").mkdir(parents=True)
        (run / "outputs/result.html").write_text(text, encoding="utf-8")
        return run

    def test_static_viewer_preserves_output_without_executable_embedding(self):
        payload = '</script><script>window.untrusted=true</script>中文'
        a = self.make_run("A", payload)
        self.make_run("B", "second output")
        (a / "eval_metadata.json").write_text(json.dumps({"eval_id": 1, "prompt": "make a page"}))
        (a / "grading.json").write_text(json.dumps({"expectations": [{"text": "has page", "passed": True, "evidence": "result.html"}]}))
        runs = viewer.find_runs(self.base / "review")
        self.assertEqual(len(runs), 2)
        self.assertTrue(any(r["outputs"][0]["content"] == payload for r in runs))
        output = self.base / "review.html"
        result = subprocess.run([sys.executable, str(SKILL / "eval-viewer/generate_review.py"), str(self.base / "review"), "--static", str(output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        html = output.read_text()
        self.assertNotIn(payload, html)
        embedded = html.split("const EMBEDDED_DATA = ", 1)[1].split(";", 1)[0]
        self.assertTrue(any(r["outputs"][0]["content"] == payload for r in json.loads(embedded)["runs"]))

    def test_viewer_does_not_follow_linked_inputs(self):
        run = self.make_run("A", "real output")
        external = self.base / "private.txt"
        external.write_text("outside the requested review")
        (run / "outputs/linked.txt").symlink_to(external)
        (self.base / "review/loop").symlink_to(self.base / "review", target_is_directory=True)
        runs = viewer.find_runs(self.base / "review")
        self.assertEqual(len(runs), 1)
        self.assertEqual(len(runs[0]["outputs"]), 1)

    def test_empty_workspace_is_not_a_successful_review(self):
        result = subprocess.run([sys.executable, str(SKILL / "eval-viewer/generate_review.py"), str(self.base), "--static", str(self.base / "review.html")], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.base / "review.html").exists())

    def test_nested_skill_artifacts_and_offline_attachment_downloads(self):
        run = self.make_run("A", "top-level result")
        skill = run / "outputs/example-skill"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text("skill entrypoint")
        (skill / "references/schema.md").write_text("actual schema")
        attachment = run / "outputs/book.xlsx"
        attachment.write_bytes(b"workbook fixture")
        files = viewer.find_runs(self.base / "review")[0]["outputs"]
        self.assertIn("example-skill/references/schema.md", {f["name"] for f in files})
        book = next(f for f in files if f["name"] == "book.xlsx")
        self.assertEqual(book["type"], "binary")
        import base64
        self.assertEqual(base64.b64decode(book["data_uri"].split(",", 1)[1]), attachment.read_bytes())


if __name__ == "__main__":
    unittest.main()
