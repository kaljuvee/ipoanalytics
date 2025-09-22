"""
Global Data Loader for IPO Map
Loads sample IPO data for global markets including APAC, EMEA, and other regions
"""

import sqlite3
import logging
import pandas as pd
from datetime import datetime, timedelta
import random
from global_markets import get_all_sample_companies, get_country_from_exchange, get_region_from_country

logger = logging.getLogger(__name__)

class GlobalIPODataLoader:
    def __init__(self, db_path: str = "data/ipo_analytics.db"):
        self.db_path = db_path
        
    def load_global_sample_data(self):
        """Load comprehensive global IPO sample data"""
        try:
            # Get all sample companies from global markets
            companies = get_all_sample_companies()
            
            # Generate realistic IPO data for each company
            ipo_data = []
            base_date = datetime(2022, 1, 1)
            
            for i, company in enumerate(companies):
                # Generate random IPO date within the last 3 years
                days_offset = random.randint(0, 1095)  # 3 years
                ipo_date = base_date + timedelta(days=days_offset)
                
                # Generate realistic market cap (in USD)
                market_cap_ranges = {
                    'Technology': (5e9, 500e9),
                    'Financial Services': (10e9, 300e9),
                    'Healthcare': (1e9, 100e9),
                    'Consumer Cyclical': (2e9, 200e9),
                    'Communication Services': (10e9, 1000e9),
                    'Energy': (5e9, 500e9),
                    'Industrials': (3e9, 150e9),
                    'Basic Materials': (2e9, 100e9),
                    'Consumer Defensive': (5e9, 200e9),
                    'Utilities': (3e9, 100e9),
                    'Real Estate': (1e9, 50e9)
                }
                
                sector = company['sector']
                min_cap, max_cap = market_cap_ranges.get(sector, (1e9, 50e9))
                market_cap = random.uniform(min_cap, max_cap)
                
                # Generate performance based on sector and region trends
                performance_factors = {
                    'Technology': 0.15,  # Generally positive
                    'Communication Services': 0.25,  # Very positive
                    'Healthcare': -0.05,  # Slightly negative
                    'Financial Services': 0.05,  # Slightly positive
                    'Consumer Cyclical': 0.10,  # Positive
                    'Energy': 0.08,  # Positive
                    'Industrials': 0.12,  # Positive
                    'Basic Materials': 0.06,  # Slightly positive
                    'Consumer Defensive': 0.03,  # Stable
                    'Utilities': 0.02,  # Stable
                    'Real Estate': -0.02  # Slightly negative
                }
                
                regional_factors = {
                    'North America': 0.05,
                    'Europe': 0.02,
                    'Asia Pacific': 0.08,
                    'India': 0.12,
                    'Middle East & Africa': 0.03,
                    'Latin America': 0.01
                }
                
                base_performance = performance_factors.get(sector, 0.0)
                regional_boost = regional_factors.get(company['region'], 0.0)
                
                # Add some randomness
                random_factor = random.uniform(-0.3, 0.5)
                final_performance = base_performance + regional_boost + random_factor
                
                # Determine exchange based on country
                country = company['country']
                exchange_mapping = {
                    'United States': ['NASDAQ', 'NYSE'],
                    'Canada': ['TSX'],
                    'United Kingdom': ['LSE', 'AIM'],
                    'Germany': ['XETRA', 'FSE'],
                    'France': ['EPA', 'EURONEXT'],
                    'Japan': ['TSE', 'TYO'],
                    'China': ['SSE', 'SZSE'],
                    'Hong Kong': ['HKEX'],
                    'South Korea': ['KRX', 'KOSPI'],
                    'Singapore': ['SGX'],
                    'Australia': ['ASX'],
                    'India': ['NSE', 'BSE'],
                    'Saudi Arabia': ['TADAWUL'],
                    'UAE': ['DFM', 'ADX'],
                    'South Africa': ['JSE'],
                    'Brazil': ['B3'],
                    'Mexico': ['BMV']
                }
                
                exchanges = exchange_mapping.get(country, ['UNKNOWN'])
                exchange = random.choice(exchanges)
                
                ipo_record = {
                    'ticker': company['ticker'],
                    'company_name': company['name'],
                    'sector': company['sector'],
                    'country': company['country'],
                    'region': company['region'],
                    'exchange': exchange,
                    'ipo_date': ipo_date.strftime('%Y-%m-%d'),
                    'market_cap': market_cap,
                    'price_change_since_ipo': final_performance,
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                ipo_data.append(ipo_record)
            
            # Save to database
            self._save_to_database(ipo_data)
            
            logger.info(f"Loaded {len(ipo_data)} global IPO records covering {len(set(c['country'] for c in companies))} countries")
            return len(ipo_data)
            
        except Exception as e:
            logger.error(f"Error loading global sample data: {e}")
            return 0
    
    def _save_to_database(self, ipo_data):
        """Save IPO data to SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Create table if it doesn't exist
            conn.execute('''
                CREATE TABLE IF NOT EXISTS ipo_data (
                    ticker TEXT PRIMARY KEY,
                    company_name TEXT,
                    sector TEXT,
                    country TEXT,
                    region TEXT,
                    exchange TEXT,
                    ipo_date TEXT,
                    market_cap REAL,
                    price_change_since_ipo REAL,
                    last_updated TEXT
                )
            ''')
            
            # Clear existing data
            conn.execute('DELETE FROM ipo_data')
            
            # Insert new data
            df = pd.DataFrame(ipo_data)
            df.to_sql('ipo_data', conn, if_exists='append', index=False)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Saved {len(ipo_data)} records to database")
            
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            raise

# Global instance
global_loader = GlobalIPODataLoader()

def load_global_ipo_data():
    """Convenience function to load global IPO data"""
    return global_loader.load_global_sample_data()
