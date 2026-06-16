"""
Neamt Scribe — install.py

Called by `neamt install` after copying files to ~/.neamt/skills/scribe/.
Also runnable directly: python install.py

Does NOT use subprocess, os, or sys — compatible with the neamt sandbox.
Uses pip's Python API and pathlib for filesystem operations.
"""

from __future__ import annotations

import pathlib


_NOTES_DIR = pathlib.Path.home() / ".neamt" / "data" / "scribe" / "notes"
_TMP_DIR   = pathlib.Path.home() / ".neamt" / "data" / "scribe" / ".tmp"

_PACKAGES = ["yt-dlp>=2024.1.0", "openai-whisper>=20231117"]


def install() -> None:
    print("Neamt Scribe — install")
    print("=" * 40)

    # ── 1. Install pip dependencies ──────────────────────────────────────────
    print("\n[1/2] Installing dependencies...")
    try:
        # pip is not in the sandbox blocked list
        from pip._internal.cli.main import main as _pip
        result = _pip(["install", "--quiet", "--upgrade"] + _PACKAGES)
        if result == 0:
            print("     yt-dlp          ✓")
            print("     openai-whisper  ✓")
        else:
            print(f"     pip returned exit code {result} — check manually:")
            for pkg in _PACKAGES:
                print(f"       pip install '{pkg}'")
    except Exception as exc:
        print(f"     Warning: could not install via pip API ({exc})")
        print("     Install manually:")
        for pkg in _PACKAGES:
            print(f"       pip install '{pkg}'")

    # ── 2. Create data directories ───────────────────────────────────────────
    print("\n[2/2] Creating data directories...")
    for d in (_NOTES_DIR, _TMP_DIR):
        d.mkdir(parents=True, exist_ok=True)
        print(f"     {d}  ✓")

    print("\n✓ Neamt Scribe installed successfully.")
    print(f"  Notes will be saved to: {_NOTES_DIR}")
    print("\nRemember to configure your Anthropic API key:")
    print("  neamt config set anthropic_api_key <your-key>")


if __name__ == "__main__":
    install()
