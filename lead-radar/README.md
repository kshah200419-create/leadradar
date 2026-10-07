# LeadRadar — find local businesses that need you

A freelance lead-finder built on SerpApi's Google Maps engine. Type a
category + city, get a ranked prospect list scored on real outreach signals:
no website, no phone, reputation pain (low rating × many reviews), volume,
and premium price band. Each prospect lands in a pricing tier mapped to a
service offer (PRO ₹14,999 / GROWTH ₹7,999 / NURTURE).

Built as an entry for the **SerpApi India Hackathon 2026** (Commerce & Market
Intelligence track) — and as a working tool for Vadodara outreach.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

1. Create a **free SerpApi account** → copy your API key (250 free search
   credits/month — plenty for development).
2. Export it: `export SERPAPI_KEY="your-key"`.

## CLI

```bash
cd <this-dir>
python3 -m lead_radar.cli --category "cafe" --city "Vadodara, Gujarat" --csv leads.csv
```

No key? Run offline with fixtures:

```bash
python3 -m lead_radar.cli --offline
```

## Web UI

```bash
streamlit run app.py
```

Enter the key in the sidebar, category + city, hit **Find leads**.

## Tests

```bash
python3 -m pytest tests/ -q
```

## How SerpApi is used (meaningful, not decorative)

- **Google Maps engine** (`engine=google_maps`, `type=search`, `gl=in`) is the
  product's only data source: every listing's title, rating, review count,
  price band, address, phone, website, and GPS coordinates comes from a live
  SerpApi response (`serpapi_client.py`).
- The **scoring engine** (`scoring.py`) turns that live search data into a
  decision: who to pitch, at which price. No search data → no score → no
  product.

## Demo script (< 3 min, must be recorded live with a real API key)

0:00 — "LeadRadar finds local businesses that need you, powered by SerpApi."
0:15 — Type `cafe` + `Vadodara, Gujarat`, hit Find leads.
0:45 — Walk the ranked list: Spice Route (no website, 3.8★ × 412 reviews →
       PRO ₹14,999 pitch), vs a cafe with a site (NURTURE).
1:30 — Export CSV; open it — the outreach sheet is ready.
2:15 — Code tour: `serpapi_client.py` (Maps engine call), `scoring.py`
       (the signals), `cli.py` (CSV export).
2:45 — Close: "Every prospect list in this challenge's outreach packs took
       hours by hand. LeadRadar makes it in seconds."

## Judging-criteria fit

- **Idea strength** — freelancers/agencies everywhere buy lead lists; this one
  scores itself from live Maps data.
- **Originality** — the scoring signals (reputation pain × missing web
  presence → price tier) are purpose-built for outreach, not a generic search
  demo.
- **Technical complexity** — real API integration, normalization layer,
  scoring engine, CLI + web UI, offline fixture mode, tested.
- **Usefulness** — dogfoods the freelance playbook: this tool can regenerate
  our own lead lists in seconds.
- **Meaningful SerpApi usage** — the product cannot function without live
  search data; see above.

## Files

| File | What |
|---|---|
| `lead_radar/serpapi_client.py` | SerpApi Maps engine wrapper + result normalization |
| `lead_radar/scoring.py` | Opportunity scoring → PRO/GROWTH/NURTURE tiers |
| `lead_radar/cli.py` | CLI: search → rank → table + CSV |
| `lead_radar/fixtures.py` | Offline fixture payload (dev/tests only) |
| `app.py` | Streamlit UI |
| `tests/test_scoring.py` | Offline scoring tests |
