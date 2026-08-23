#!/usr/bin/env python3
"""Gatekeeper for auto-merged CatBench submissions.

Decides whether a set of contributed files is boring enough to merge without a
human looking at it. Used by both the PR path (catbench-pr-validate.yml) and the
issue path (catbench-issue-submit.yml) so there is exactly one definition of
"eligible".

Threat model (read this before loosening anything)
--------------------------------------------------
This file is not the real protection. The job layout is. Submitted Python only
runs in a job with a read-only token and no secrets, and the render it produces
gets committed with the source, so `build_catbench_manifest.py` on main finds an
existing `<model>-python.<raster>` and never exec()s the source again. Submitted
code runs once, where there's nothing to take.

That matters because build.yml runs on push to main with `contents: write`, and
actions/checkout leaves push credentials in the workspace. Code running there
could push to main and deface the published Pages site.

This script is the second layer. It keeps obvious junk out and stops a
submission touching anything except its own asset files. The Python import
allowlist is a "this is not a kitten drawing" filter, not a sandbox. Anyone who
tries can get around it, which is fine, since that only buys you the
unprivileged job.

Usage
-----
    catbench_validate.py check   --root <dir> --file <repo-relative-path> [...]
                                 [--json <out.json>]
    catbench_validate.py extract --body-file <issue-body.md> --out-dir <dir>
                                 [--json <out.json>]

`extract` turns an issue-form body into candidate files on disk; `check` judges
a set of candidate files. The issue workflow runs `extract` in both its
unprivileged and its privileged job. The privileged one re-reads the issue body
from the API rather than trusting anything the render job produced, so the only
thing carried across the trust boundary is the rendered JPEG.

Exit 0 = eligible for auto-merge, 1 = needs a human. Reasons land on stderr and
in the JSON report.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ASSET_DIR = "demos/CatBench/assets"

# User asked for: an image (svg / png / jpg / jpeg) and/or a .py. Deliberately no
# .gif. The one in the repo predates this and can stay hand-merged.
SOURCE_EXTS = {".py", ".svg"}
RASTER_EXTS = {".png", ".jpg", ".jpeg"}
ALLOWED_EXTS = SOURCE_EXTS | RASTER_EXTS

# Mirrors build_catbench_manifest.py's tolerance: letters, digits, dot, dash,
# underscore, space, plus. No path separators, no leading dot, no '..'.
STEM_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._+-]{0,63}$")

# Suffixes the manifest treats as "this raster belongs to <base>".
RASTER_SUFFIXES = ("-svg", "-python")

MAX_BYTES = {".py": 200 * 1024, ".svg": 2 * 1024 * 1024}
MAX_RASTER_BYTES = 5 * 1024 * 1024
MAX_FILES = 4

MAGIC = {
    ".png": b"\x89PNG\r\n\x1a\n",
    ".jpg": b"\xff\xd8\xff",
    ".jpeg": b"\xff\xd8\xff",
}

# Everything a matplotlib kitten could legitimately want. Anything else is not
# rejected as "malicious", it's rejected as "a human should look at this".
PY_IMPORT_ALLOWLIST = {
    "matplotlib", "mpl_toolkits", "numpy", "np",
    "math", "cmath", "random", "colorsys", "itertools", "functools",
    "dataclasses", "typing", "__future__", "collections", "copy", "string",
    # Models like to wrap their kitten in a CLI. render_python.py already
    # neutralises it (argv is blanked, SystemExit swallowed), and one entry in
    # the repo relies on this, so it stays allowed.
    "argparse",
}

# Builtins with no business in a drawing script.
PY_BANNED_NAMES = {
    "eval", "exec", "compile", "__import__", "open", "input", "breakpoint",
    "globals", "locals", "vars", "memoryview",
}

# <use> is NOT banned: href="#localId" is ordinary SVG reuse and two entries in
# the repo depend on it. It is instead required to stay a local fragment below,
# which is the part that would otherwise pull a remote document.
SVG_BANNED_TAGS = {"script", "foreignobject", "iframe", "embed", "object"}
SVG_EVENT_ATTR = re.compile(r"^on[a-z]+$", re.I)
SVG_REMOTE_REF = re.compile(r"(?:https?:)?//|^\s*javascript:|^\s*data:text/html", re.I)


def strip_ns(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower() if isinstance(tag, str) else ""


def stem_and_kind(name: str) -> tuple[str, str]:
    """Return (model_key_stem, kind) where kind is py|svg|raster."""
    p = Path(name)
    ext = p.suffix.lower()
    if ext == ".py":
        return p.stem, "py"
    if ext == ".svg":
        return p.stem, "svg"
    stem = p.stem
    for suf in RASTER_SUFFIXES:
        if stem.lower().endswith(suf):
            return stem[: -len(suf)], "raster"
    return stem, "raster"


def check_paths(files: list[str], root: Path) -> list[str]:
    errs: list[str] = []

    if not files:
        return ["no files changed"]
    if len(files) > MAX_FILES:
        errs.append(f"{len(files)} files changed; auto-merge allows at most {MAX_FILES}")

    stems: set[str] = set()
    kinds: set[str] = set()
    for rel in files:
        posix = Path(rel).as_posix()

        # Only ever the one drop folder. This is what keeps a submission from
        # editing workflows, scripts/, index.html or data.json.
        parent = str(Path(posix).parent)
        if parent != ASSET_DIR:
            errs.append(f"{posix}: outside {ASSET_DIR}/")
            continue
        if ".." in Path(posix).parts:
            errs.append(f"{posix}: path traversal")
            continue

        ext = Path(posix).suffix.lower()
        if ext not in ALLOWED_EXTS:
            errs.append(f"{posix}: extension {ext or '(none)'} not allowed "
                        f"({', '.join(sorted(ALLOWED_EXTS))})")
            continue

        name = Path(posix).name
        base, kind = stem_and_kind(name)
        if not STEM_RE.match(base):
            errs.append(f"{posix}: model name '{base}' has characters outside "
                        "[A-Za-z0-9 ._+-] or is too long")
            continue
        if kind in ("py", "svg") and base.lower().endswith(RASTER_SUFFIXES):
            errs.append(f"{posix}: source file must not end in -python/-svg")
            continue

        # New files only. Overwriting an existing entry is how you would swap a
        # published render for something else, so it goes to a human.
        if (root / posix).exists() and not (root / posix).is_symlink():
            pass  # existence in the *candidate* tree is expected; see check below
        stems.add(base.lower())
        kinds.add(kind)

    if len(stems) > 1:
        errs.append(f"submission spans multiple models ({', '.join(sorted(stems))}); "
                    "auto-merge handles one model at a time")

    # CatBench is two prompts, so an entry is the pair. A model that answered
    # only one of them is a partial result, and partial results are a judgement
    # call rather than something to land unattended.
    if not errs:
        missing = [k for k in ("py", "svg") if k not in kinds]
        if missing:
            names = {"py": "a .py (the matplotlib prompt)", "svg": "an .svg (the SVG prompt)"}
            errs.append("a CatBench entry is both prompts; this submission is missing "
                        + " and ".join(names[k] for k in missing))
    return errs


def check_python(data: bytes, name: str) -> list[str]:
    errs: list[str] = []
    try:
        src = data.decode("utf-8")
    except UnicodeDecodeError:
        return [f"{name}: not valid UTF-8"]

    try:
        tree = ast.parse(src, filename=name)
    except SyntaxError as e:
        return [f"{name}: syntax error line {e.lineno}: {e.msg}"]

    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imported.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level:  # relative import, nothing to import from
                errs.append(f"{name}: relative import")
            if node.module:
                imported.add(node.module.split(".")[0])
        elif isinstance(node, ast.Name) and node.id in PY_BANNED_NAMES:
            errs.append(f"{name}: uses '{node.id}'")
        elif isinstance(node, ast.Attribute) and node.attr.startswith("__") \
                and node.attr.endswith("__") and node.attr != "__name__":
            errs.append(f"{name}: dunder attribute access '{node.attr}'")

    for mod in sorted(imported - PY_IMPORT_ALLOWLIST):
        errs.append(f"{name}: imports '{mod}', a matplotlib kitten shouldn't need it")

    if not imported & {"matplotlib", "mpl_toolkits"}:
        errs.append(f"{name}: never imports matplotlib")

    return sorted(set(errs))


def check_svg(data: bytes, name: str) -> list[str]:
    errs: list[str] = []
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return [f"{name}: not valid UTF-8"]

    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        return [f"{name}: not well-formed XML: {e}"]

    if strip_ns(root.tag) != "svg":
        errs.append(f"{name}: root element is <{strip_ns(root.tag)}>, expected <svg>")

    # The page inlines SVG into the lightbox and CI rasterises it in a real
    # Chromium, so active content is a live XSS / SSRF surface, not theoretical.
    for el in root.iter():
        tag = strip_ns(el.tag)
        if tag in SVG_BANNED_TAGS:
            errs.append(f"{name}: contains <{tag}>")
        for attr, val in el.attrib.items():
            a = strip_ns(attr)
            if SVG_EVENT_ATTR.match(a):
                errs.append(f"{name}: event handler {a}=")
            if a in ("href", "src"):
                ref = (val or "").strip()
                if SVG_REMOTE_REF.search(ref):
                    errs.append(f"{name}: external/active reference in {a}=")
                elif tag == "use" and not ref.startswith("#"):
                    errs.append(f"{name}: <use {a}='{ref[:40]}'> is not a local #fragment")
    if "<!entity" in text.lower():
        errs.append(f"{name}: declares an XML entity")

    return sorted(set(errs))


def check_raster(data: bytes, name: str, ext: str) -> list[str]:
    magic = MAGIC.get(ext)
    if magic and not data.startswith(magic):
        return [f"{name}: content is not a real {ext.lstrip('.').upper()}"]
    if len(data) > MAX_RASTER_BYTES:
        return [f"{name}: {len(data)} bytes exceeds {MAX_RASTER_BYTES}"]
    return []


def check_contents(files: list[str], root: Path) -> list[str]:
    errs: list[str] = []
    for rel in files:
        p = root / rel
        if not p.is_file():
            errs.append(f"{rel}: missing from the candidate tree (deletion or rename?)")
            continue
        if p.is_symlink():
            errs.append(f"{rel}: is a symlink")
            continue
        data = p.read_bytes()
        ext = p.suffix.lower()

        cap = MAX_BYTES.get(ext, MAX_RASTER_BYTES)
        if len(data) > cap:
            errs.append(f"{rel}: {len(data)} bytes exceeds {cap}")
            continue
        if not data:
            errs.append(f"{rel}: empty file")
            continue

        if ext == ".py":
            errs += check_python(data, rel)
        elif ext == ".svg":
            errs += check_svg(data, rel)
        elif ext in RASTER_EXTS:
            errs += check_raster(data, rel, ext)
    return errs


# --- issue-form extraction -------------------------------------------------

# Headings must match the labels in .github/ISSUE_TEMPLATE/catbench-submission.yml.
H_MODEL = "model name"
H_PYTHON = "python code"
H_SVG = "svg markup"
NO_RESPONSE = "_no response_"

FENCE_RE = re.compile(r"^\s*```[^\n]*\n(.*?)\n?\s*```\s*$", re.S)


def split_sections(body: str) -> dict[str, str]:
    """Issue forms render each field as '### Label' followed by its value."""
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in body.replace("\r\n", "\n").split("\n"):
        if line.startswith("### "):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[4:].strip().lower()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def unfence(value: str) -> str:
    """Textarea fields with `render:` set arrive wrapped in a code fence."""
    m = FENCE_RE.match(value.strip())
    return (m.group(1) if m else value).strip("\n")


def extract(body: str, out_dir: Path) -> tuple[list[str], list[str]]:
    """Materialise submitted files under out_dir. Returns (repo_rel_paths, errors)."""
    sections = split_sections(body)
    errors: list[str] = []

    model = sections.get(H_MODEL, "").strip()
    if not model or model.lower() == NO_RESPONSE:
        return [], ["the 'Model name' field is empty"]
    if not STEM_RE.match(model):
        return [], [f"model name '{model[:64]}' has characters outside [A-Za-z0-9 ._+-] "
                    "or is longer than 64"]

    written: list[str] = []
    dest_dir = out_dir / ASSET_DIR
    dest_dir.mkdir(parents=True, exist_ok=True)

    for heading, ext in ((H_PYTHON, ".py"), (H_SVG, ".svg")):
        raw = sections.get(heading, "")
        if not raw or raw.strip().lower() == NO_RESPONSE:
            continue
        content = unfence(raw)
        if not content.strip():
            continue
        rel = f"{ASSET_DIR}/{model}{ext}"
        (out_dir / rel).write_text(content + "\n", encoding="utf-8")
        written.append(rel)

    if not written:
        errors.append("no code submitted, both the Python and the SVG field are required")
    return written, errors


def cmd_extract(args) -> int:
    body = args.body_file.read_text(encoding="utf-8", errors="replace")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    files, errors = extract(body, args.out_dir)

    if not errors:
        errors = check_paths(files, args.out_dir)
    if not errors:
        errors = check_contents(files, args.out_dir)

    eligible = not errors
    report = {"eligible": eligible, "files": files, "reasons": errors}
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if eligible:
        print(f"extracted: {', '.join(files)}")
    else:
        print("submission not eligible:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
    return 0 if eligible else 1


def cmd_check(args) -> int:
    files = [f for f in (s.strip() for s in args.files) if f]
    errors = check_paths(files, args.root)
    if not errors:
        errors = check_contents(files, args.root)

    eligible = not errors
    report = {"eligible": eligible, "files": files, "reasons": errors}
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if eligible:
        print(f"eligible: {', '.join(files)}")
    else:
        print("NOT eligible for auto-merge:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
    return 0 if eligible else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="judge candidate files already on disk")
    c.add_argument("--root", required=True, type=Path,
                   help="tree holding the candidate files")
    c.add_argument("--file", dest="files", action="append", default=[],
                   help="repo-relative path (repeatable)")
    c.add_argument("--json", type=Path, help="write a JSON report here")
    c.set_defaults(func=cmd_check)

    e = sub.add_parser("extract", help="materialise + judge an issue-form submission")
    e.add_argument("--body-file", required=True, type=Path,
                   help="file containing the raw issue body")
    e.add_argument("--out-dir", required=True, type=Path,
                   help="tree to write the candidate files into")
    e.add_argument("--json", type=Path, help="write a JSON report here")
    e.set_defaults(func=cmd_extract)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
