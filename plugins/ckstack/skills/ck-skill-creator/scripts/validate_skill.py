#!/usr/bin/env python3
"""Check portable skill metadata and local resource links; no behavioral claims."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


def validate(directory: Path) -> list[str]:
    errors = []
    entrypoint = directory / "SKILL.md"
    if not entrypoint.is_file():
        return ["Missing SKILL.md"]
    text = entrypoint.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
    if not match:
        return ["Expected YAML frontmatter delimited by --- lines"]
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return [f"Invalid YAML: {exc}"]
    if not isinstance(metadata, dict):
        return ["Frontmatter must be a mapping"]
    name = metadata.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("name must be a nonempty lowercase kebab name of at most 64 characters")
    elif directory.name != name:
        errors.append(f"Directory name {directory.name!r} differs from skill name {name!r}")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("description must be a nonempty string")

    # Inspect Markdown resources reachable from the entrypoint, skipping sample
    # code fences. Host-specific metadata and Markdown anchors need host checks.
    pending, seen = [entrypoint], set()
    while pending:
        source = pending.pop()
        resolved = source.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        lines, fence = [], None
        for line in source.read_text(encoding="utf-8").splitlines():
            opening = re.match(r"^\s*(`{3,}|~{3,})", line)
            if opening:
                marker = opening.group(1)
                if fence is None:
                    fence = marker
                elif marker[0] == fence[0] and len(marker) >= len(fence):
                    fence = None
                continue
            if fence is None:
                lines.append(line)
        for raw in re.findall(r"!?\[[^\]]*\]\(([^\n]+?)\)", "\n".join(lines)):
            target = raw.strip()
            target = target[1:target.index(">")] if target.startswith("<") and ">" in target else target.split()[0]
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = Path(unquote(parsed.path))
            if path.is_absolute():
                errors.append(f"{source.name}: nonportable absolute link {target}")
                continue
            linked = (source.parent / path).resolve()
            if not linked.is_relative_to(directory.resolve()):
                errors.append(f"{source.name}: link leaves skill package: {target}")
            elif not linked.exists():
                errors.append(f"{source.name}: missing resource: {target}")
            elif linked.is_file() and linked.suffix.lower() == ".md":
                pending.append(linked)
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_skill.py <skill-directory>", file=sys.stderr)
        return 2
    try:
        errors = validate(Path(sys.argv[1]).expanduser().absolute())
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Portable metadata and linked resources are valid; behavior was not tested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
