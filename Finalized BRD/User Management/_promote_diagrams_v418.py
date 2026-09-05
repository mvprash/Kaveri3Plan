# -*- coding: utf-8 -*-
"""Promote the refreshed .drawio diagrams and PNG exports into the canonical
ProcessDiagrams/User_Management folder referenced by the BRD.

Existing files are archived under _superseded_v4.17/ rather than deleted.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent
CANON = BASE / "ProcessDiagrams" / "User_Management"
NEW = CANON / "NewProcessDiagrams" / "ProcessDiagrams"
ARCHIVE = CANON / "_superseded_v4.17"


def main() -> None:
    if not NEW.is_dir():
        raise FileNotFoundError(NEW)
    ARCHIVE.mkdir(exist_ok=True)

    archived = 0
    for old in sorted(list(CANON.glob("*.drawio")) + list(CANON.glob("*.drawio.png"))):
        shutil.move(str(old), str(ARCHIVE / old.name))
        archived += 1

    copied = 0
    for src in sorted(NEW.glob("*.drawio")):
        shutil.copy2(src, CANON / src.name)
        copied += 1
    for src in sorted(NEW.glob("*.png")):
        shutil.copy2(src, CANON / f"{src.stem}.drawio.png")
        copied += 1

    print(f"archived {archived} file(s) to {ARCHIVE}")
    print(f"copied {copied} file(s) into {CANON}")


if __name__ == "__main__":
    main()
