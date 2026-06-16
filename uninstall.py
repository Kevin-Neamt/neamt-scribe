"""
Neamt Scribe — uninstall.py

Called by `neamt uninstall scribe` before removing skill files.
Asks whether to delete user notes; skill files themselves are removed by the CLI.
"""

from __future__ import annotations

import pathlib


_DATA_DIR = pathlib.Path.home() / ".neamt" / "data" / "scribe"


def _rmtree(path: pathlib.Path) -> int:
    """Recursively delete a directory tree using only pathlib (no shutil)."""
    count = 0
    if path.is_file() or path.is_symlink():
        path.unlink()
        return 1
    for child in path.iterdir():
        count += _rmtree(child)
    path.rmdir()
    return count


def uninstall() -> None:
    print("Neamt Scribe — uninstall")
    print("=" * 40)

    if not _DATA_DIR.exists():
        print("No Scribe data directory found — nothing to clean up.")
        return

    notes_dir = _DATA_DIR / "notes"
    note_count = len(list(notes_dir.glob("*.md"))) if notes_dir.exists() else 0

    print(f"\nFound {note_count} note(s) in {_DATA_DIR}")
    answer = input("\nDelete all Scribe notes and data? This cannot be undone. [y/N] ").strip().lower()

    if answer == "y":
        deleted = _rmtree(_DATA_DIR)
        print(f"✓ Deleted {deleted} file(s)/director(ies) from {_DATA_DIR}")
    else:
        print("Notes preserved — skill files will be removed but your notes stay.")
        print(f"  Location: {_DATA_DIR}")


if __name__ == "__main__":
    uninstall()
