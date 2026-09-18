"""Check portable dependency closure, regeneration, and output ownership."""

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
module_spec = importlib.util.spec_from_file_location("build_plugins", ROOT / "scripts/build_plugins.py")
builder = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(builder)


class PluginBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.output = self.base / "ckstack"

    def test_real_bundle_contains_companions_references_and_licenses(self):
        builder.build(ROOT, self.output)
        names = {path.name for path in (self.output / "skills").iterdir()}
        self.assertEqual(names, {"ck-architect", "ck-arena", "ck-how", "ck-impact", "ck-prototype",
                                 "ck-reflect", "ck-skill-creator", "ck-teach",
                                 "ck-verify-create", "ck-verify-maintain", "ck-why", "confer", "deposition"})
        for name in names:
            for original in (ROOT / "skills" / name).rglob("*"):
                if any(part in builder.IGNORED_NAMES for part in original.relative_to(ROOT / "skills" / name).parts):
                    continue
                if original.suffix in builder.IGNORED_SUFFIXES:
                    continue
                if original.is_file():
                    copied = self.output / original.relative_to(ROOT)
                    self.assertEqual(copied.read_bytes(), original.read_bytes(), str(original))
        self.assertTrue((self.output / "skills/ck-architect/references/runner-prompt.md").is_file())
        self.assertTrue((self.output / "skills/ck-how/SKILL.md").is_file())
        self.assertTrue((self.output / "skills/ck-why/SKILL.md").is_file())
        for relative in ("scripts/confer.mjs", "scripts/confer-test.mjs", "references/providers.md", "agents/openai.yaml"):
            self.assertTrue((self.output / "skills/confer" / relative).is_file(), relative)
        self.assertTrue((self.output / "skills/confer/scripts/confer.mjs").stat().st_mode & 0o111,
                        "The installed confer CLI must remain executable")
        creator = self.output / "skills/ck-skill-creator"
        for relative in ("scripts/validate_skill.py", "eval-viewer/generate_review.py",
                         "eval-viewer/viewer.html", "references/evaluation.md", "LICENSE-APACHE-2.0"):
            self.assertTrue((creator / relative).is_file(), relative)
        self.assertTrue((creator / "scripts/validate_skill.py").stat().st_mode & 0o111)
        self.assertEqual((self.output / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
        portable = json.loads((self.output / "plugin.json").read_bytes())
        codex = json.loads((self.output / ".codex-plugin/plugin.json").read_bytes())
        for key, value in portable.items():
            if key != "$schema":
                self.assertEqual(codex[key], value)
        self.assertEqual(builder.build(ROOT, self.output, check=True), [])

    def test_check_reports_drift_without_writing_and_build_repairs_it(self):
        builder.build(ROOT, self.output)
        entrypoint = self.output / "skills/ck-teach/SKILL.md"
        entrypoint.write_text("local drift\n")
        missing = self.output / "skills/ck-how/LICENSE"
        missing.unlink()
        before = entrypoint.stat().st_mtime_ns
        changes = builder.build(ROOT, self.output, check=True)
        self.assertIn("skills/ck-teach/SKILL.md", changes)
        self.assertIn("skills/ck-how/LICENSE", changes)
        self.assertEqual(entrypoint.read_text(), "local drift\n")
        self.assertEqual(entrypoint.stat().st_mtime_ns, before)
        self.assertFalse(missing.exists())
        builder.build(ROOT, self.output)
        self.assertEqual(builder.build(ROOT, self.output, check=True), [])

    def test_unknown_user_file_prevents_all_writes(self):
        builder.build(ROOT, self.output)
        user_file = self.output / "notes.txt"
        user_file.write_text("keep me")
        entrypoint = self.output / "skills/ck-teach/SKILL.md"
        entrypoint.write_text("do not overwrite before preflight")
        with self.assertRaisesRegex(builder.BuildError, "Unknown output files"):
            builder.build(ROOT, self.output)
        self.assertEqual(user_file.read_text(), "keep me")
        self.assertEqual(entrypoint.read_text(), "do not overwrite before preflight")

    def test_unowned_directory_and_output_escape_are_rejected(self):
        self.output.mkdir()
        (self.output / "plugin.json").write_text("user's existing plugin")
        with self.assertRaisesRegex(builder.BuildError, "not owned"):
            builder.build(ROOT, self.output)
        with self.assertRaisesRegex(builder.BuildError, "restricted"):
            builder.build(ROOT, ROOT / "skills/ckstack")
        with self.assertRaisesRegex(builder.BuildError, "must be named"):
            builder.build(ROOT, self.base / "wrong-name")
        with self.assertRaisesRegex(builder.BuildError, "must not contain"):
            builder.build(ROOT, self.base / "elsewhere/../ckstack")
        alias = self.base / "alias"
        alias.mkdir()
        (alias / "ckstack").symlink_to(self.output, target_is_directory=True)
        with self.assertRaisesRegex(builder.BuildError, "symlink"):
            builder.build(ROOT, alias / "ckstack")
        self.assertEqual((self.output / "plugin.json").read_text(), "user's existing plugin")

    def test_source_symlinks_rejected_and_caches_excluded(self):
        source = self.base / "source"
        shutil.copytree(ROOT / "packaging", source / "packaging")
        shutil.copy2(ROOT / "LICENSE", source / "LICENSE")
        spec = json.loads((source / builder.SPEC).read_bytes())
        for name in spec["skills"]:
            shutil.copytree(ROOT / "skills" / name, source / "skills" / name)
        skill = source / "skills/ck-how"
        (skill / "__pycache__").mkdir()
        (skill / "__pycache__/ignored.pyc").write_bytes(b"cache")
        (skill / ".DS_Store").write_bytes(b"noise")
        builder.build(source, self.output)
        self.assertFalse((self.output / "skills/ck-how/__pycache__").exists())
        self.assertFalse((self.output / "skills/ck-how/.DS_Store").exists())
        (skill / "external.md").symlink_to(ROOT / "README.md")
        with self.assertRaisesRegex(builder.BuildError, "Source symlink"):
            builder.build(source, self.output)
        self.assertFalse((self.output / "skills/ck-how/external.md").exists())


if __name__ == "__main__":
    unittest.main()
