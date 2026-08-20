#!/usr/bin/env python3
import pathlib
import re
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WANT = (1280, 640)
DECLARED = re.compile(r'class="cap">.*?<b>([\w.-]+\.png)</b>')
CARD = re.compile(r'class="card"')


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError("not a PNG")
    return struct.unpack(">II", head[16:24])


def main():
    fails = []

    found = {p.name for p in ROOT.glob("exports/*.png")}
    for name in sorted(found):
        try:
            size = png_size(ROOT / "exports" / name)
        except (OSError, ValueError, struct.error) as err:
            fails.append(f"exports/{name}: unreadable ({err})")
            continue
        if size != WANT:
            fails.append(f"exports/{name}: {size[0]}x{size[1]}, want 1280x640")

    declared = set()
    for tpl in sorted(ROOT.glob("templates/*.html")):
        src = tpl.read_text(encoding="utf-8")
        names = DECLARED.findall(src)
        cards = len(CARD.findall(src))
        if len(names) != cards:
            fails.append(f"templates/{tpl.name}: {cards} cards, {len(names)} declared .cap filenames")
        declared.update(names)

    for name in sorted(declared - found):
        fails.append(f"exports/{name}: declared in templates/, not exported")
    for name in sorted(found - declared):
        fails.append(f"exports/{name}: exported, no card declares it")

    for line in fails:
        print(f"FAIL {line}", file=sys.stderr)
    print(f"checked {len(found)} exports against {len(declared)} declared cards, {len(fails)} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
