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
from enhanced_global_loader import load_comprehensive_global_ipo_data
from ai_commentary import get_ipo_commentary
from ipo_news import get_ipo_news
from enhanced_regional_mapping import (
    add_regional_data, get_region_display_name, 
    get_countries_by_region, get_exchanges_by_region
)

# Page configuration
st.set_page_config(
    page_title="IPO Map - Market Heatmap",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .filter-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        border: 1px solid #e9ecef;
    }
    .filter-header {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
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

# Main header
st.markdown('<div class="main-header">IPO Map - Global Market Heatmap</div>', unsafe_allow_html=True)

# Sidebar for data refresh only
with st.sidebar:
    st.subheader("📊 Data Management")
    
    current_year = datetime.now().year
    selected_timeframe = st.selectbox(
        "Select Timeframe",
        options=["Last 3 years", "Last 5 years"],
        index=0
    )

    # Calculate years based on timeframe
    if selected_timeframe == "Last 3 years":
        years_to_include = [current_year, current_year - 1, current_year - 2]
    else:  # Last 5 years
        years_to_include = [current_year, current_year - 1, current_year - 2, current_year - 3, current_year - 4]

    # Data refresh button
    if st.button("🔄 Refresh IPO Data", type="primary"):
        with st.spinner("Fetching global IPO data from market sources..."):
            try:
                # Log refresh start
                refresh_start = datetime.now().isoformat()
                
                # Load comprehensive global IPO data from all regions
                records_loaded = load_comprehensive_global_ipo_data(max_per_region=100)
                
                # Also fetch some real US data for recent years
                all_ipo_records = []
                for year in years_to_include[-2:]:  # Last 2 years only for real data
                    year_records = fetcher.get_nasdaq_nyse_ipos(year=year)
                    if year_records:
                        all_ipo_records.extend(year_records)
                
                ipo_records = all_ipo_records
                
                # Log successful refresh for global data
                db.log_refresh(
                    refresh_type="GLOBAL_IPO_DATA_REFRESH",
                    status="SUCCESS",
                    records_processed=records_loaded,
                    started_at=refresh_start
                )
                
                if ipo_records:
                    # Insert additional real US data
                    records_inserted = db.insert_ipo_data(ipo_records)
                    st.success(f"✅ Successfully loaded {records_loaded} global IPO records + {records_inserted} recent US IPOs!")
                else:
                    st.success(f"✅ Successfully loaded {records_loaded} global IPO records!")
                
                st.session_state.data_loaded = True
                
                # Force rerun to update the display
                st.rerun()
                    
            except Exception as e:
                error_msg = str(e)
                st.error(f"❌ Error refreshing data: {error_msg}")
                db.log_refresh(
                    refresh_type="GLOBAL_IPO_DATA_REFRESH",
                    status="ERROR",
                    records_processed=0,
                    error_message=error_msg,
                    started_at=refresh_start
                )

    # Database stats
    last_refresh = db.get_last_refresh()
    if last_refresh:
        st.markdown("---")
        st.subheader("📈 Database Stats")
        st.write(f"**Last Refresh:** {last_refresh['completed_at'][:19]}")
        st.write(f"**Status:** {last_refresh['status']}")
        st.write(f"**Records:** {last_refresh['records_processed']}")

# Load data from database
def load_ipo_data(years):
    all_data = []
    for year in years:
        year_data = db.get_ipo_data(year=year)
        if not year_data.empty:
            all_data.append(year_data)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True).drop_duplicates(subset=['ticker'])
        # Apply regional mapping to all data
        combined_df = add_regional_data(combined_df)
        return combined_df
    else:
        return pd.DataFrame()

df = load_ipo_data(years_to_include)

# Main content area
if not df.empty:
    st.session_state.data_loaded = True
    st.session_state.ipo_data = df
    
    # Filters section in main pane
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="filter-header">🔍 Global Market Filters</div>', unsafe_allow_html=True)
    
    # Create filter columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Regional filter (primary filter)
        # Ensure we have all regions from the database, not just filtered data
        all_regions = ['APAC', 'EMEA', 'Americas', 'Other']  # Define expected regions
        available_regions = []
        
        # Check which regions actually have data
        for region in all_regions:
            if region in df['region'].values:
                available_regions.append(region)
        
        # If no regions found, fall back to unique values from df
        if not available_regions:
            available_regions = sorted([r for r in df['region'].unique().tolist() if r is not None])
            if 'Other' in available_regions:
                available_regions.remove('Other')
                available_regions.append('Other')  # Move 'Other' to end
        
        # Create display names for regions
        region_options = [get_region_display_name(region) for region in available_regions]
        region_mapping = dict(zip(region_options, available_regions))
        
        selected_region_displays = st.multiselect(
            "🌍 Select Regions",
            options=region_options,
            default=region_options,  # Select all by default
            key="region_filter"
        )
        
        selected_regions = [region_mapping[display] for display in selected_region_displays]
    
    with col2:
        # Filter by selected regions first
        if selected_regions:
            region_filtered_df = df[df['region'].isin(selected_regions)]
        else:
            region_filtered_df = df  # Show all if no regions selected
        
        # Country filter (within selected regions)
        available_countries = [c for c in region_filtered_df['country'].unique().tolist() if c is not None and c != 'Unknown']
        available_countries = sorted(available_countries) if available_countries else []
        
        # Smart default selection - limit to top 10 countries to avoid overwhelming UI
        default_countries = available_countries[:10] if len(available_countries) > 10 else available_countries
        
        selected_countries = st.multiselect(
            "🏳️ Select Countries",
            options=available_countries,
            default=default_countries,
            key="country_filter",
            help=f"Showing countries from selected regions. {len(available_countries)} countries available."
        )
    
    with col3:
        # Exchange filter (within selected countries)
        if selected_countries:
            country_filtered_df = region_filtered_df[region_filtered_df['country'].isin(selected_countries)]
        else:
            country_filtered_df = region_filtered_df
            
        available_exchanges = [e for e in country_filtered_df['exchange'].unique().tolist() if e is not None]
        available_exchanges = sorted(available_exchanges) if available_exchanges else []
        
        # Smart default selection for exchanges
        default_exchanges = available_exchanges[:15] if len(available_exchanges) > 15 else available_exchanges
        
        selected_exchanges = st.multiselect(
            "🏢 Select Exchanges",
            options=available_exchanges,
            default=default_exchanges,
            key="exchange_filter",
            help=f"Showing exchanges from selected countries. {len(available_exchanges)} exchanges available."
        )
    
    with col4:
        # Sector filter - use all data for sectors as they span across regions
        available_sectors = [s for s in df['sector'].unique().tolist() if s is not None]
        available_sectors = sorted(available_sectors) if available_sectors else []
        
        # Default to all sectors for comprehensive view
        selected_sectors = st.multiselect(
            "🏭 Select Sectors",
            options=available_sectors,
            default=available_sectors,
            key="sector_filter",
            help=f"All sectors across selected regions. {len(available_sectors)} sectors available."
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply all filters
    filtered_df = df[
        (df['region'].isin(selected_regions)) &
        (df['country'].isin(selected_countries)) &
        (df['exchange'].isin(selected_exchanges)) &
        (df['sector'].isin(selected_sectors))
    ]
    
    # Check if filtered data is available
    if filtered_df.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your filter criteria.")
        st.info("💡 Try selecting more regions, countries, or sectors to see data.")
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
        st.subheader(f"📊 IPO Performance Treemap - {selected_timeframe}")
        
        if len(filtered_df) > 0:
            # Prepare data for treemap with enhanced hierarchy
            treemap_df = filtered_df.copy()
            
            # Create hierarchical path: Global IPOs -> Region -> Country -> Sector -> Ticker
            treemap_df['path'] = (
                "Global IPOs" + " / " +
                treemap_df['region'].astype(str) + " / " +
                treemap_df['country'].astype(str) + " / " +
                treemap_df['sector'].astype(str) + " / " +
                treemap_df['ticker'].astype(str)
            )
            
            # Format hover data
            treemap_df['hover_text'] = (
                "<b>" + treemap_df['ticker'] + "</b><br>" +
                treemap_df['company_name'] + "<br>" +
                "Region: " + treemap_df['region'] + "<br>" +
                "Country: " + treemap_df['country'] + "<br>" +
                "Exchange: " + treemap_df['exchange'] + "<br>" +
                "Sector: " + treemap_df['sector'] + "<br>" +
                "Market Cap: " + treemap_df['market_cap'].apply(format_market_cap) + "<br>" +
                "Performance: " + treemap_df['price_change_since_ipo'].apply(format_percentage)
            )
            
            # Create treemap
            fig = px.treemap(
                treemap_df,
                path=[px.Constant("Global IPOs"), 'region', 'country', 'sector', 'ticker'],
                values='market_cap',
                color='price_change_since_ipo',
                hover_data={'hover_text': True},
                color_continuous_scale='RdYlGn',
                color_continuous_midpoint=0,
                title=f"IPO Performance Treemap - {selected_timeframe}",
                labels={'price_change_since_ipo': 'Performance Since IPO'}
            )
            
            fig.update_traces(
                hovertemplate='%{customdata[0]}<extra></extra>',
                textinfo="label+value"
            )
            
            fig.update_layout(
                height=600,
                font_size=12,
                title_font_size=16
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Country Summary Section
        st.subheader("🌍 Global Market Overview")
        
        # Create country summary with flags and statistics
        country_summary = filtered_df.groupby(['country', 'region']).agg({
            'ticker': 'count',
            'exchange': lambda x: ', '.join(sorted(x.unique())),
            'price_change_since_ipo': 'mean',
            'market_cap': 'sum'
        }).reset_index()
        
        country_summary.columns = ['Country', 'Region', 'IPO Count', 'Exchanges', 'Avg Performance', 'Total Market Cap']
        country_summary = country_summary.sort_values('IPO Count', ascending=False)
        
        # Country flag mapping
        country_flags = {
            'United States': '🇺🇸', 'Canada': '🇨🇦', 'Brazil': '🇧🇷', 'Argentina': '🇦🇷', 'Mexico': '🇲🇽',
            'United Kingdom': '🇬🇧', 'Germany': '🇩🇪', 'France': '🇫🇷', 'Netherlands': '🇳🇱', 'Italy': '🇮🇹',
            'Spain': '🇪🇸', 'Switzerland': '🇨🇭', 'Sweden': '🇸🇪', 'Norway': '🇳🇴', 'Denmark': '🇩🇰',
            'Finland': '🇫🇮', 'Poland': '🇵🇱', 'Czech Republic': '🇨🇿', 'Austria': '🇦🇹', 'Belgium': '🇧🇪',
            'Portugal': '🇵🇹', 'Greece': '🇬🇷', 'Ireland': '🇮🇪', 'Luxembourg': '🇱🇺', 'Estonia': '🇪🇪',
            'Latvia': '🇱🇻', 'Lithuania': '🇱🇹', 'Hungary': '🇭🇺', 'Slovakia': '🇸🇰', 'Slovenia': '🇸🇮',
            'Croatia': '🇭🇷', 'Romania': '🇷🇴', 'Bulgaria': '🇧🇬', 'Serbia': '🇷🇸', 'Turkey': '🇹🇷',
            'Russia': '🇷🇺', 'Ukraine': '🇺🇦', 'Israel': '🇮🇱', 'Saudi Arabia': '🇸🇦', 'UAE': '🇦🇪',
            'Qatar': '🇶🇦', 'Kuwait': '🇰🇼', 'Egypt': '🇪🇬', 'South Africa': '🇿🇦', 'Nigeria': '🇳🇬',
            'China': '🇨🇳', 'Hong Kong': '🇭🇰', 'Japan': '🇯🇵', 'South Korea': '🇰🇷', 'India': '🇮🇳',
            'Singapore': '🇸🇬', 'Australia': '🇦🇺', 'New Zealand': '🇳🇿', 'Thailand': '🇹🇭', 'Malaysia': '🇲🇾',
            'Indonesia': '🇮🇩', 'Philippines': '🇵🇭', 'Vietnam': '🇻🇳', 'Taiwan': '🇹🇼', 'Bangladesh': '🇧🇩',
            'Pakistan': '🇵🇰', 'Sri Lanka': '🇱🇰', 'Myanmar': '🇲🇲', 'Cambodia': '🇰🇭', 'Laos': '🇱🇦'
        }
        
        # Add flags to country names
        country_summary['Country_Display'] = country_summary['Country'].apply(
            lambda x: f"{country_flags.get(x, '🏳️')} {x}"
        )
        
        # Format performance and market cap
        country_summary['Performance'] = country_summary['Avg Performance'].apply(
            lambda x: f"+{x:.1f}%" if x >= 0 else f"{x:.1f}%"
        )
        country_summary['Market Cap'] = country_summary['Total Market Cap'].apply(format_market_cap)
        
        # Display country summary in columns
        cols = st.columns(3)
        for i, (_, row) in enumerate(country_summary.iterrows()):
            col_idx = i % 3
            with cols[col_idx]:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    border-left: 4px solid #4CAF50;
                ">
                    <h4 style="margin: 0; color: #2c3e50;">{row['Country_Display']}</h4>
                    <p style="margin: 5px 0; color: #34495e;"><strong>Region:</strong> {row['Region']}</p>
                    <p style="margin: 5px 0; color: #34495e;"><strong>IPOs:</strong> {row['IPO Count']}</p>
                    <p style="margin: 5px 0; color: #34495e;"><strong>Performance:</strong> {row['Performance']}</p>
                    <p style="margin: 5px 0; color: #34495e;"><strong>Market Cap:</strong> {row['Market Cap']}</p>
                    <p style="margin: 5px 0; font-size: 0.9em; color: #7f8c8d;"><strong>Exchanges:</strong> {row['Exchanges']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Additional sections
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance distribution
            st.subheader("📊 Performance Distribution")
            hist_fig = px.histogram(
                filtered_df,
                x='price_change_since_ipo',
                nbins=20,
                title="Distribution of IPO Performance",
                labels={'price_change_since_ipo': 'Performance Since IPO', 'count': 'Number of IPOs'}
            )
            hist_fig.update_layout(height=400)
            st.plotly_chart(hist_fig, use_container_width=True)
        
        with col2:
            # Sector performance
            st.subheader("🏢 Sector Performance")
            sector_perf = filtered_df.groupby('sector')['price_change_since_ipo'].mean().sort_values(ascending=True)
            sector_fig = px.bar(
                x=sector_perf.values,
                y=sector_perf.index,
                orientation='h',
                title="Average Performance by Sector",
                labels={'x': 'Average Performance', 'y': 'Sector'}
            )
            sector_fig.update_layout(height=400)
            st.plotly_chart(sector_fig, use_container_width=True)
        
        # Expandable sections
        with st.expander("🚀 Top Performers"):
            top_performers = filtered_df.nlargest(10, 'price_change_since_ipo')[
                ['ticker', 'company_name', 'country', 'sector', 'price_change_since_ipo', 'market_cap']
            ]
            top_performers['Performance'] = top_performers['price_change_since_ipo'].apply(format_percentage)
            top_performers['Market Cap'] = top_performers['market_cap'].apply(format_market_cap)
            st.dataframe(
                top_performers[['ticker', 'company_name', 'country', 'sector', 'Performance', 'Market Cap']],
                use_container_width=True
            )
        
        with st.expander("📉 Worst Performers"):
            worst_performers = filtered_df.nsmallest(10, 'price_change_since_ipo')[
                ['ticker', 'company_name', 'country', 'sector', 'price_change_since_ipo', 'market_cap']
            ]
            worst_performers['Performance'] = worst_performers['price_change_since_ipo'].apply(format_percentage)
            worst_performers['Market Cap'] = worst_performers['market_cap'].apply(format_market_cap)
            st.dataframe(
                worst_performers[['ticker', 'company_name', 'country', 'sector', 'Performance', 'Market Cap']],
                use_container_width=True
            )
        
        with st.expander("📋 Detailed IPO Data"):
            display_df = filtered_df.copy()
            display_df['Performance'] = display_df['price_change_since_ipo'].apply(format_percentage)
            display_df['Market Cap'] = display_df['market_cap'].apply(format_market_cap)
            st.dataframe(
                display_df[['ticker', 'company_name', 'region', 'country', 'exchange', 'sector', 'Performance', 'Market Cap']],
                use_container_width=True
            )

else:
    # No data available
    st.info("👆 Please click 'Refresh IPO Data' in the sidebar to load IPO data for visualization.")
    
    # Show sample data structure
    st.subheader("📋 Expected Data Structure")
    sample_data = {
        'ticker': ['RDDT', 'SMCI', 'ARM', 'SHOP.TO', 'ASML.AS'],
        'company_name': ['Reddit Inc.', 'Super Micro Computer', 'ARM Holdings', 'Shopify Inc.', 'ASML Holding'],
        'region': ['Americas', 'Americas', 'Americas', 'Americas', 'EMEA'],
        'country': ['United States', 'United States', 'United States', 'Canada', 'Netherlands'],
        'sector': ['Technology', 'Technology', 'Technology', 'Technology', 'Technology'],
        'exchange': ['NYSE', 'NASDAQ', 'NASDAQ', 'TSX', 'AMS'],
        'market_cap': [8500000000, 45000000000, 120000000000, 180000000000, 350000000000],
        'price_change_since_ipo': [0.15, -0.25, 0.08, 2.45, 1.85]
    }
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df, use_container_width=True)

# AI Commentary Section
st.markdown("---")
st.subheader("🤖 AI Market Analysis")

if not df.empty and not filtered_df.empty:
    try:
        commentary = get_ipo_commentary(filtered_df, selected_timeframe)
        if commentary:
            # Clean and format the commentary for proper markdown display
            cleaned_commentary = commentary.replace('**', '**').replace('*', '*')
            st.markdown(cleaned_commentary)
        else:
            # Fallback analysis with proper markdown formatting
            regional_analysis = []
            for region in filtered_df['region'].unique():
                avg_perf = filtered_df[filtered_df['region'] == region]['price_change_since_ipo'].mean()
                regional_analysis.append(f"- **{region}:** {format_percentage(avg_perf)} average returns")
            
            sector_analysis = []
            for sector in filtered_df['sector'].value_counts().head(5).index:
                avg_perf = filtered_df[filtered_df['sector'] == sector]['price_change_since_ipo'].mean()
                sector_analysis.append(f"- **{sector}:** {format_percentage(avg_perf)} average performance")
            
            st.markdown(f"""
### IPO Market Analysis - {selected_timeframe}

**Market Overview:**  
Analyzing {len(filtered_df)} IPOs with an average performance of {format_percentage(filtered_df['price_change_since_ipo'].mean())} since listing.

**Regional Performance:**  
{chr(10).join(regional_analysis)}

**Sector Analysis:**  
{chr(10).join(sector_analysis)}

**Key Insights:**  
The performance disparity across regions and sectors reflects varying market conditions, investor sentiment, and economic fundamentals. Strong performers likely benefit from favorable market dynamics and investor confidence, while underperformers may face sector-specific challenges or regional economic pressures.

*Note: AI-powered detailed analysis is temporarily unavailable. This summary provides basic statistical insights.*
            """)
            st.info("ℹ️ Showing statistical analysis (OpenAI API not configured)")
    except Exception as e:
        st.error(f"Error generating AI commentary: {str(e)}")

# News Section
st.markdown("---")
st.subheader("📰 IPO News")

try:
    # Check if API keys are configured
    import os
    tavily_key = os.getenv('TAVILY_API_KEY')
    exa_key = os.getenv('EXA_API_KEY', 'ba4e615f-b7e9-4b91-b83f-591aa0ec5132')  # Use provided key as default
    
    if tavily_key or exa_key:
        news_data = get_ipo_news()
        if news_data is not None and len(news_data) > 0:
            st.success(f"✅ Live news data loaded ({len(news_data)} articles)")
            # Display news in a nice format
            for article in news_data[:5]:  # Show top 5 articles
                # Handle both dict and string formats
                if isinstance(article, dict):
                    title = article.get('title', 'No title')
                    url = article.get('url', '#')
                    summary = article.get('summary', 'No summary available')
                    date = article.get('date', 'No date')
                    source = article.get('source', 'Unknown source')
                    relevance_score = article.get('relevance_score', None)
                else:
                    # Handle string format or other formats
                    title = str(article)
                    url = '#'
                    summary = 'No summary available'
                    date = 'No date'
                    source = 'Unknown source'
                    relevance_score = None
                
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**[{title}]({url})**")
                        st.markdown(f"*{summary}*")
                        st.markdown(f"📅 {date} | 📰 {source}")
                    with col2:
                        if relevance_score is not None:
                            st.metric("Relevance", f"{relevance_score:.2f}")
                    st.markdown("---")
        else:
            st.warning("⚠️ No news data available from configured APIs")
    else:
        st.info("ℹ️ Showing sample news data (API keys not configured)")
        # Show sample news
        sample_news = [
            {
                "title": "Major Technology IPO Expected in Q4 2025",
                "summary": "A leading AI company is preparing for a significant public offering worth over $10 billion.",
                "source": "Financial Times",
                "date": "2025-09-22",
                "relevance_score": 0.95
            },
            {
                "title": "Healthcare IPO Market Shows Strong Recovery",
                "summary": "Biotech companies are seeing increased investor interest with several successful listings this quarter.",
                "source": "Reuters",
                "date": "2025-09-21",
                "relevance_score": 0.88
            }
        ]
        
        for article in sample_news:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{article['title']}**")
                    st.markdown(f"*{article['summary']}*")
                    st.markdown(f"📅 {article['date']} | 📰 {article['source']}")
                with col2:
                    st.metric("Relevance", f"{article['relevance_score']:.2f}")
                st.markdown("---")
                
except Exception as e:
    st.error(f"Error loading news: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Developed by [Julian Kaljuvee](https://www.linkedin.com/in/kaljuvee/) at [Predictive Labs](https://www.predictivelabs.ai/)")
