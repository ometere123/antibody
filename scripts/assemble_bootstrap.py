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
        "c81657a575c6029cbfcdf4d05c3bf07eb1d6d07677ab207f542572a597f58d19",
    ),
    (
        "test_antibody.py.b64.",
        ROOT / "tests" / "direct" / "test_antibody.py",
        "8755ad106daadbc07c3d699a8a2dc17cc8a00561ca4d6d98f8c6710e5ffac3c3",
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
