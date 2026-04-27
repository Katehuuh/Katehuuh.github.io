#!/usr/bin/env python3
"""Run a CatBench Python entry and save its matplotlib figure as PNG.

Usage: render_python.py <input.py> <output.png>

Robust to scripts that call plt.show() instead of plt.savefig() — show is
patched to a no-op so the script doesn't block, and we save whatever's on
the canvas at exit. AI-generated kitten code rarely calls savefig itself.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(src: Path, out: Path) -> int:
    plt.show = lambda *a, **kw: None  # capture-and-continue

    # Pretend the user script was launched bare (no extra args), so any
    # argparse.parse_args() inside it sees no positional arguments and uses
    # defaults instead of erroring on our wrapper's argv.
    saved_argv = sys.argv
    sys.argv = [str(src)]

    namespace = {"__name__": "__main__", "__file__": str(src)}
    try:
        code = compile(src.read_text(encoding="utf-8"), str(src), "exec")
        exec(code, namespace)
    except SystemExit as e:
        # argparse can call sys.exit() on bad args; just continue and check figures.
        if e.code not in (None, 0):
            print(f"NOTE: {src.name} called sys.exit({e.code}); checking figures anyway", file=sys.stderr)
    except Exception as e:
        print(f"ERROR rendering {src}: {type(e).__name__}: {e}", file=sys.stderr)
        sys.argv = saved_argv
        return 1
    finally:
        sys.argv = saved_argv

    if not plt.get_fignums():
        print(f"WARN: no figure produced by {src}", file=sys.stderr)
        return 3

    out.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs = {"dpi": 120, "bbox_inches": "tight", "facecolor": "white"}
    if out.suffix.lower() in {".jpg", ".jpeg"}:
        save_kwargs["pil_kwargs"] = {"quality": 92, "optimize": True}
    plt.savefig(out, **save_kwargs)
    plt.close("all")
    print(f"saved {out}")
    return 0


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: render_python.py <input.py> <output.png>", file=sys.stderr)
        return 2
    return render(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    sys.exit(main())
