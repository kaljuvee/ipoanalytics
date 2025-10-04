import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
import os

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from yfinance_util import IPODataFetcher, format_market_cap, format_percentage
from database import IPODatabase
from enhanced_global_loader import load_comprehensive_global_ipo_data
from enhanced_regional_mapping import add_regional_data

REGION = 'EMEA'

st.set_page_config(page_title=f"{REGION} IPO Heatmap", page_icon="🌍", layout="wide")

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'ipo_data' not in st.session_state:
    st.session_state.ipo_data = pd.DataFrame()

@st.cache_resource
def init_components():
    db = IPODatabase()
    fetcher = IPODataFetcher()
    return db, fetcher

db, fetcher = init_components()

st.markdown(f"<div style='font-size:2rem;font-weight:700;margin-bottom:8px'>{REGION} IPO Performance</div>", unsafe_allow_html=True)

# Sidebar - Data refresh
with st.sidebar:
    st.subheader("📊 Data Management")
    current_year = datetime.now().year
    selected_timeframe = "Last 3 years"
    years_to_include = [current_year, current_year - 1, current_year - 2]

    if st.button("🔄 Refresh Global IPO Data", type="primary"):
        with st.spinner("Fetching global IPO data..."):
            try:
                refresh_start = datetime.now().isoformat()
                records_loaded = load_comprehensive_global_ipo_data(max_per_region=100)

                # Also fetch some recent US data for completeness
                all_ipo_records = []
                for year in years_to_include[-2:]:
                    year_records = fetcher.get_nasdaq_nyse_ipos(year=year)
                    if year_records:
                        all_ipo_records.extend(year_records)

                db.log_refresh(
                    refresh_type="GLOBAL_IPO_DATA_REFRESH",
                    status="SUCCESS",
                    records_processed=records_loaded + len(all_ipo_records),
                    started_at=refresh_start
                )

                if all_ipo_records:
                    db.insert_ipo_data(all_ipo_records)
                st.success(f"✅ Loaded global data. Use the main page refresh if needed.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error refreshing data: {str(e)}")

@st.cache_data
def load_ipo_data(years):
    all_data = []
    for year in years:
        year_data = db.get_ipo_data(year=year)
        if not year_data.empty:
            all_data.append(year_data)
    if all_data:
        return pd.concat(all_data, ignore_index=True).drop_duplicates(subset=['ticker'])
    return pd.DataFrame()

df = load_ipo_data(years_to_include)

if not df.empty:
    st.session_state.data_loaded = True
    df = add_regional_data(df)
    df = df[df['region'] == REGION]

    # Filters
    st.markdown('<div style="background:#f8f9fa;padding:16px;border-radius:8px;border:1px solid #e9ecef">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:1.1rem;font-weight:700;color:#1f77b4;margin-bottom:8px">🔍 Filters</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        available_countries = sorted([c for c in df['country'].dropna().unique().tolist() if c != 'Unknown'])
        selected_countries = st.multiselect("🏳️ Countries", options=available_countries, default=available_countries, key="countries_emea")

    with col2:
        country_filtered = df[df['country'].isin(selected_countries)]
        available_exchanges = sorted([e for e in country_filtered['exchange'].dropna().unique().tolist()])
        selected_exchanges = st.multiselect("🏢 Exchanges", options=available_exchanges, default=available_exchanges, key="exchanges_emea")

    with col3:
        available_sectors = sorted([s for s in df['sector'].dropna().unique().tolist()])
        selected_sectors = st.multiselect("🏭 Sectors", options=available_sectors, default=available_sectors, key="sectors_emea")
    st.markdown('</div>', unsafe_allow_html=True)

    filtered_df = df[
        (df['country'].isin(selected_countries)) &
        (df['exchange'].isin(selected_exchanges)) &
        (df['sector'].isin(selected_sectors))
    ]

    if filtered_df.empty:
        st.warning("⚠️ No data matches the selected filters.")
    else:
        # Metrics
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total IPOs", len(filtered_df))
        with c2:
            st.metric("Avg Performance", format_percentage(filtered_df['price_change_since_ipo'].mean()))
        with c3:
            st.metric("Total Market Cap", format_market_cap(filtered_df['market_cap'].sum()))
        with c4:
            best = filtered_df.loc[filtered_df['price_change_since_ipo'].idxmax()] if len(filtered_df) else None
            if best is not None:
                st.metric("Best Performer", f"{best['ticker']} ({format_percentage(best['price_change_since_ipo'])})")

        st.markdown("---")

        # Treemap
        treemap_df = filtered_df.copy()
        treemap_df = treemap_df.dropna(subset=['country', 'sector', 'ticker'])
        treemap_df['hover_text'] = (
            "<b>" + treemap_df['ticker'] + "</b><br>" +
            treemap_df['company_name'] + "<br>" +
            "Country: " + treemap_df['country'] + "<br>" +
            "Exchange: " + treemap_df['exchange'] + "<br>" +
            "Sector: " + treemap_df['sector'] + "<br>" +
            "Market Cap: " + treemap_df['market_cap'].apply(format_market_cap) + "<br>" +
            "Performance: " + treemap_df['price_change_since_ipo'].apply(format_percentage)
        )
        fig = px.treemap(
            treemap_df,
            path=[px.Constant(f"{REGION} IPOs"), 'country', 'sector', 'ticker'],
            values='market_cap',
            color='price_change_since_ipo',
            hover_data={'hover_text': True},
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=0,
            title=f"{REGION} IPO Performance - Last 3 years",
            labels={'price_change_since_ipo': 'Performance Since IPO'}
        )
        fig.update_traces(hovertemplate='%{customdata[0]}<extra></extra>', textinfo="label+value")
        fig.update_layout(height=600, font_size=12, title_font_size=16)
        st.plotly_chart(fig, use_container_width=True)

        # Tables
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("🚀 Top Performers")
            top_performers = filtered_df.nlargest(10, 'price_change_since_ipo')[
                ['ticker', 'company_name', 'country', 'sector', 'price_change_since_ipo', 'market_cap']
            ].copy()
            top_performers['Performance'] = top_performers['price_change_since_ipo'].apply(format_percentage)
            top_performers['Market Cap'] = top_performers['market_cap'].apply(format_market_cap)
            st.dataframe(top_performers[['ticker', 'company_name', 'country', 'sector', 'Performance', 'Market Cap']], use_container_width=True)

        with col_b:
            st.subheader("📉 Worst Performers")
            worst_performers = filtered_df.nsmallest(10, 'price_change_since_ipo')[
                ['ticker', 'company_name', 'country', 'sector', 'price_change_since_ipo', 'market_cap']
            ].copy()
            worst_performers['Performance'] = worst_performers['price_change_since_ipo'].apply(format_percentage)
            worst_performers['Market Cap'] = worst_performers['market_cap'].apply(format_market_cap)
            st.dataframe(worst_performers[['ticker', 'company_name', 'country', 'sector', 'Performance', 'Market Cap']], use_container_width=True)

        st.subheader("📋 Detailed IPO Data")
        display_df = filtered_df.copy()
        display_df['Performance'] = display_df['price_change_since_ipo'].apply(format_percentage)
        display_df['Market Cap'] = display_df['market_cap'].apply(format_market_cap)
        st.dataframe(display_df[['ticker', 'company_name', 'country', 'exchange', 'sector', 'Performance', 'Market Cap']], use_container_width=True)

else:
    st.info("👆 Use the main page to refresh data, then revisit this tab.")


