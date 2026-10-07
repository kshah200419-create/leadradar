"""Offline fixtures: real-shaped SerpApi Google Maps responses for dev/tests.

These stand in for live API results when no API key is available.
Fixtures are never submitted as demo footage; the demo must run live.
"""
from __future__ import annotations

FIXTURE_PAYLOAD = {
    "local_results": {
        "places": [
            {
                "title": "Spice Route Fine Dine",
                "type": "North Indian restaurant",
                "rating": 3.8,
                "reviews": 412,
                "price": "$$$",
                "address": "Alkapuri, Vadodara, Gujarat",
                "phone": "",
                "website": "",
                "gps_coordinates": {"latitude": 22.31, "longitude": 73.18},
            },
            {
                "title": "Cafe Brew Junction",
                "type": "Cafe",
                "rating": 4.4,
                "reviews": 231,
                "price": "$$",
                "address": "Fatehgunj, Vadodara, Gujarat",
                "phone": "+91 98765 43210",
                "website": "https://cafebrewjunction.example.in",
                "gps_coordinates": {"latitude": 22.32, "longitude": 73.19},
            },
            {
                "title": "Gokul Sweets & Snacks",
                "type": "Sweet shop",
                "rating": 4.1,
                "reviews": 96,
                "price": "$",
                "address": "Manjalpur, Vadodara, Gujarat",
                "phone": "+91 90123 45678",
                "website": "",
                "gps_coordinates": {"latitude": 22.29, "longitude": 73.20},
            },
            {
                "title": "The Urban Thali House",
                "type": "Gujarati restaurant",
                "rating": 4.7,
                "reviews": 1204,
                "price": "$$",
                "address": "Sayajigunj, Vadodara, Gujarat",
                "phone": "+91 91234 56789",
                "website": "https://urbanthali.example.in",
                "gps_coordinates": {"latitude": 22.31, "longitude": 73.18},
            },
        ]
    }
}
