#!/usr/bin/env python3
"""
make_all.py — one-click reproduction runner.
- Generates CSV tables (表1–表3)
- Generates Figures 1–3
Options:
  --clean    Remove previous outputs in ./results before running
  --quiet    Suppress subprocess stdout
"""
import argparse, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"

def run(cmd, quiet=False):
    if quiet:
        subprocess.run(cmd, cwd=HERE, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    else:
        subprocess.run(cmd, cwd=HERE, check=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clean", action="store_true", help="remove previous outputs in ./results")
    ap.add_argument("--quiet", action="store_true", help="suppress subprocess outputs")
    args = ap.parse_args()

    RESULTS.mkdir(exist_ok=True, parents=True)
    if args.clean:
        for p in RESULTS.glob("*"):
            try:
                if p.is_file():
                    p.unlink()
                elif p.is_dir():
                    shutil.rmtree(p)
            except Exception as e:
                print(f"[warn] cannot remove {p}: {e}")

    # Step 1: Tables
    run([sys.executable, "make_tables.py"], quiet=args.quiet)

    # Step 2: Figures (will use CSVs or fallback to embedded)
    run([sys.executable, "make_figures.py"], quiet=args.quiet)

    print("✅ Done. See ./results for CSVs and PNGs.")

if __name__ == "__main__":
    main()
