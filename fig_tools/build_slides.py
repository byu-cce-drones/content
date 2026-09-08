"""Export Marp lecture decks under docs/slides/ to HTML and PDF.

Every docs/slides/*.md that opens with `marp: true` in its front matter is a
deck. This script runs the Marp CLI once per deck with the course theme
(docs/slides/theme.css) and writes the exports next to the source Markdown,
which is where MkDocs will publish them from. Files without `marp: true` are
skipped, so this folder can hold notes or a README without choking the build.

Usage:
    /c/Users/williagp/anaconda3/python.exe fig_tools/build_slides.py
    /c/Users/williagp/anaconda3/python.exe fig_tools/build_slides.py --only week_05
    /c/Users/williagp/anaconda3/python.exe fig_tools/build_slides.py --pptx

Outputs (per deck, next to its .md):
    docs/slides/<deck>.html
    docs/slides/<deck>.pdf
    docs/slides/<deck>.pptx   only with --pptx

Requires the Marp CLI (`npm install -g @marp-team/marp-cli`). Run from the
repository root; paths below are resolved relative to this script's location
regardless of the working directory.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SLIDES_DIR = REPO_ROOT / "docs" / "slides"
THEME = SLIDES_DIR / "theme.css"


def find_marp() -> str | None:
    """Locate the Marp CLI executable, including the Windows .cmd shim."""
    exe = shutil.which("marp")
    if exe:
        return exe
    if sys.platform == "win32":
        exe = shutil.which("marp.cmd")
        if exe:
            return exe
    return None


def is_marp_deck(md_path: Path) -> bool:
    """True if the file's front matter declares `marp: true`."""
    try:
        head = md_path.read_text(encoding="utf-8").split("---", 2)
    except OSError:
        return False
    if len(head) < 3:
        return False
    front_matter = head[1]
    return any(line.strip() == "marp: true" for line in front_matter.splitlines())


def build_deck(marp_exe: str, md_path: Path, pptx: bool) -> bool:
    """Run Marp once per export format for one deck. Returns True if every
    export succeeded.

    Marp's `--html` flag does not mean "export HTML" — it means "allow raw
    HTML tags in the Markdown" — so plain HTML output is the CLI's default
    when no `--pdf`/`--pptx`/`--images` flag is given. Each format needs its
    own invocation with an explicit `-o` so the export always lands next to
    the source regardless of the current working directory.
    """
    base = ["--theme-set", str(THEME), "--allow-local-files", "--html"]
    jobs = [("html", []), ("pdf", ["--pdf"])]
    if pptx:
        jobs.append(("pptx", ["--pptx"]))

    ok = True
    for ext, flags in jobs:
        out_path = md_path.with_suffix(f".{ext}")
        cmd = [marp_exe, str(md_path), *base, *flags, "-o", str(out_path)]
        print("running:", " ".join(cmd))
        result = subprocess.run(cmd, cwd=REPO_ROOT)
        if result.returncode != 0:
            print(f"FAILED: {md_path.name} -> {ext} (exit {result.returncode})")
            ok = False
        else:
            print(f"built {out_path.name}")
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", help="build only the deck with this file stem, "
                                    "for example week_05")
    ap.add_argument("--pptx", action="store_true",
                     help="also export .pptx (off by default)")
    args = ap.parse_args()

    marp_exe = find_marp()
    if not marp_exe:
        print("Marp CLI not found. Install it with "
              "'npm install -g @marp-team/marp-cli' and make sure it is on "
              "PATH (or run 'marp --version' to check).")
        sys.exit(1)

    if not SLIDES_DIR.is_dir():
        print(f"no slides directory at {SLIDES_DIR}")
        sys.exit(1)

    md_files = sorted(SLIDES_DIR.glob("*.md"))
    if args.only:
        md_files = [p for p in md_files if p.stem == args.only]
        if not md_files:
            print(f"no deck named '{args.only}' in {SLIDES_DIR}")
            sys.exit(1)

    decks = [p for p in md_files if is_marp_deck(p)]
    skipped = [p for p in md_files if p not in decks]
    for p in skipped:
        print(f"skipping {p.name}: no 'marp: true' in front matter")

    if not decks:
        print("no Marp decks to build")
        sys.exit(1)

    failures = [p for p in decks if not build_deck(marp_exe, p, args.pptx)]

    if failures:
        print(f"{len(failures)} of {len(decks)} deck(s) failed to export")
        sys.exit(1)

    print(f"{len(decks)} deck(s) exported successfully")


if __name__ == "__main__":
    main()
