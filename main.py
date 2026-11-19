#!/usr/bin/env python3
"""Entry for make.fun bounty news-image-20261119.

Writes the shipped entry.png (a one-page digest of Thursday
19 November 2026's world news) to /output/entry.png, byte for byte,
so repeated runs are identical. Standard library only, no network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
