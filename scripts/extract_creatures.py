"""Extract Shandalar's creature table from the original MAGIC.EXE into a CSV.

The executable is not shipped with Shandalar Forever, so this runs once against
the reference copy and its output, content/creatures.csv, is kept in the
website. Run it again only if the reference game changes:

    python scripts/extract_creatures.py ../microprose-shandalar-source/game-data/MAGIC.EXE

The table is a list of 68-byte records: a 20-byte name, a 20-byte plural, then
28 bytes of data. Byte 3 of the data is a colour mask and bytes 4-5 are the
number of the creature's deck in DECKS/. A record's position in the table is
the creature type the engine uses to pick its overworld sprite.
"""

from __future__ import annotations

import csv
import hashlib
import struct
import sys
from pathlib import Path

# SHA-256 of the accepted 1.0 MAGIC.EXE; the offsets below only hold for it.
MAGIC_EXE_SHA256 = "21c2cc676de952cda782327048f9533345aba4cd5760f422d675def8f8947267"
TABLE_START = 0x120000  # The "Lair" record, the first in the table.
RECORD_SIZE = 68
COUNT = 56  # Lair, 54 creatures and Arzakon.

COLOR_BITS = {2: "black", 4: "blue", 8: "green", 16: "red", 32: "white"}

# Creature type -> overworld sprite folder, from the sprite switch in the
# recovered engine (magic/world/engine_core.c). Types without a sprite, such
# as the Guild Lords, never walk the overworld.
SPRITES = {
    1: "BK_FWZ", 2: "BK_KHT", 3: "BK_MWZ", 4: "BK_LRD", 5: "BK_WG", 6: "BK_AMG",
    8: "W_MWZ", 9: "W_FWZ", 10: "W_KHT", 11: "W_LRD", 12: "W_WG", 13: "W_AMG",
    15: "BU_FWZ", 16: "BU_LRD", 17: "BU_MWZ", 18: "BU_WRM", 19: "B_SFR", 20: "BU_AMG",
    22: "G_MWZ", 23: "G_KHT", 24: "G_FWZ", 25: "G_WRM", 26: "G_LRD", 27: "G_AMG",
    29: "R_FWZ", 30: "R_MWZ", 31: "TROLL", 32: "R_LRD", 33: "R_WRM", 34: "R_AMG",
    35: "R_AMG", 36: "M_TSK", 37: "M_TRL", 38: "M_APE", 39: "M_CEN2", 40: "M_WG",
    41: "M_FNG", 42: "M_CEN", 43: "M_LRD", 44: "M_KHT", 45: "M_FWZ",
    46: "BK_DJN", 47: "G_DJN", 48: "R_DJN", 49: "BU_DJN",
    50: "DG_BRU", 51: "DG_UWB", 52: "DG_GWR", 53: "DG_RBG", 54: "DG_WUG",
}


def main(exe_path: Path, out_path: Path) -> None:
    data = exe_path.read_bytes()
    if hashlib.sha256(data).hexdigest() != MAGIC_EXE_SHA256:
        sys.exit(f"{exe_path} is not the accepted 1.0 MAGIC.EXE")

    rows = []
    for creature_type in range(COUNT):
        offset = TABLE_START + creature_type * RECORD_SIZE
        name = data[offset : offset + 20].split(b"\0")[0].decode("cp1252")
        color_mask = data[offset + 43]
        deck = struct.unpack_from("<H", data, offset + 44)[0]
        colors = [color for bit, color in COLOR_BITS.items() if color_mask & bit]
        rows.append(
            {
                "type": creature_type,
                "name": name,
                "home_colors": " ".join(colors),
                "deck": deck,
                "sprite": SPRITES.get(creature_type, ""),
            }
        )

    with out_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} creatures to {out_path}")


if __name__ == "__main__":
    website = Path(__file__).resolve().parent.parent
    main(Path(sys.argv[1]), website / "content" / "creatures.csv")
