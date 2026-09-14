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
        "1987c967255bc4e1a49eef04561403d472994ab6df8cc74f3493759d71856828",
    ),
    (
        "test_antibody.py.b64.",
        ROOT / "tests" / "direct" / "test_antibody.py",
        "fd2ba7ca94c6a9809557a9dc9e646afea90397c82f6147c80ccf3e2620855de2",
    ),
]

assembled = []
for prefix, destination, expected_sha in TARGETS:
    parts = sorted(BOOT.glob(prefix + "*"))
    if not parts:
        raise SystemExit(f"missing bootstrap parts for {prefix}")
    encoded = "".join(part.read_text(encoding="utf-8").strip() for part in parts)
    decoded = base64.b64decode(encoded, validate=True)
    actual = hashlib.sha256(decoded).hexdigest()
    print(f"{destination.relative_to(ROOT)} actual_sha256={actual} expected_sha256={expected_sha}")
    assembled.append((destination, decoded, actual, expected_sha))

mismatches = [
    f"{destination.relative_to(ROOT)}: {actual} != {expected}"
    for destination, _decoded, actual, expected in assembled
    if actual != expected
]
if mismatches:
    raise SystemExit("bootstrap integrity mismatch: " + "; ".join(mismatches))

for destination, decoded, _actual, _expected in assembled:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(decoded)

print("bootstrap assembly OK")
