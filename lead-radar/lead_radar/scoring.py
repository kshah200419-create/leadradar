"""Lead scoring: turns raw Maps listings into outreach-ready prospects.

Signals of "this business would buy a website/chatbot/setup service":
  - no website listed            -> +35 (they lack even a web presence)
  - no phone listed              -> +15 (hard to reach = automation upside)
  - low rating (< 4.0) with 50+ reviews -> +20 (reputation pain)
  - high review count (100+)     -> +10 (volume = real business, budget)
  - fine-dine price band ($$$)   -> +10 (pay-ability proxy)

Tier mapping (matches our Vadodara outreach pricing):
  score >= 70 -> PRO   (₹14,999 chatbot setup)
  score >= 40 -> GROWTH (₹7,999)
  else        -> NURTURE (content/drip, revisit later)
"""
from __future__ import annotations

LOW_RATING_THRESHOLD = 4.0
HIGH_REVIEW_COUNT = 100
REPUTATION_REVIEW_FLOOR = 50


def score_place(place: dict) -> dict:
    score = 0
    reasons: list[str] = []

    if not (place.get("website") or "").strip():
        score += 35
        reasons.append("no website")
    if not (place.get("phone") or "").strip():
        score += 15
        reasons.append("no phone listed")
    rating = place.get("rating")
    reviews = place.get("reviews") or 0
    if rating is not None and rating < LOW_RATING_THRESHOLD and reviews >= REPUTATION_REVIEW_FLOOR:
        score += 20
        reasons.append(f"rating {rating} with {reviews} reviews")
    if reviews >= HIGH_REVIEW_COUNT:
        score += 10
        reasons.append(f"{reviews} reviews")
    if (place.get("price") or "").count("$") >= 3:
        score += 10
        reasons.append("premium price band")

    tier = "PRO" if score >= 70 else ("GROWTH" if score >= 40 else "NURTURE")
    return {
        **place,
        "lead_score": score,
        "tier": tier,
        "why": "; ".join(reasons) or "established presence",
    }


def rank_places(places: list[dict]) -> list[dict]:
    scored = [score_place(p) for p in places]
    scored.sort(key=lambda p: (-p["lead_score"], -int(p.get("reviews") or 0)))
    return scored
