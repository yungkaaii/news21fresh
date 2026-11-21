#!/usr/bin/env python3
"""Entry point: copy the pre-rendered front page to /output/entry.png.

Pure Python 3.13 standard library only. No network, no timestamps, no
randomness: the copied bytes are exactly the bytes render.py produced,
so repeated runs are byte-identical.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "poster.png")
DST = "/output/entry.png"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    if sha256(SRC) != sha256(DST):
        raise SystemExit("copy verification failed: %s != %s" % (DST, SRC))
    print("wrote %s (%d bytes)" % (DST, os.path.getsize(DST)))


if __name__ == "__main__":
    sys.exit(main())
