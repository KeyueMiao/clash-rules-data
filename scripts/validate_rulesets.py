#!/usr/bin/env python3
"""Validate source rule-sets without third-party Python dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOMAIN_PATTERN = re.compile(
    r"^  - '\+\.([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
    r"(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+)'$"
)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    domains: set[str] = set()
    saw_payload = False

    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line or line.lstrip().startswith("#"):
            continue
        if line == "payload:":
            saw_payload = True
            continue
        match = DOMAIN_PATTERN.fullmatch(line)
        if not match:
            errors.append(f"{path}:{number}: invalid entry: {line}")
            continue
        domain = match.group(1)
        if domain in domains:
            errors.append(f"{path}:{number}: duplicate domain: {domain}")
        domains.add(domain)

    if not saw_payload:
        errors.append(f"{path}: missing payload: key")
    if not domains:
        errors.append(f"{path}: no domains found")
    print(f"{path}: {len(domains)} domains")
    return errors


def main() -> int:
    source_dir = Path("geo/geosite")
    paths = sorted(source_dir.glob("*.yaml"))
    if not paths:
        print("No source YAML files found.", file=sys.stderr)
        return 1
    errors = [error for path in paths for error in validate(path)]
    if errors:
        print(*errors, sep="\n", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

