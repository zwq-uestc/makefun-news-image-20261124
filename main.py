#!/usr/bin/env python3
"""News-image entry: copy entry.png to the output directory.

Standard library only, no network, deterministic: the same bytes are
written on every run. The image was drawn by generate_image.py in this
repository (PIL, DejaVu fonts) from news verified on 24 November 2026.
"""
import os
import shutil
from pathlib import Path

here = Path(__file__).resolve().parent
out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
out_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(here / "entry.png", out_dir / "entry.png")
