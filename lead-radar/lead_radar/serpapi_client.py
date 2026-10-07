"""Thin client for SerpApi's Google Maps engine.

Uses raw HTTPS (no extra SDK dependency). Every call that touches the
network carries the user's SerpApi API key; offline mode falls back to
fixtures so the app is developable and testable without a key.
"""
from __future__ import annotations

import requests

BASE_URL = "https://serpapi.com/search.json"


class SerpApiError(RuntimeError):
    pass


class SerpApiClient:
    def __init__(self, api_key: str, timeout: int = 30) -> None:
        if not api_key:
            raise ValueError("SerpApi API key is required")
        self.api_key = api_key
        self.timeout = timeout

    def search_places(self, query: str, location: str = "", num: int = 20) -> dict:
        """Google Maps engine, type=search. Returns raw SerpApi JSON."""
        params = {
            "engine": "google_maps",
            "q": query,
            "type": "search",
            "api_key": self.api_key,
            "hl": "en",
            "gl": "in",
        }
        if location:
            params["location"] = location
        try:
            resp = requests.get(BASE_URL, params=params, timeout=self.timeout)
        except requests.RequestException as exc:
            raise SerpApiError(f"network error calling SerpApi: {exc}") from exc
        if resp.status_code != 200:
            raise SerpApiError(f"SerpApi HTTP {resp.status_code}: {resp.text[:200]}")
        data = resp.json()
        if "error" in data:
            raise SerpApiError(f"SerpApi error: {data['error']}")
        return data

    @staticmethod
    def extract_places(payload: dict) -> list[dict]:
        """Normalize local_results into flat dicts.

        The live Google Maps API returns local_results as a LIST of place
        dicts; older fixtures use local_results.places. Handle both.
        """
        lr = payload.get("local_results") or []
        if isinstance(lr, dict):
            lr = lr.get("places") or []
        places = lr if isinstance(lr, list) else []
        out = []
        for p in places:
            out.append(
                {
                    "name": p.get("title", ""),
                    "type": p.get("type", ""),
                    "rating": p.get("rating"),
                    "reviews": p.get("reviews", 0) or 0,
                    "price": p.get("price", ""),
                    "address": p.get("address", ""),
                    "phone": p.get("phone", ""),
                    "website": p.get("website", ""),
                    "gps": p.get("gps_coordinates") or {},
                }
            )
        return out
