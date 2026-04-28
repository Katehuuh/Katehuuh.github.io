#!/usr/bin/env python3
"""Shared git utilities for the build pipeline."""
from __future__ import annotations

import subprocess
from pathlib import Path


def first_commit_iso(rel_path: str, cwd: Path) -> str | None:
    """ISO-8601 author date of the earliest commit that touched `rel_path`.
    Returns None if git fails or the path was never committed."""
    try:
        r = subprocess.run(
            ["git", "log", "--reverse", "--format=%aI", "--", rel_path],
            capture_output=True, text=True, cwd=cwd, check=False,
        )
        line = (r.stdout or "").strip().split("\n", 1)[0].strip()
        return line or None
    except Exception:
        return None
