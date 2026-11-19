#!/usr/bin/env python3
"""Entry point for the make.fun bounty news-image-20261119.

The entry image (a one-page digest of Thursday 19 November 2026's
world news, drawn by build_image.py) ships in this repository as
entry.png. This program copies it to /output/entry.png byte for byte,
so the sealed harness's two runs produce identical output.
Standard library only; no network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main() -> None:
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    print("wrote", target, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    main()
