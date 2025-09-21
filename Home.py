import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from yfinance_util import IPODataFetcher, format_market_cap, format_percentage
from database import IPODatabase

# Page configuration
st.set_page_config(
    page_title="IPO Analytics - Market Heatmap",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'ipo_data' not in st.session_state:
    st.session_state.ipo_data = pd.DataFrame()

# Initialize database and data fetcher
@st.cache_resource
def init_components():
    db = IPODatabase()
    fetcher = IPODataFetcher()
    return db, fetcher

db, fetcher = init_components()

# Sidebar
st.sidebar.markdown('<div class="sidebar-header">IPO Analytics Control Panel</div>', unsafe_allow_html=True)

# Data refresh section
st.sidebar.subheader("📊 Data Management")

current_year = datetime.now().year
selected_year = st.sidebar.selectbox(
    "Select Year",
    options=[current_year, current_year - 1, current_year - 2],
    index=0
)

# Data refresh button
if st.sidebar.button("🔄 Refresh IPO Data", type="primary"):
    with st.spinner("Fetching IPO data from Yahoo Finance..."):
        try:
            # Log refresh start
            refresh_start = datetime.now().isoformat()
            
            # Fetch IPO data
            ipo_records = fetcher.get_nasdaq_nyse_ipos(year=selected_year)
            
            if ipo_records:
                # Insert into database
                records_inserted = db.insert_ipo_data(ipo_records)
                
                # Log successful refresh
                db.log_refresh(
                    refresh_type="IPO_DATA_REFRESH",
                    status="SUCCESS",
                    records_processed=records_inserted,
                    started_at=refresh_start
                )
                
                st.sidebar.success(f"✅ Successfully refreshed {records_inserted} IPO records!")
                st.session_state.data_loaded = True
                
                # Force rerun to update the display
                st.rerun()
                
            else:
                st.sidebar.warning("⚠️ No IPO data found for the selected year.")
                db.log_refresh(
                    refresh_type="IPO_DATA_REFRESH",
                    status="NO_DATA",
                    records_processed=0,
                    started_at=refresh_start
                )
                
        except Exception as e:
            error_msg = str(e)
            st.sidebar.error(f"❌ Error refreshing data: {error_msg}")
            db.log_refresh(
                refresh_type="IPO_DATA_REFRESH",
                status="ERROR",
                records_processed=0,
                error_message=error_msg,
                started_at=refresh_start
            )

# Filters section
st.sidebar.subheader("🔍 Filters")

# Load data from database
@st.cache_data
def load_ipo_data(year):
    return db.get_ipo_data(year=year)

df = load_ipo_data(selected_year)

if not df.empty:
    st.session_state.data_loaded = True
    st.session_state.ipo_data = df
    
    # Exchange filter
    available_exchanges = df['exchange'].unique().tolist()
    selected_exchanges = st.sidebar.multiselect(
        "Select Exchanges",
        options=available_exchanges,
        default=available_exchanges
    )
    
    # Sector filter
    available_sectors = df['sector'].unique().tolist()
    selected_sectors = st.sidebar.multiselect(
        "Select Sectors",
        options=available_sectors,
        default=available_sectors
    )
    
    # Market cap filter
    min_market_cap = st.sidebar.number_input(
        "Minimum Market Cap (Millions)",
        min_value=0,
        max_value=int(df['market_cap'].max() / 1e6) if not df.empty else 1000,
        value=0,
        step=100
    )
    
    # Apply filters
    filtered_df = df[
        (df['exchange'].isin(selected_exchanges)) &
        (df['sector'].isin(selected_sectors)) &
        (df['market_cap'] >= min_market_cap * 1e6)
    ]
    
else:
    filtered_df = pd.DataFrame()

# Database stats
last_refresh = db.get_last_refresh()
if last_refresh:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Database Stats")
    st.sidebar.write(f"**Last Refresh:** {last_refresh['completed_at'][:19]}")
    st.sidebar.write(f"**Status:** {last_refresh['status']}")
    st.sidebar.write(f"**Records:** {last_refresh['records_processed']}")

# Main content
st.markdown('<div class="main-header">IPO Analytics - Market Heatmap</div>', unsafe_allow_html=True)

# Check if data is available
if not st.session_state.data_loaded or filtered_df.empty:
    st.info("👆 Please click 'Refresh IPO Data' in the sidebar to load IPO data for visualization.")
    
    # Show sample data structure
    st.subheader("📋 Expected Data Structure")
    sample_data = {
        'ticker': ['RDDT', 'SMCI', 'ARM'],
        'company_name': ['Reddit Inc.', 'Super Micro Computer', 'ARM Holdings'],
        'sector': ['Technology', 'Technology', 'Technology'],
        'exchange': ['NYSE', 'NASDAQ', 'NASDAQ'],
        'market_cap': [8500000000, 45000000000, 120000000000],
        'price_change_since_ipo': [0.15, -0.25, 0.08]
    }
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df, use_container_width=True)
    
else:
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{len(filtered_df)}</h3>
            <p>Total IPOs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_performance = filtered_df['price_change_since_ipo'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{format_percentage(avg_performance)}</h3>
            <p>Avg Performance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_market_cap = filtered_df['market_cap'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{format_market_cap(total_market_cap)}</h3>
            <p>Total Market Cap</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        best_performer = filtered_df.loc[filtered_df['price_change_since_ipo'].idxmax()]
        st.markdown(f"""
        <div class="metric-card">
            <h3>{best_performer['ticker']}</h3>
            <p>Best Performer ({format_percentage(best_performer['price_change_since_ipo'])})</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create treemap visualization
    st.subheader(f"🗺️ IPO Market Heatmap - {selected_year}")
    
    if len(filtered_df) > 0:
        # Prepare data for treemap
        treemap_df = filtered_df.copy()
        
        # Format IPO date for display
        treemap_df['ipo_date_formatted'] = pd.to_datetime(treemap_df['ipo_date']).dt.strftime('%Y-%m-%d')
        
        # Create hover text
        treemap_df['hover_text'] = treemap_df.apply(lambda row: 
            f"<b>{row['ticker']}</b><br>" +
            f"{row['company_name']}<br>" +
            f"Sector: {row['sector']}<br>" +
            f"Exchange: {row['exchange']}<br>" +
            f"IPO Date (First Listing): {row['ipo_date_formatted']}<br>" +
            f"Market Cap: {format_market_cap(row['market_cap'])}<br>" +
            f"Performance: {format_percentage(row['price_change_since_ipo'])}", 
            axis=1
        )
        
        # Create treemap
        fig = px.treemap(
            treemap_df,
            path=[px.Constant("All IPOs"), "sector", "ticker"],
            values="market_cap",
            color="price_change_since_ipo",
            hover_data={
                'market_cap': ':,.0f',
                'price_change_since_ipo': ':.2%',
                'company_name': True,
                'ipo_date_formatted': True
            },
            color_continuous_scale="RdYlGn",
            color_continuous_midpoint=0,
            title=f"IPO Performance Heatmap - {selected_year}"
        )
        
        # Update layout
        fig.update_layout(
            height=800,
            font_size=12,
            title_font_size=20,
            coloraxis_colorbar=dict(
                title="Performance Since IPO",
                tickformat=".1%"
            )
        )
        
        # Update traces for better hover info
        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>" +
                         "Market Cap: $%{value:,.0f}<br>" +
                         "Performance: %{color:.2%}<br>" +
                         "IPO Date (First Listing): %{customdata[3]}<br>" +
                         "<extra></extra>",
            customdata=treemap_df[['market_cap', 'price_change_since_ipo', 'company_name', 'ipo_date_formatted']].values
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Performance Distribution")
            
            # Create histogram
            hist_fig = px.histogram(
                filtered_df,
                x="price_change_since_ipo",
                nbins=20,
                title="Distribution of IPO Performance",
                labels={"price_change_since_ipo": "Performance Since IPO", "count": "Number of IPOs"}
            )
            hist_fig.update_layout(height=400)
            hist_fig.update_xaxes(tickformat=".1%")
            st.plotly_chart(hist_fig, use_container_width=True)
        
        with col2:
            st.subheader("🏢 Sector Performance")
            
            # Sector performance
            sector_perf = filtered_df.groupby('sector').agg({
                'price_change_since_ipo': 'mean',
                'market_cap': 'sum',
                'ticker': 'count'
            }).round(4)
            sector_perf.columns = ['Avg Performance', 'Total Market Cap', 'Count']
            sector_perf = sector_perf.sort_values('Avg Performance', ascending=False)
            
            # Create bar chart
            bar_fig = px.bar(
                x=sector_perf.index,
                y=sector_perf['Avg Performance'],
                title="Average Performance by Sector",
                labels={"x": "Sector", "y": "Average Performance"}
            )
            bar_fig.update_layout(height=400)
            bar_fig.update_yaxes(tickformat=".1%")
            st.plotly_chart(bar_fig, use_container_width=True)
        
        # Top and worst performers
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚀 Top Performers")
            top_performers = filtered_df.nlargest(5, 'price_change_since_ipo')[
                ['ticker', 'company_name', 'sector', 'price_change_since_ipo', 'market_cap']
            ].copy()
            top_performers['Performance'] = top_performers['price_change_since_ipo'].apply(format_percentage)
            top_performers['Market Cap'] = top_performers['market_cap'].apply(format_market_cap)
            st.dataframe(
                top_performers[['ticker', 'company_name', 'sector', 'Performance', 'Market Cap']],
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.subheader("📉 Worst Performers")
            worst_performers = filtered_df.nsmallest(5, 'price_change_since_ipo')[
                ['ticker', 'company_name', 'sector', 'price_change_since_ipo', 'market_cap']
            ].copy()
            worst_performers['Performance'] = worst_performers['price_change_since_ipo'].apply(format_percentage)
            worst_performers['Market Cap'] = worst_performers['market_cap'].apply(format_market_cap)
            st.dataframe(
                worst_performers[['ticker', 'company_name', 'sector', 'Performance', 'Market Cap']],
                use_container_width=True,
                hide_index=True
            )
        
        # Detailed data table
        st.markdown("---")
        st.subheader("📋 Detailed IPO Data")
        
        # Prepare display dataframe
        display_df = filtered_df.copy()
        display_df['Performance'] = display_df['price_change_since_ipo'].apply(format_percentage)
        display_df['Market Cap'] = display_df['market_cap'].apply(format_market_cap)
        display_df['IPO Date'] = pd.to_datetime(display_df['ipo_date']).dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_df[['ticker', 'company_name', 'sector', 'exchange', 'IPO Date', 'Performance', 'Market Cap']],
            use_container_width=True,
            hide_index=True
        )
        
    else:
        st.warning("No IPO data matches the current filters. Please adjust your filter criteria.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>IPO Analytics Dashboard | Data sourced from Yahoo Finance | 
    <a href="https://finance.yahoo.com" target="_blank">Yahoo Finance</a></p>
</div>
""", unsafe_allow_html=True)
