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
        "19df96c5964f2da5a12765188cad10b102994c6ce1d0b9ba2194e113891a70e0",
    ),
    (
        "test_antibody.py.b64.",
        ROOT / "tests" / "direct" / "test_antibody.py",
        "aa453ceda2664b93fcc63735fef6dbbd95c615d803d953a3e35c433b3331ffee",
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
