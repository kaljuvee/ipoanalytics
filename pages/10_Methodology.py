import streamlit as st
import pandas as pd

st.set_page_config(page_title="Methodology & Overview", page_icon="🧭", layout="wide")

st.title("🧭 IPO Map Methodology & App Overview")

st.markdown("""
This page summarizes the methodology, data coverage, and current status of the IPO Map application. It consolidates information previously documented in markdown files (e.g., README, complete records report, country list status, and testing summaries) directly into the app.
""")

st.markdown("---")

st.header("What this app does")
st.markdown("""
The app visualizes global IPO performance using an interactive treemap (Global → Region → Country → Sector → Ticker) with cascading filters for regions, countries, exchanges, and sectors. It provides:

- Interactive market heatmap with performance coloring and size by market cap
- Global regional filtering (APAC, EMEA, Americas) and drill-downs
- AI-powered commentary (with statistical fallback)
- News integration (Tavily/Exa.ai) with graceful fallback samples
- Key metrics: total IPOs, average performance, total market cap, best performer
""")

st.subheader("Global coverage (summary)")
st.markdown("""
- 50+ countries across 70+ exchanges supported in the data layer
- Regions: APAC, EMEA, Americas
- Exchange mapping with country/regional classification
- Data stored locally in SQLite with refresh logging and caching
""")

st.markdown("---")

st.header("Data coverage snapshot")
st.markdown("From the latest consolidated report:")

col1, col2 = st.columns(2)
with col1:
    st.metric("Total IPO records (snapshot)", "51")
    st.write("Regional distribution:")
    st.write("- APAC: 26 (51.0%)")
    st.write("- Americas: 18 (35.3%)")
    st.write("- EMEA: 7 (13.7%)")

with col2:
    st.write("Representative exchanges:")
    st.write("NASDAQ (US), HKEX (HK), TSE (JP), ASX (AU), NSE (IN), SGX (SG), KRX (KR), B3 (BR), TSX (CA), BMV (MX), LSE (UK), AMS (NL), WSE (PL)")

st.markdown("""
Performance highlights (illustrative):
- Top performers include LPP SA (Poland), GFNORTEO (Mexico), SHOP (Canada)
- Average performance varies by region with EMEA leading in the snapshot
""")

st.markdown("---")

st.header("Methodology")
st.markdown("""
1) Data sourcing
- Primary market data from Yahoo Finance via `yfinance`
- IPO lists curated for recent periods; global expansion ongoing
- Market cap and performance computed from current price vs first listing price

2) Processing & storage
- Normalized records stored in SQLite (`data/ipo_analytics.db`)
- Regional/country enrichment via exchange-to-country mapping
- Refresh operations logged; caching used to speed reads

3) Visualization
- Plotly treemap hierarchy: Global → Region → Country → Sector → Ticker
- Size by market cap; color by performance since IPO
- Rich hover text: ticker, company, region, country, exchange, sector, performance, market cap

4) UX & analysis
- Filters in the main pane for discoverability
- AI commentary uses OpenAI if configured; otherwise statistical fallback
- News uses Tavily/Exa.ai if keys configured; otherwise sample headlines
""")

st.markdown("---")

st.header("Country list status")
st.markdown("""
The country summary section presents cards with flags, IPO counts, average performance, total market cap, and exchange listings in a three-column layout. If not visible, scroll further down or first click "Refresh IPO Data" in the sidebar to load data.
""")

st.markdown("---")

st.header("Known limitations and next steps")
st.markdown("""
- IPO discovery currently relies on curated lists
- Data quality varies by ticker/market availability on Yahoo Finance
- Filter cascade logic may need refinement for full population across regions
- Expansion of European IPO data is planned
""")

st.markdown("---")

st.header("How to use")
st.markdown("""
1. Click "🔄 Refresh IPO Data" in the sidebar to populate the database
2. Use filters in the main pane to explore regions, countries, exchanges, and sectors
3. Explore the treemap, metrics, AI commentary, news, and detailed tables
""")

st.info("This methodology page consolidates the contents of prior markdown documentation directly into the app.")


