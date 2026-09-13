#!/usr/bin/env python3
"""Reconstruct the two large source files from integrity-pinned bootstrap chunks."""
from pathlib import Path
import base64
import hashlib

ROOT = Path(__file__).resolve().parents[1]
BOOT = ROOT / ".bootstrap"

TARGETS = [
    (
        "antibody.py.b64.",
        ROOT / "contracts" / "antibody.py",
        "8da0806d06639fd5e78bec6bfdf0728af8f7d8a61095da5859fcbb44cb6c91e9",
    ),
    (
        "test_antibody.py.b64.",
        ROOT / "tests" / "direct" / "test_antibody.py",
        "c0c8130bfe17d6d47cf3a1eb4a4d2c458052d521e03a27abfd90c82297b9f62e",
    ),
]

for prefix, destination, expected_sha in TARGETS:
    parts = sorted(BOOT.glob(prefix + "*"))
    if not parts:
        raise SystemExit(f"missing bootstrap parts for {prefix}")
    encoded = "".join(part.read_text(encoding="utf-8").strip() for part in parts)
    decoded = base64.b64decode(encoded, validate=True)
    actual = hashlib.sha256(decoded).hexdigest()
    if actual != expected_sha:
        raise SystemExit(f"{destination}: sha256 mismatch {actual} != {expected_sha}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(decoded)
    print(f"{destination.relative_to(ROOT)} {actual}")

print("bootstrap assembly OK")
