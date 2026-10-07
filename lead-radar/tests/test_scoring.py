"""Offline tests for the scoring engine (no API key needed)."""
from __future__ import annotations

from lead_radar.fixtures import FIXTURE_PAYLOAD
from lead_radar.scoring import rank_places, score_place
from lead_radar.serpapi_client import SerpApiClient


def test_extract_places():
    places = SerpApiClient.extract_places(FIXTURE_PAYLOAD)
    assert len(places) == 4
    assert places[0]["name"] == "Spice Route Fine Dine"


def test_no_website_scores_high():
    scored = score_place({"name": "X", "rating": None, "reviews": 10, "price": "$", "phone": "", "website": ""})
    assert scored["lead_score"] == 35 + 15  # no website + no phone
    assert "no website" in scored["why"]


def test_premium_low_rated_big_reviews_is_pro():
    scored = score_place(
        {"name": "Y", "rating": 3.5, "reviews": 412, "price": "$$$", "phone": "", "website": ""}
    )
    assert scored["lead_score"] >= 70
    assert scored["tier"] == "PRO"


def test_established_web_presence_is_nurture():
    scored = score_place(
        {"name": "Z", "rating": 4.7, "reviews": 1204, "price": "$$",
         "phone": "+91 91234 56789", "website": "https://z.example.in"}
    )
    assert scored["tier"] == "NURTURE"


def test_ranking_orders_by_score():
    ranked = rank_places(SerpApiClient.extract_places(FIXTURE_PAYLOAD))
    assert ranked[0]["tier"] == "PRO"
    scores = [p["lead_score"] for p in ranked]
    assert scores == sorted(scores, reverse=True)
