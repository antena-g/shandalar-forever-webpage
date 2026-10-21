"""Copy the game files the website uses into game-assets/.

The site is built from game-assets/ so that it does not depend on the game
repository. Run this again when the game's converted art or card data changes,
or when the site starts using new art:

    uv run python scripts/sync_game_assets.py [path/to/shandalar-forever/assets/original]

It builds the site once from the game's own assets folder, records every file
the build opens there, and copies exactly those files.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

from shandalar_site.build import WEBSITE, build

GAME_ASSETS = WEBSITE / "game-assets"
DEFAULT_SOURCE = WEBSITE.parent / "shandalar-forever" / "assets" / "original"


def main(source: Path) -> None:
    source = source.resolve()
    used: set[Path] = set()

    # Python raises an "open" audit event for every file opened, including
    # those opened by Pillow and shutil.
    def record(event: str, args: tuple) -> None:
        if event == "open" and isinstance(args[0], (str, Path)):
            path = Path(args[0]).resolve()
            if path.is_relative_to(source):
                used.add(path)

    sys.addaudithook(record)
    with tempfile.TemporaryDirectory() as out:
        build(Path(out), source)

    shutil.rmtree(GAME_ASSETS, ignore_errors=True)
    for path in sorted(used):
        dest = GAME_ASSETS / path.relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)

    size = sum(path.stat().st_size for path in GAME_ASSETS.rglob("*") if path.is_file())
    print(f"Copied {len(used)} files ({size / 1_000_000:.1f} MB) into {GAME_ASSETS}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE)
