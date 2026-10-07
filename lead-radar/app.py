"""Optional Streamlit UI. Requires `pip install streamlit`."""
from __future__ import annotations

try:
    import streamlit as st
except ImportError:  # graceful when streamlit isn't installed
    raise SystemExit("Streamlit not installed. Run: pip install -r requirements.txt")

from lead_radar.fixtures import FIXTURE_PAYLOAD
from lead_radar.scoring import rank_places
from lead_radar.serpapi_client import SerpApiClient

st.set_page_config(page_title="LeadRadar", page_icon="🎯")
st.title("🎯 LeadRadar")
st.caption("Find local businesses that would buy a website, chatbot, or review-repair service.")

api_key = st.sidebar.text_input("SerpApi API key", type="password")
category = st.text_input("Business category", "cafe")
city = st.text_input("City / region", "Vadodara, Gujarat")
offline = st.sidebar.checkbox("Offline fixture mode", value=not bool(api_key))

if st.button("Find leads"):
    with st.spinner("Searching…"):
        if offline:
            places = SerpApiClient.extract_places(FIXTURE_PAYLOAD)
        else:
            client = SerpApiClient(api_key)
            payload = client.search_places(f"{category} in {city}")
            places = SerpApiClient.extract_places(payload)
    ranked = rank_places(places)
    st.success(f"{len(ranked)} prospects, ranked by opportunity score.")
    for p in ranked:
        with st.expander(f"{p['tier']} · {p['lead_score']} — {p['name']}"):
            st.write(f"★ {p.get('rating') or '—'} · {p['reviews']} reviews · {p['price']} · {p['type']}")
            st.write(p["address"])
            st.write(f"📞 {p['phone'] or 'not listed'} · 🌐 {p['website'] or 'no website'}")
            st.write(f"**Why:** {p['why']}")
