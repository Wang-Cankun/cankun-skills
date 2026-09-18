#!/usr/bin/env python3
"""Build CK Stack from packaging/ckstack.json and unchanged skill directories.

An existing nonempty output must carry this generator's ownership marker.
Unknown files are never overwritten or removed; remove stale generated files
explicitly when changing the bundle's file list. --check never writes files.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
SPEC = Path("packaging/ckstack.json")
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MARKER = ".ckstack-build.json"
OWNER = {"generator": "cankun-skills/scripts/build_plugins.py", "plugin": "ckstack"}
IGNORED_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".DS_Store"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


class BuildError(Exception):
    """Invalid source or unsafe output; no destructive recovery is attempted."""


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def read_file(path: Path) -> tuple[bytes, int]:
    if path.is_symlink():
        raise BuildError(f"Source symlink is not portable: {path}")
    if not path.is_file():
        raise BuildError(f"Expected a regular source file: {path}")
    return path.read_bytes(), 0o755 if path.stat().st_mode & 0o111 else 0o644


def source_files(directory: Path):
    if directory.is_symlink():
        raise BuildError(f"Source symlink is not portable: {directory}")
    if not directory.is_dir():
        raise BuildError(f"Missing source directory: {directory}")
    for path in sorted(directory.iterdir()):
        if path.is_symlink():
            raise BuildError(f"Source symlink is not portable: {path}")
        if path.name in IGNORED_NAMES or path.suffix in IGNORED_SUFFIXES:
            continue
        if path.is_dir():
            yield from source_files(path)
        elif path.is_file():
            yield path
        else:
            raise BuildError(f"Unsupported source file type: {path}")


def expected_files(root: Path) -> dict[str, tuple[bytes, int]]:
    """Use an explicit JSON bundle list; SKILL.md content is never parsed."""
    spec = json.loads(read_file(root / SPEC)[0])
    plugin = spec["plugin"]
    if plugin.get("name") != "ckstack":
        raise BuildError("packaging/ckstack.json plugin.name must be ckstack")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", plugin.get("version", "")):
        raise BuildError("plugin.version must be a semantic version")
    skills = spec["skills"]
    if not isinstance(skills, list) or not skills or any(
        not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", name)
        for name in skills
    ) or len(skills) != len(set(skills)):
        raise BuildError("skills must be a nonempty list of unique skill directory names")
    if (root / "skills").is_symlink():
        raise BuildError(f"Source symlink is not portable: {root / 'skills'}")
    files = {
        "plugin.json": (json_bytes({"$schema": SCHEMA, **plugin}), 0o644),
        ".codex-plugin/plugin.json": (json_bytes({**plugin, "skills": "./skills/", "interface": spec["interface"]}), 0o644),
        "LICENSE": read_file(root / "LICENSE"),
    }
    for name in skills:
        directory = root / "skills" / name
        if not (directory / "SKILL.md").is_file():
            raise BuildError(f"Missing skill entrypoint: {directory / 'SKILL.md'}")
        for path in source_files(directory):
            files[path.relative_to(root).as_posix()] = read_file(path)
    files[MARKER] = (json_bytes({**OWNER, "files": sorted(files)}), 0o644)
    return files


def output_path(root: Path, requested: Path) -> Path:
    """Keep outputs away from the canonical source tree and symlink targets."""
    lexical = requested.expanduser().absolute()
    if ".." in lexical.parts:
        raise BuildError(f"Output path must not contain '..': {requested}")
    if lexical.name != "ckstack":
        raise BuildError("Output directory must be named ckstack")
    # Canonicalize the parent, allowing normal OS aliases such as /tmp. The
    # output itself must be a real directory, never a link to another tree.
    if lexical.is_symlink():
        raise BuildError(f"Output directory must not be a symlink: {lexical}")
    target = lexical.parent.resolve() / lexical.name
    root = root.resolve()
    if target == root or target in root.parents:
        raise BuildError(f"Output would contain the source repository: {target}")
    if root in target.parents and target != root / "plugins" / "ckstack":
        raise BuildError("Inside the repository, output is restricted to plugins/ckstack")
    if target.exists() and not target.is_dir():
        raise BuildError(f"Output is not a directory: {target}")
    return target


def inspect_output(target: Path, expected: dict[str, tuple[bytes, int]]) -> dict[str, Path]:
    if not target.exists():
        return {}
    actual = {}
    for path in sorted(target.rglob("*")):
        if path.is_symlink():
            raise BuildError(f"Output contains a symlink: {path}")
        if path.is_dir():
            # Empty directories also belong to somebody; refuse unrelated ones.
            prefix = path.relative_to(target).as_posix() + "/"
            if not any(name.startswith(prefix) for name in expected):
                raise BuildError(f"Unknown output directory: {path}")
        elif path.is_file():
            actual[path.relative_to(target).as_posix()] = path
        else:
            raise BuildError(f"Unsupported output file type: {path}")
    unknown = sorted(set(actual) - set(expected))
    if unknown:
        raise BuildError("Unknown output files; preserve or move them before building: " + ", ".join(unknown))
    if actual:
        marker = actual.get(MARKER)
        try:
            owner = json.loads(marker.read_bytes()) if marker else {}
        except (ValueError, OSError) as exc:
            raise BuildError(f"Cannot read output ownership marker: {target / MARKER}") from exc
        if not isinstance(owner, dict) or any(owner.get(key) != value for key, value in OWNER.items()):
            raise BuildError(f"Nonempty output is not owned by this generator: {target}")
    return actual


def atomic_write(path: Path, content: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".plugin-build-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        temporary.chmod(mode)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def build(root: Path, requested: Path, check: bool = False) -> list[str]:
    target = output_path(root, requested)
    expected = expected_files(root)
    actual = inspect_output(target, expected)
    changed = [name for name, (content, mode) in expected.items() if name not in actual
               or actual[name].read_bytes() != content
               or stat.S_IMODE(actual[name].stat().st_mode) != mode]
    if check:
        return changed
    # Establish ownership before the first payload write so an interrupted
    # initial build remains safely resumable. No existing directory is cleared.
    for name in ([MARKER] if MARKER in changed else []) + [name for name in changed if name != MARKER]:
        content, mode = expected[name]
        atomic_write(target / name, content, mode)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "plugins" / "ckstack",
                        help="Plugin root directory (must be named ckstack)")
    parser.add_argument("--check", action="store_true", help="Read-only comparison against source bytes and file list")
    args = parser.parse_args()
    try:
        changed = build(ROOT, args.output_dir, args.check)
    except (BuildError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if args.check and changed:
        print("Plugin drift: " + ", ".join(changed), file=sys.stderr)
        return 1
    print(f"{'Verified' if args.check else 'Built'} CK Stack: {args.output_dir} ({len(changed)} files changed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
