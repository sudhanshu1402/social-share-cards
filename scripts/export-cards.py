#!/usr/bin/env python3
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
SETTLE = 30
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CAP = re.compile(r'class="cap">.*?<b>([\w.-]+)\.png</b>')
CARD = re.compile(r'<div class="card"[^>]*>')
OPEN = re.compile(r"<div\b")
CLOSE = re.compile(r"</div>")


def head(src):
    return src[: src.index("</head>")] + "<style>body{padding:0}</style></head>"


# The card is one balanced div, so count tags instead of trusting a regex to stop in the right place.
def card_at(src, start):
    found = CARD.search(src, start)
    if found is None:
        raise ValueError("caption with no card after it")
    begin = found.start()
    depth = 0
    pos = begin
    while True:
        nxt_open = OPEN.search(src, pos)
        nxt_close = CLOSE.search(src, pos)
        if nxt_close is None:
            raise ValueError("unbalanced card markup")
        if nxt_open and nxt_open.start() < nxt_close.start():
            depth += 1
            pos = nxt_open.end()
            continue
        depth -= 1
        pos = nxt_close.end()
        if depth == 0:
            return src[begin:pos]


def cards(src):
    out = {}
    for cap in CAP.finditer(src):
        out[cap.group(1)] = card_at(src, cap.end())
    return out


def shoot(html, out):
    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp) / "card.html"
        page.write_text(html, encoding="utf-8")
        shot = pathlib.Path(tmp) / "out.png"
        proc = subprocess.Popen(
            [
                CHROME,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                f"--user-data-dir={tmp}/profile",
                "--no-first-run",
                "--no-default-browser-check",
                # New headless does not always exit after the screenshot; the budget ends the run.
                "--virtual-time-budget=2000",
                "--window-size=1280,640",
                f"--screenshot={shot}",
                page.as_uri(),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # It writes the PNG in a second or two, then often refuses to exit, so wait on the file.
        try:
            for _ in range(SETTLE):
                if proc.poll() is not None:
                    break
                if shot.exists() and shot.stat().st_size > 0:
                    size = shot.stat().st_size
                    time.sleep(1)
                    if shot.stat().st_size == size:
                        break
                time.sleep(1)
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        if not shot.exists():
            raise RuntimeError(f"chrome wrote no screenshot for {out.name}")
        # A crash mid-write leaves a PNG with a valid header and no end, which the checker passes.
        if shot.read_bytes()[-12:-4] != b"\x00\x00\x00\x00IEND":
            raise RuntimeError(f"chrome wrote a truncated png for {out.name}")
        # Move only after the render finished, so an interrupt cannot destroy the tracked export.
        shutil.move(shot, out)


def main(argv):
    if not pathlib.Path(CHROME).exists():
        print(f"FAIL {CHROME} not found", file=sys.stderr)
        return 1
    found = {}
    for tpl in sorted(ROOT.glob("templates/*.html")):
        src = tpl.read_text(encoding="utf-8")
        for name, card in cards(src).items():
            found[name] = f"{head(src)}<body>{card}</body></html>"

    wanted = argv or sorted(found)
    missing = [name for name in wanted if name not in found]
    for name in missing:
        print(f"FAIL {name}: no card declares {name}.png", file=sys.stderr)

    (ROOT / "exports").mkdir(exist_ok=True)
    for name in wanted:
        if name in missing:
            continue
        out = ROOT / "exports" / f"{name}.png"
        shoot(found[name], out)
        print(f"wrote exports/{name}.png")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
