"""CLI: search -> score -> ranked CSV + terminal table."""
from __future__ import annotations

import argparse
import csv
import os
import sys

from lead_radar.fixtures import FIXTURE_PAYLOAD
from lead_radar.scoring import rank_places
from lead_radar.serpapi_client import SerpApiClient

TIER_PRICE = {"PRO": "₹14,999", "GROWTH": "₹7,999", "NURTURE": "—"}
COLUMNS = ["name", "type", "rating", "reviews", "price", "address", "phone", "website", "lead_score", "tier", "why"]


def run(category: str, city: str, api_key: str | None, offline: bool) -> list[dict]:
    if offline or not api_key:
        places = SerpApiClient.extract_places(FIXTURE_PAYLOAD)
    else:
        client = SerpApiClient(api_key)
        payload = client.search_places(f"{category} in {city}")
        places = SerpApiClient.extract_places(payload)
    return rank_places(places)


def print_table(ranked: list[dict]) -> None:
    print(f"\n{'TIER':7} {'SCORE':5}  NAME (why)")
    print("-" * 72)
    for p in ranked:
        rating = p.get("rating") or "—"
        print(f"{p['tier']:7} {p['lead_score']:>5}  {p['name']} — ★{rating} · {p['reviews']} reviews")
        print(f"{'':13}{p['why']}  |  pitch: {TIER_PRICE[p['tier']]}")
    print(f"\n{len(ranked)} prospects ranked.\n")


def write_csv(ranked: list[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(ranked)
    print(f"CSV written: {path}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="LeadRadar — find local businesses that need you")
    ap.add_argument("--category", default="cafe", help="business category to search")
    ap.add_argument("--city", default="Vadodara, Gujarat", help="city/region to search")
    ap.add_argument("--api-key", default=os.environ.get("SERPAPI_KEY", ""), help="SerpApi API key")
    ap.add_argument("--offline", action="store_true", help="use offline fixtures instead of the live API")
    ap.add_argument("--csv", default="", help="write ranked prospects to this CSV path")
    args = ap.parse_args(argv)

    if not args.offline and not args.api_key:
        print("No API key: running in OFFLINE fixture mode. Set SERPAPI_KEY for live data.", file=sys.stderr)
        args.offline = True

    try:
        ranked = run(args.category, args.city, args.api_key, args.offline)
    except Exception as exc:  # noqa: BLE001 — surface honestly
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print_table(ranked)
    if args.csv:
        write_csv(ranked, args.csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
