#!/usr/bin/env python3
"""Uniform Guanyin lot draw, jiaobei emulator, and lot lookup."""

from __future__ import annotations

import argparse
import json
import secrets
from pathlib import Path


DATA = Path(__file__).resolve().parent.parent / "references" / "lots.json"


def draw_lot() -> int:
    """Return an unbiased integer from 1 through 100."""
    return secrets.randbelow(100) + 1


def toss_cup() -> dict[str, object]:
    """Emulate two fair binary blocks: holy 1/2, laugh 1/4, yin 1/4."""
    bits = secrets.randbits(2)
    if bits in (1, 2):
        return {"result": "圣筊", "faces": "一平一凸", "probability": "1/2"}
    if bits == 0:
        return {"result": "笑筊", "faces": "两面皆平", "probability": "1/4"}
    return {"result": "阴筊", "faces": "两面皆凸", "probability": "1/4"}


def load_lot(number: int) -> dict[str, object]:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    return payload["lots"][number - 1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("draw", help="draw one uniform lot from 1 to 100")
    sub.add_parser("cup", help="emulate one pair of fair jiaobei")
    lookup = sub.add_parser("lookup", help="print one lot from the reference data")
    lookup.add_argument("number", type=int, choices=range(1, 101))
    args = parser.parse_args()

    if args.command == "draw":
        print(json.dumps({"lot": draw_lot(), "probability": "1/100"}, ensure_ascii=False))
    elif args.command == "cup":
        print(json.dumps(toss_cup(), ensure_ascii=False))
    else:
        print(json.dumps(load_lot(args.number), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

