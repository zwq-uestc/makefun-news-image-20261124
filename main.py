#!/usr/bin/env python3
"""News-image entry: copy entry.png to the output directory.

Standard library only, no network, deterministic: the same bytes are
written on every run. The image was drawn by generate_image.py in this
repository (PIL, Noto Serif/Sans) from news verified on 24 November 2026.
"""
import hashlib
import os
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
out_dir.mkdir(parents=True, exist_ok=True)

src = here / "entry.png"
if not src.is_file() or src.stat().st_size == 0:
    print("entry.png is missing or empty", file=sys.stderr)
    raise SystemExit(1)
# Sanity check: it must be a 1024x1024 PNG (signature + IHDR width/height).
data = src.read_bytes()
if data[:8] != b"\x89PNG\r\n\x1a\n" or int.from_bytes(data[16:20], "big") != 1024:
    print("entry.png is not a 1024-wide PNG", file=sys.stderr)
    raise SystemExit(1)

tmp = out_dir / "entry.png.tmp"
tmp.write_bytes(data)
tmp.replace(out_dir / "entry.png")
print(f"wrote entry.png ({len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()[:12]})")
