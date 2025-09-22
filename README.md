# IPO Analytics - Global Market Heatmap

A comprehensive Streamlit application that visualizes Initial Public Offering (IPO) performance data using an interactive market heatmap similar to Finviz. The application provides **global market coverage** across 70 exchanges in 50+ countries with regional filtering (APAC/EMEA/Americas), AI-powered market commentary, and real-time news integration.

## 🚀 Features

### Core Functionality
- **Interactive Market Heatmap**: Treemap visualization with hierarchical structure (Global → Region → Country → Sector → Ticker)
- **Global Regional Filtering**: Filter by APAC, EMEA, Americas regions with cascading country/exchange filters
- **Real-time Global Data**: Fetches live data from 70 exchanges across 50+ countries via Yahoo Finance API
- **AI-Powered Commentary**: Market insights and trend analysis using OpenAI GPT integration
- **Real-time News Integration**: Latest IPO news from Tavily and Exa.ai APIs
- **Comprehensive Performance Metrics**: Regional comparisons, sector analysis, and detailed statistics
- **Upcoming IPOs Pipeline**: Comprehensive view of expected public offerings

### Enhanced Technical Features
- **Parallel Data Processing**: Multi-threaded data fetching for improved performance across global markets
- **Comprehensive Error Handling**: Robust fallback mechanisms and status indicators
- **Professional UI**: Clean, responsive design with proper loading states and status indicators
- **SQLite Database**: Optimized local storage with regional indexing and bulk operations

## 🌍 Global Market Coverage (70 Exchanges)

### 🌎 Americas Region (15 Exchanges)
- **United States**: NASDAQ, NYSE, AMEX, NYSEARCA
- **Canada**: TSX, TSXV, CSE
- **Brazil**: B3, BOVESPA
- **Mexico**: BMV
- **Argentina**: BCBA
- **Chile**: BCS
- **Colombia**: BVC
- **Peru**: BVL

### 🌍 EMEA Region (35 Exchanges)
- **United Kingdom**: LSE, AIM, LON
- **Germany**: XETRA, FSE, FRA, BER, MUN, STU, HAM, DUS
- **France**: EPA, EURONEXT, PAR
- **Netherlands**: AMS
- **Italy**: BIT, MIL
- **Spain**: BME, MCE, MAD
- **Switzerland**: SIX, VTX
- **Nordic Countries**: STO (Sweden), HEL (Finland), CPH (Denmark), OSL (Norway)
- **Eastern Europe**: WSE (Poland), BUD (Hungary), PRA (Czech Republic), ATH (Greece), LIS (Portugal), BRU (Belgium), VIE (Austria), TAL (Estonia), RIG (Latvia), VSE (Lithuania)
- **Middle East**: IST (Turkey), TASE (Israel), DFM (Dubai), ADX (Abu Dhabi), TADAWUL (Saudi Arabia), QE (Qatar), KSE (Kuwait)
- **Africa**: JSE (South Africa), EGX (Egypt), CSE (Cyprus), NSE_NG (Nigeria), NSE_KE (Kenya)

### 🌏 APAC Region (20 Exchanges)
- **China**: SSE (Shanghai), SZSE (Shenzhen)
- **Hong Kong**: HKEX, HKG
- **Japan**: TSE (Tokyo), JPX, OSA (Osaka)
- **South Korea**: KRX, KOSPI, KOSDAQ
- **India**: BSE (Bombay), NSE (National)
- **Singapore**: SGX
- **Taiwan**: TWSE, TPEx
- **Australia**: ASX
- **New Zealand**: NZX
- **Southeast Asia**: SET (Thailand), KLSE (Malaysia), IDX (Indonesia), PSE (Philippines), HOSE (Vietnam), HNX (Vietnam)
- **Other APAC**: DSE (Bangladesh), KSE (Pakistan), CSE (Sri Lanka), MSE (Mongolia), KASE (Kazakhstan), UzSE (Uzbekistan)

## 📊 Visualization Details

The heatmap displays:
- **Hierarchy**: All IPOs → Country → Sector → Individual Companies
- **Rectangle Size**: Proportional to current market capitalization
- **Color Coding**: Performance since IPO (green = positive, red = negative)
- **Hover Data**: 
  - Company ticker and name
  - Country and exchange
  - Sector classification
  - IPO Date (First Listing)
  - Current market capitalization
  - Performance percentage since IPO

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- pip package manager

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kaljuvee/ipoanalytics.git
   cd ipoanalytics
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run Home.py
   ```

4. **Access the dashboard**:
   Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
IPOAnalytics/
├── Home.py                          # Main Streamlit application with enhanced UI
├── requirements.txt                 # Python dependencies including AI/news APIs
├── README.md                       # Comprehensive documentation
├── utils/
│   ├── database.py                 # SQLite database management with regional indexing
│   ├── yfinance_util.py           # Original Yahoo Finance utility
│   ├── global_yfinance_util.py    # Enhanced global data fetcher (70 exchanges)
│   ├── enhanced_global_loader.py  # Global data integration and processing
│   ├── regional_mapping.py        # Regional categorization (APAC/EMEA/Americas)
│   ├── ai_commentary.py           # OpenAI integration for market analysis
│   ├── enhanced_news.py           # Tavily/Exa.ai news integration
│   └── performance_utils.py       # Performance calculations and metrics
├── data/
│   └── ipo_analytics.db           # SQLite database (created automatically)
├── docs/                          # Documentation and implementation summaries
│   ├── global_implementation_summary.md
│   ├── browser_testing_summary.md
│   └── enhanced_features_summary.md
└── playground/                    # Development and testing files
```

## 🔧 Usage

### Initial Setup
1. Launch the application using `streamlit run Home.py`
2. Click "🔄 Refresh IPO Data" in the sidebar to populate the database
3. The app will fetch IPO data from Yahoo Finance and store it locally

### Navigation
- **Year Selection**: Choose which year's IPOs to analyze
- **Country Filter**: Select specific countries to analyze
- **Exchange Filter**: Select specific exchanges within countries
- **Sector Filter**: Filter by specific industry sectors

### Data Refresh
- Use the "Refresh IPO Data" button to update with latest market data
- The app tracks refresh history and displays last update information
- Data is cached in SQLite for fast subsequent loads

## 📈 Data Sources

- **Primary Data**: Yahoo Finance API via `yfinance` library
- **IPO Identification**: Curated list of recent IPOs (2024 focus)
- **Market Data**: Real-time stock prices, market caps, and company information
- **Performance Calculation**: Based on first trading day vs current price

## 🎯 Key Metrics Displayed

1. **Total IPOs**: Count of IPOs in selected timeframe
2. **Average Performance**: Mean return since IPO across all companies
3. **Total Market Cap**: Combined market capitalization
4. **Best Performer**: Highest returning IPO with percentage gain

## 🔍 Technical Implementation

### Database Schema
- **ipo_data**: Main table storing IPO information and performance
- **performance_metrics**: Additional calculated metrics
- **refresh_log**: Audit trail of data updates

### Data Processing
- Fetches stock information using Yahoo Finance API
- Maps exchanges to countries for geographic analysis
- Calculates performance metrics since IPO date
- Handles missing data and delisted securities gracefully
- Implements rate limiting to respect API constraints

### Visualization
- Uses Plotly Express for interactive treemap generation
- Country-based hierarchical organization
- Custom color scaling for performance visualization
- Responsive design with container-width charts
- Detailed hover tooltips with comprehensive information

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python test_app.py
```

The test suite verifies:
- Database connectivity and initialization
- Yahoo Finance data fetching
- IPO data processing and storage
- Sector analysis functionality

## 📊 Sample Data

The application includes sample IPO data from 2024, including:
- **Technology**: Reddit (RDDT), ARM Holdings (ARM), Super Micro Computer (SMCI)
- **Financial Services**: TPG Inc (TPG), KKR & Co (KKR)
- **Consumer**: DoorDash (DASH), Airbnb (ABNB), Bumble (BMBL)
- **Healthcare**: Various biotech and pharmaceutical IPOs
- **Industrial**: Rivian (RIVN), Lucid Motors (LCID)

## 🚨 Limitations

1. **IPO Detection**: Uses a curated list rather than automated IPO discovery
2. **Data Accuracy**: Dependent on Yahoo Finance data quality and availability
3. **Historical Scope**: Limited to companies with available trading history
4. **Rate Limits**: Yahoo Finance API has usage restrictions
5. **European Data**: Infrastructure ready but requires European IPO data integration

## 🔮 Future Enhancements

- **Automated IPO Discovery**: Integration with dedicated IPO data providers
- **European IPO Data**: Full integration with European market data
- **Advanced Analytics**: Volatility metrics, sector rotation analysis
- **Real-time Updates**: Live data streaming and automatic refresh
- **Export Functionality**: CSV/Excel export of filtered data
- **Alert System**: Email notifications for significant IPO movements

## 🤝 Contributing

To extend the application:

1. **Add New Exchanges**: Modify `EXCHANGE_COUNTRY_MAP` in `yfinance_util.py`
2. **Enhanced Metrics**: Add new calculations in the performance metrics module
3. **UI Improvements**: Customize the Streamlit interface in `Home.py`
4. **Data Sources**: Integrate additional financial data APIs

## 📄 License

This project is provided as-is for educational and analytical purposes. Please ensure compliance with data provider terms of service when using financial APIs.

## 🆘 Support

For issues or questions:
1. Check the test suite output for diagnostic information
2. Verify internet connectivity for Yahoo Finance API access
3. Ensure all dependencies are properly installed
4. Review the refresh log in the sidebar for data update status

---

**Built with**: Streamlit, Plotly, Yahoo Finance API, SQLite, and Python 3.11
