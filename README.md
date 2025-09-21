# IPO Analytics - Market Heatmap Dashboard

A comprehensive Streamlit application that visualizes Initial Public Offering (IPO) performance data using an interactive market heatmap similar to Finviz. The application tracks IPOs from NASDAQ and NYSE exchanges, showing performance since listing with sector-based organization and market cap-weighted visualization.

## 🚀 Features

- **Interactive Market Heatmap**: Treemap visualization showing IPO performance with color-coded returns
- **Real-time Data**: Fetches live data from Yahoo Finance API
- **SQLite Database**: Local data storage for efficient querying and caching
- **Sector Analysis**: Performance breakdown by industry sectors
- **Exchange Filtering**: Filter by NASDAQ, NYSE, or both exchanges
- **Market Cap Filtering**: Adjustable minimum market capitalization filters
- **Performance Metrics**: Detailed statistics including top/worst performers
- **Hover Information**: Comprehensive details including IPO date, market cap, and performance

## 📊 Visualization Details

The heatmap displays:
- **Rectangle Size**: Proportional to current market capitalization
- **Color Coding**: Performance since IPO (green = positive, red = negative)
- **Hover Data**: 
  - Company ticker and name
  - Sector and exchange
  - IPO Date (First Listing)
  - Current market capitalization
  - Performance percentage since IPO

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- pip package manager

### Setup Instructions

1. **Clone or download the project**:
   ```bash
   cd IPOAnalytics
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
├── Home.py                 # Main Streamlit application
├── utils/
│   ├── yfinance_util.py   # Yahoo Finance data fetching utilities
│   └── database.py        # SQLite database management
├── data/
│   └── ipo_analytics.db   # SQLite database (created automatically)
├── requirements.txt       # Python dependencies
├── test_app.py           # Test suite for functionality verification
└── README.md             # This file
```

## 🔧 Usage

### Initial Setup
1. Launch the application using `streamlit run Home.py`
2. Click "🔄 Refresh IPO Data" in the sidebar to populate the database
3. The app will fetch IPO data from Yahoo Finance and store it locally

### Navigation
- **Year Selection**: Choose which year's IPOs to analyze
- **Exchange Filter**: Select NASDAQ, NYSE, or both
- **Sector Filter**: Filter by specific industry sectors
- **Market Cap Filter**: Set minimum market capitalization threshold

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
- Calculates performance metrics since IPO date
- Handles missing data and delisted securities gracefully
- Implements rate limiting to respect API constraints

### Visualization
- Uses Plotly Express for interactive treemap generation
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
5. **Market Coverage**: Currently focuses on US exchanges (NASDAQ/NYSE)

## 🔮 Future Enhancements

- **Automated IPO Discovery**: Integration with dedicated IPO data providers
- **International Exchanges**: Support for European and Asian markets
- **Advanced Analytics**: Volatility metrics, sector rotation analysis
- **Real-time Updates**: Live data streaming and automatic refresh
- **Export Functionality**: CSV/Excel export of filtered data
- **Alert System**: Email notifications for significant IPO movements

## 🤝 Contributing

To extend the application:

1. **Add New Exchanges**: Modify `yfinance_util.py` to include additional exchanges
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
