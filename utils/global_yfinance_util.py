"""
Enhanced Global YFinance Utility for IPO Analytics
Fetches IPO data from all major global exchanges with regional categorization
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import time
from typing import List, Dict, Optional, Tuple
import logging
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Comprehensive global exchange mapping with regional categorization
GLOBAL_EXCHANGES = {
    # AMERICAS
    'Americas': {
        # United States
        'NASDAQ': {'country': 'United States', 'suffix': '', 'name': 'NASDAQ'},
        'NYSE': {'country': 'United States', 'suffix': '', 'name': 'New York Stock Exchange'},
        'AMEX': {'country': 'United States', 'suffix': '', 'name': 'American Stock Exchange'},
        'NYSEARCA': {'country': 'United States', 'suffix': '', 'name': 'NYSE Arca'},
        
        # Canada
        'TSX': {'country': 'Canada', 'suffix': '.TO', 'name': 'Toronto Stock Exchange'},
        'TSXV': {'country': 'Canada', 'suffix': '.V', 'name': 'TSX Venture Exchange'},
        'CSE': {'country': 'Canada', 'suffix': '.CN', 'name': 'Canadian Securities Exchange'},
        
        # Brazil
        'B3': {'country': 'Brazil', 'suffix': '.SA', 'name': 'B3 Brasil Bolsa Balcão'},
        'BOVESPA': {'country': 'Brazil', 'suffix': '.SA', 'name': 'Bovespa'},
        
        # Mexico
        'BMV': {'country': 'Mexico', 'suffix': '.MX', 'name': 'Mexican Stock Exchange'},
        
        # Argentina
        'BCBA': {'country': 'Argentina', 'suffix': '.BA', 'name': 'Buenos Aires Stock Exchange'},
        
        # Chile
        'BCS': {'country': 'Chile', 'suffix': '.SN', 'name': 'Santiago Stock Exchange'},
        
        # Colombia
        'BVC': {'country': 'Colombia', 'suffix': '.BO', 'name': 'Colombian Stock Exchange'},
        
        # Peru
        'BVL': {'country': 'Peru', 'suffix': '.LM', 'name': 'Lima Stock Exchange'},
    },
    
    # EMEA (Europe, Middle East, Africa)
    'EMEA': {
        # United Kingdom
        'LSE': {'country': 'United Kingdom', 'suffix': '.L', 'name': 'London Stock Exchange'},
        'AIM': {'country': 'United Kingdom', 'suffix': '.L', 'name': 'Alternative Investment Market'},
        'LON': {'country': 'United Kingdom', 'suffix': '.L', 'name': 'London Stock Exchange'},
        
        # Germany
        'XETRA': {'country': 'Germany', 'suffix': '.DE', 'name': 'Xetra'},
        'FSE': {'country': 'Germany', 'suffix': '.F', 'name': 'Frankfurt Stock Exchange'},
        'FRA': {'country': 'Germany', 'suffix': '.F', 'name': 'Frankfurt Stock Exchange'},
        'BER': {'country': 'Germany', 'suffix': '.BE', 'name': 'Berlin Stock Exchange'},
        'MUN': {'country': 'Germany', 'suffix': '.MU', 'name': 'Munich Stock Exchange'},
        'STU': {'country': 'Germany', 'suffix': '.SG', 'name': 'Stuttgart Stock Exchange'},
        'HAM': {'country': 'Germany', 'suffix': '.HM', 'name': 'Hamburg Stock Exchange'},
        'DUS': {'country': 'Germany', 'suffix': '.DU', 'name': 'Düsseldorf Stock Exchange'},
        
        # France
        'EPA': {'country': 'France', 'suffix': '.PA', 'name': 'Euronext Paris'},
        'EURONEXT': {'country': 'France', 'suffix': '.PA', 'name': 'Euronext'},
        'PAR': {'country': 'France', 'suffix': '.PA', 'name': 'Paris Stock Exchange'},
        
        # Netherlands
        'AMS': {'country': 'Netherlands', 'suffix': '.AS', 'name': 'Euronext Amsterdam'},
        
        # Italy
        'BIT': {'country': 'Italy', 'suffix': '.MI', 'name': 'Borsa Italiana'},
        'MIL': {'country': 'Italy', 'suffix': '.MI', 'name': 'Milan Stock Exchange'},
        
        # Spain
        'BME': {'country': 'Spain', 'suffix': '.MC', 'name': 'Bolsas y Mercados Españoles'},
        'MCE': {'country': 'Spain', 'suffix': '.MC', 'name': 'Madrid Stock Exchange'},
        'MAD': {'country': 'Spain', 'suffix': '.MC', 'name': 'Madrid Stock Exchange'},
        
        # Switzerland
        'SIX': {'country': 'Switzerland', 'suffix': '.SW', 'name': 'SIX Swiss Exchange'},
        'VTX': {'country': 'Switzerland', 'suffix': '.SW', 'name': 'SIX Swiss Exchange'},
        
        # Nordic Countries
        'STO': {'country': 'Sweden', 'suffix': '.ST', 'name': 'Stockholm Stock Exchange'},
        'HEL': {'country': 'Finland', 'suffix': '.HE', 'name': 'Helsinki Stock Exchange'},
        'CPH': {'country': 'Denmark', 'suffix': '.CO', 'name': 'Copenhagen Stock Exchange'},
        'OSL': {'country': 'Norway', 'suffix': '.OL', 'name': 'Oslo Stock Exchange'},
        
        # Other European
        'WSE': {'country': 'Poland', 'suffix': '.WA', 'name': 'Warsaw Stock Exchange'},
        'BUD': {'country': 'Hungary', 'suffix': '.BD', 'name': 'Budapest Stock Exchange'},
        'PRA': {'country': 'Czech Republic', 'suffix': '.PR', 'name': 'Prague Stock Exchange'},
        'ATH': {'country': 'Greece', 'suffix': '.AT', 'name': 'Athens Stock Exchange'},
        'LIS': {'country': 'Portugal', 'suffix': '.LS', 'name': 'Lisbon Stock Exchange'},
        'BRU': {'country': 'Belgium', 'suffix': '.BR', 'name': 'Euronext Brussels'},
        'VIE': {'country': 'Austria', 'suffix': '.VI', 'name': 'Vienna Stock Exchange'},
        'TAL': {'country': 'Estonia', 'suffix': '.TL', 'name': 'Tallinn Stock Exchange'},
        'RIG': {'country': 'Latvia', 'suffix': '.RG', 'name': 'Riga Stock Exchange'},
        'VSE': {'country': 'Lithuania', 'suffix': '.VS', 'name': 'Vilnius Stock Exchange'},
        'IST': {'country': 'Turkey', 'suffix': '.IS', 'name': 'Istanbul Stock Exchange'},
        'MSX': {'country': 'Russia', 'suffix': '.ME', 'name': 'Moscow Exchange'},
        'TASE': {'country': 'Israel', 'suffix': '.TA', 'name': 'Tel Aviv Stock Exchange'},
        'JSE': {'country': 'South Africa', 'suffix': '.JO', 'name': 'Johannesburg Stock Exchange'},
        'DFM': {'country': 'UAE', 'suffix': '.DU', 'name': 'Dubai Financial Market'},
        'ADX': {'country': 'UAE', 'suffix': '.AD', 'name': 'Abu Dhabi Securities Exchange'},
        'TADAWUL': {'country': 'Saudi Arabia', 'suffix': '.SR', 'name': 'Saudi Stock Exchange'},
        'QE': {'country': 'Qatar', 'suffix': '.QA', 'name': 'Qatar Stock Exchange'},
        'KSE': {'country': 'Kuwait', 'suffix': '.KW', 'name': 'Kuwait Stock Exchange'},
        'EGX': {'country': 'Egypt', 'suffix': '.CA', 'name': 'Egyptian Exchange'},
        'CSE': {'country': 'Morocco', 'suffix': '.CS', 'name': 'Casablanca Stock Exchange'},
        'NSE_NG': {'country': 'Nigeria', 'suffix': '.LG', 'name': 'Nigerian Stock Exchange'},
        'NSE_KE': {'country': 'Kenya', 'suffix': '.NR', 'name': 'Nairobi Securities Exchange'},
    },
    
    # APAC (Asia-Pacific)
    'APAC': {
        # China
        'SSE': {'country': 'China', 'suffix': '.SS', 'name': 'Shanghai Stock Exchange'},
        'SZSE': {'country': 'China', 'suffix': '.SZ', 'name': 'Shenzhen Stock Exchange'},
        
        # Hong Kong
        'HKEX': {'country': 'Hong Kong', 'suffix': '.HK', 'name': 'Hong Kong Stock Exchange'},
        'HKG': {'country': 'Hong Kong', 'suffix': '.HK', 'name': 'Hong Kong Stock Exchange'},
        
        # Japan
        'TSE': {'country': 'Japan', 'suffix': '.T', 'name': 'Tokyo Stock Exchange'},
        'JPX': {'country': 'Japan', 'suffix': '.T', 'name': 'Japan Exchange Group'},
        'OSA': {'country': 'Japan', 'suffix': '.OS', 'name': 'Osaka Exchange'},
        
        # South Korea
        'KRX': {'country': 'South Korea', 'suffix': '.KS', 'name': 'Korea Exchange'},
        'KOSPI': {'country': 'South Korea', 'suffix': '.KS', 'name': 'KOSPI'},
        'KOSDAQ': {'country': 'South Korea', 'suffix': '.KQ', 'name': 'KOSDAQ'},
        
        # India
        'BSE': {'country': 'India', 'suffix': '.BO', 'name': 'Bombay Stock Exchange'},
        'NSE': {'country': 'India', 'suffix': '.NS', 'name': 'National Stock Exchange of India'},
        
        # Singapore
        'SGX': {'country': 'Singapore', 'suffix': '.SI', 'name': 'Singapore Exchange'},
        
        # Taiwan
        'TWSE': {'country': 'Taiwan', 'suffix': '.TW', 'name': 'Taiwan Stock Exchange'},
        'TPEx': {'country': 'Taiwan', 'suffix': '.TWO', 'name': 'Taipei Exchange'},
        
        # Australia
        'ASX': {'country': 'Australia', 'suffix': '.AX', 'name': 'Australian Securities Exchange'},
        
        # New Zealand
        'NZX': {'country': 'New Zealand', 'suffix': '.NZ', 'name': 'New Zealand Exchange'},
        
        # Southeast Asia
        'SET': {'country': 'Thailand', 'suffix': '.BK', 'name': 'Stock Exchange of Thailand'},
        'KLSE': {'country': 'Malaysia', 'suffix': '.KL', 'name': 'Kuala Lumpur Stock Exchange'},
        'IDX': {'country': 'Indonesia', 'suffix': '.JK', 'name': 'Indonesia Stock Exchange'},
        'PSE': {'country': 'Philippines', 'suffix': '.PS', 'name': 'Philippine Stock Exchange'},
        'HOSE': {'country': 'Vietnam', 'suffix': '.VN', 'name': 'Ho Chi Minh Stock Exchange'},
        'HNX': {'country': 'Vietnam', 'suffix': '.HN', 'name': 'Hanoi Stock Exchange'},
        
        # Other APAC
        'DSE': {'country': 'Bangladesh', 'suffix': '.DH', 'name': 'Dhaka Stock Exchange'},
        'KSE': {'country': 'Pakistan', 'suffix': '.KA', 'name': 'Karachi Stock Exchange'},
        'CSE': {'country': 'Sri Lanka', 'suffix': '.CM', 'name': 'Colombo Stock Exchange'},
        'MSE': {'country': 'Mongolia', 'suffix': '.UB', 'name': 'Mongolian Stock Exchange'},
        'KASE': {'country': 'Kazakhstan', 'suffix': '.KZ', 'name': 'Kazakhstan Stock Exchange'},
        'UzSE': {'country': 'Uzbekistan', 'suffix': '.UZ', 'name': 'Uzbekistan Stock Exchange'},
    }
}

# Known IPO tickers by region (sample data - would be expanded with real IPO databases)
KNOWN_IPOS_BY_REGION = {
    'Americas': {
        'US': ['RDDT', 'SMCI', 'ARM', 'SOLV', 'KKVR', 'KROS', 'TMDX', 'CGON', 'KRYS', 'VERA', 'IMVT', 'PRCT', 'CGEM', 'LYEL', 'NRIX', 'BCYC', 'TPG', 'FBIN', 'SOLV', 'KROS'],
        'Canada': ['SHOP.TO', 'LSPD.TO', 'NUVEI.TO', 'WELL.TO', 'DOC.V', 'FOOD.TO'],
        'Brazil': ['MGLU3.SA', 'VVAR3.SA', 'RENT3.SA', 'CASH3.SA', 'LWSA3.SA', 'MELI.SA'],
        'Mexico': ['AMXL.MX', 'GFNORTEO.MX', 'LIVEPOLC-1.MX', 'ORBIA.MX'],
    },
    'EMEA': {
        'UK': ['WISE.L', 'DPLM.L', 'MOONPIG.L', 'THG.L', 'DELIVEROO.L', 'DARKTRACE.L'],
        'Germany': ['DELIVERY.DE', 'ABOUT.DE', 'ZEAL.DE', 'SYNLAB.DE', 'VERBIO.DE'],
        'France': ['MCPHY.PA', 'NEOEN.PA', 'BELIEVE.PA', 'PLANISWARE.PA'],
        'Netherlands': ['ADYEN.AS', 'JDE.AS', 'PROSUS.AS', 'BESI.AS'],
        'Italy': ['FERRARI.MI', 'MONCLER.MI', 'AMPLIFON.MI', 'RECORDATI.MI'],
        'Spain': ['SOLARIA.MC', 'SIEMENS.MC', 'CELLNEX.MC', 'MERLIN.MC'],
        'Switzerland': ['PARTNERS.SW', 'ALCON.SW', 'SIG.SW', 'TEMENOS.SW'],
        'Nordic': ['SPOTIFY.ST', 'EVOLUTION.ST', 'NIBE.ST', 'INVESTOR.ST'],
        'Other_EU': ['ALLEGRO.WA', 'CD.WA', 'DINO.WA', 'LPP.WA', 'CCC.WA'],
    },
    'APAC': {
        'China': ['9988.HK', '9618.HK', '1024.HK', '2015.HK', '6060.HK'],
        'Japan': ['4385.T', '4477.T', '4490.T', '4565.T', '4588.T'],
        'South_Korea': ['035720.KS', '251270.KS', '068270.KS', '035900.KS'],
        'India': ['ZOMATO.NS', 'PAYTM.NS', 'NYKAA.NS', 'POLICYBZR.NS', 'CARTRADE.NS'],
        'Singapore': ['G13.SI', 'S68.SI', 'AWX.SI', 'BN4.SI'],
        'Australia': ['APT.AX', 'ZIP.AX', 'BRN.AX', 'NXT.AX', 'XRO.AX'],
        'Southeast_Asia': ['GRAB.PS', 'SEA.PS', 'GOJEK.JK', 'BUKALAPAK.JK'],
    }
}

class GlobalIPODataFetcher:
    """Enhanced IPO data fetcher for global exchanges"""
    
    def __init__(self):
        self.current_year = datetime.now().year
        self.session = requests.Session()
        
    def get_region_from_exchange(self, exchange: str) -> str:
        """Get region for a given exchange"""
        for region, exchanges in GLOBAL_EXCHANGES.items():
            if exchange in exchanges:
                return region
        return 'Other'
    
    def get_country_from_exchange(self, exchange: str) -> str:
        """Get country for a given exchange"""
        for region, exchanges in GLOBAL_EXCHANGES.items():
            if exchange in exchanges:
                return exchanges[exchange]['country']
        return 'Unknown'
    
    def get_exchange_suffix(self, exchange: str) -> str:
        """Get Yahoo Finance suffix for exchange"""
        for region, exchanges in GLOBAL_EXCHANGES.items():
            if exchange in exchanges:
                return exchanges[exchange]['suffix']
        return ''
    
    def fetch_stock_data(self, ticker: str, exchange: str = None) -> Optional[Dict]:
        """Fetch stock data for a single ticker"""
        try:
            # Add exchange suffix if provided
            if exchange:
                suffix = self.get_exchange_suffix(exchange)
                if suffix and not ticker.endswith(suffix):
                    ticker = f"{ticker}{suffix}"
            
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="max")
            
            if hist.empty or not info:
                return None
            
            # Calculate performance metrics
            first_price = hist['Close'].iloc[0] if len(hist) > 0 else None
            current_price = hist['Close'].iloc[-1] if len(hist) > 0 else None
            
            if first_price is None or current_price is None:
                return None
            
            performance = (current_price - first_price) / first_price
            
            # Get IPO date (approximate from first trading date)
            ipo_date = hist.index[0].strftime('%Y-%m-%d') if len(hist) > 0 else None
            
            # Extract relevant information
            data = {
                'ticker': ticker.split('.')[0],  # Remove suffix for display
                'company_name': info.get('longName', info.get('shortName', ticker)),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'exchange': exchange or 'Unknown',
                'country': self.get_country_from_exchange(exchange) if exchange else 'Unknown',
                'region': self.get_region_from_exchange(exchange) if exchange else 'Other',
                'market_cap': info.get('marketCap', 0),
                'current_price': float(current_price),
                'ipo_price': float(first_price),  # Add IPO price field
                'ipo_date': ipo_date,
                'price_change_since_ipo': float(performance),
                'volume': info.get('volume', 0),
                'employees': info.get('fullTimeEmployees', 0),
                'website': info.get('website', ''),
                'business_summary': info.get('longBusinessSummary', '')[:500] if info.get('longBusinessSummary') else '',
                'last_updated': datetime.now().isoformat()
            }
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
            return None
    
    def fetch_regional_ipos(self, region: str, max_per_country: int = 20) -> List[Dict]:
        """Fetch IPO data for a specific region"""
        logger.info(f"Fetching IPO data for {region} region")
        
        if region not in KNOWN_IPOS_BY_REGION:
            logger.warning(f"No known IPOs for region: {region}")
            return []
        
        all_ipos = []
        region_data = KNOWN_IPOS_BY_REGION[region]
        
        # Get exchanges for this region
        region_exchanges = GLOBAL_EXCHANGES.get(region, {})
        
        for country_group, tickers in region_data.items():
            logger.info(f"Processing {country_group} tickers: {len(tickers)}")
            
            # Determine exchange for country group
            exchange = self._get_primary_exchange_for_country_group(region, country_group)
            
            # Process tickers in parallel
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_ticker = {
                    executor.submit(self.fetch_stock_data, ticker, exchange): ticker 
                    for ticker in tickers[:max_per_country]
                }
                
                for future in as_completed(future_to_ticker):
                    ticker = future_to_ticker[future]
                    try:
                        data = future.result(timeout=30)
                        if data:
                            all_ipos.append(data)
                            logger.info(f"Successfully fetched data for {ticker}")
                        else:
                            logger.warning(f"No data returned for {ticker}")
                    except Exception as e:
                        logger.error(f"Error processing {ticker}: {e}")
                    
                    # Rate limiting
                    time.sleep(0.1)
        
        logger.info(f"Successfully fetched {len(all_ipos)} IPOs for {region}")
        return all_ipos
    
    def _get_primary_exchange_for_country_group(self, region: str, country_group: str) -> str:
        """Get primary exchange for a country group"""
        exchange_mapping = {
            'Americas': {
                'US': 'NASDAQ',
                'Canada': 'TSX',
                'Brazil': 'B3',
                'Mexico': 'BMV',
            },
            'EMEA': {
                'UK': 'LSE',
                'Germany': 'XETRA',
                'France': 'EPA',
                'Netherlands': 'AMS',
                'Italy': 'BIT',
                'Spain': 'BME',
                'Switzerland': 'SIX',
                'Nordic': 'STO',
                'Other_EU': 'WSE',
            },
            'APAC': {
                'China': 'HKEX',
                'Japan': 'TSE',
                'South_Korea': 'KRX',
                'India': 'NSE',
                'Singapore': 'SGX',
                'Australia': 'ASX',
                'Southeast_Asia': 'SET',
            }
        }
        
        return exchange_mapping.get(region, {}).get(country_group, 'Unknown')
    
    def fetch_all_global_ipos(self, max_per_region: int = 50) -> List[Dict]:
        """Fetch IPO data from all global regions"""
        logger.info("Starting global IPO data fetch")
        
        all_ipos = []
        
        for region in ['Americas', 'EMEA', 'APAC']:
            try:
                region_ipos = self.fetch_regional_ipos(region, max_per_region // 3)
                all_ipos.extend(region_ipos)
                logger.info(f"Fetched {len(region_ipos)} IPOs from {region}")
                
                # Rate limiting between regions
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error fetching IPOs for {region}: {e}")
        
        logger.info(f"Total IPOs fetched: {len(all_ipos)}")
        return all_ipos
    
    def get_exchange_list_by_region(self, region: str) -> List[str]:
        """Get list of exchanges for a specific region"""
        return list(GLOBAL_EXCHANGES.get(region, {}).keys())
    
    def get_all_exchanges(self) -> Dict[str, List[str]]:
        """Get all exchanges organized by region"""
        return {region: list(exchanges.keys()) for region, exchanges in GLOBAL_EXCHANGES.items()}

# Utility functions for backward compatibility
def format_market_cap(market_cap: float) -> str:
    """Format market cap for display"""
    if market_cap >= 1e12:
        return f"${market_cap/1e12:.1f}T"
    elif market_cap >= 1e9:
        return f"${market_cap/1e9:.1f}B"
    elif market_cap >= 1e6:
        return f"${market_cap/1e6:.1f}M"
    elif market_cap >= 1e3:
        return f"${market_cap/1e3:.1f}K"
    else:
        return f"${market_cap:.0f}"

def format_percentage(percentage: float) -> str:
    """Format percentage for display"""
    return f"{percentage*100:+.2f}%"

def get_country_from_exchange(exchange: str) -> str:
    """Get country from exchange code"""
    fetcher = GlobalIPODataFetcher()
    return fetcher.get_country_from_exchange(exchange)

def get_region_from_exchange(exchange: str) -> str:
    """Get region from exchange code"""
    fetcher = GlobalIPODataFetcher()
    return fetcher.get_region_from_exchange(exchange)

# Main execution for testing
if __name__ == "__main__":
    fetcher = GlobalIPODataFetcher()
    
    # Test fetching data for each region
    print("Testing Global IPO Data Fetcher")
    print("=" * 50)
    
    # Test Americas
    print("\n1. Testing Americas region:")
    americas_data = fetcher.fetch_regional_ipos('Americas', max_per_country=5)
    print(f"Fetched {len(americas_data)} IPOs from Americas")
    
    # Test EMEA
    print("\n2. Testing EMEA region:")
    emea_data = fetcher.fetch_regional_ipos('EMEA', max_per_country=5)
    print(f"Fetched {len(emea_data)} IPOs from EMEA")
    
    # Test APAC
    print("\n3. Testing APAC region:")
    apac_data = fetcher.fetch_regional_ipos('APAC', max_per_country=5)
    print(f"Fetched {len(apac_data)} IPOs from APAC")
    
    # Show sample data
    all_data = americas_data + emea_data + apac_data
    if all_data:
        print(f"\nSample IPO data:")
        for ipo in all_data[:3]:
            print(f"- {ipo['ticker']} ({ipo['company_name']}) - {ipo['country']} - {ipo['region']}")
    
    print(f"\nTotal IPOs fetched: {len(all_data)}")
    print("Global IPO data fetcher test completed!")
