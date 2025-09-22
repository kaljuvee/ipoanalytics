"""
Simplified Global Data Loader for IPO Map
Creates sample global IPO data without complex imports
"""

import sqlite3
import logging
import pandas as pd
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

def get_sample_global_companies():
    """Get sample companies from global markets"""
    companies = [
        # US Companies
        {'ticker': 'RDDT', 'name': 'Reddit, Inc.', 'country': 'United States', 'region': 'North America', 'sector': 'Communication Services'},
        {'ticker': 'ARM', 'name': 'Arm Holdings plc', 'country': 'United States', 'region': 'North America', 'sector': 'Technology'},
        {'ticker': 'DASH', 'name': 'DoorDash, Inc.', 'country': 'United States', 'region': 'North America', 'sector': 'Consumer Cyclical'},
        {'ticker': 'ABNB', 'name': 'Airbnb, Inc.', 'country': 'United States', 'region': 'North America', 'sector': 'Consumer Cyclical'},
        {'ticker': 'SNOW', 'name': 'Snowflake Inc.', 'country': 'United States', 'region': 'North America', 'sector': 'Technology'},
        
        # European Companies
        {'ticker': 'ASML.AS', 'name': 'ASML Holding N.V.', 'country': 'Netherlands', 'region': 'Europe', 'sector': 'Technology'},
        {'ticker': 'SAP.DE', 'name': 'SAP SE', 'country': 'Germany', 'region': 'Europe', 'sector': 'Technology'},
        {'ticker': 'NESN.SW', 'name': 'Nestlé S.A.', 'country': 'Switzerland', 'region': 'Europe', 'sector': 'Consumer Defensive'},
        {'ticker': 'NOVN.SW', 'name': 'Novartis AG', 'country': 'Switzerland', 'region': 'Europe', 'sector': 'Healthcare'},
        {'ticker': 'MC.PA', 'name': 'LVMH Moët Hennessy', 'country': 'France', 'region': 'Europe', 'sector': 'Consumer Cyclical'},
        {'ticker': 'ADYEN.AS', 'name': 'Adyen N.V.', 'country': 'Netherlands', 'region': 'Europe', 'sector': 'Financial Services'},
        {'ticker': 'SPOT', 'name': 'Spotify Technology S.A.', 'country': 'Sweden', 'region': 'Europe', 'sector': 'Communication Services'},
        
        # Asian Companies
        {'ticker': 'TSM', 'name': 'Taiwan Semiconductor', 'country': 'Taiwan', 'region': 'Asia Pacific', 'sector': 'Technology'},
        {'ticker': 'BABA', 'name': 'Alibaba Group Holding', 'country': 'China', 'region': 'Asia Pacific', 'sector': 'Consumer Cyclical'},
        {'ticker': 'TCEHY', 'name': 'Tencent Holdings Ltd.', 'country': 'China', 'region': 'Asia Pacific', 'sector': 'Communication Services'},
        {'ticker': '7203.T', 'name': 'Toyota Motor Corporation', 'country': 'Japan', 'region': 'Asia Pacific', 'sector': 'Consumer Cyclical'},
        {'ticker': '005930.KS', 'name': 'Samsung Electronics', 'country': 'South Korea', 'region': 'Asia Pacific', 'sector': 'Technology'},
        {'ticker': 'SE', 'name': 'Sea Limited', 'country': 'Singapore', 'region': 'Asia Pacific', 'sector': 'Communication Services'},
        
        # Indian Companies
        {'ticker': 'RELIANCE.NS', 'name': 'Reliance Industries', 'country': 'India', 'region': 'India', 'sector': 'Energy'},
        {'ticker': 'TCS.NS', 'name': 'Tata Consultancy Services', 'country': 'India', 'region': 'India', 'sector': 'Technology'},
        {'ticker': 'INFY.NS', 'name': 'Infosys Limited', 'country': 'India', 'region': 'India', 'sector': 'Technology'},
        {'ticker': 'HDFCBANK.NS', 'name': 'HDFC Bank Limited', 'country': 'India', 'region': 'India', 'sector': 'Financial Services'},
        
        # Middle East & Africa
        {'ticker': '2222.SR', 'name': 'Saudi Aramco', 'country': 'Saudi Arabia', 'region': 'Middle East & Africa', 'sector': 'Energy'},
        {'ticker': 'NPN.JO', 'name': 'Naspers Limited', 'country': 'South Africa', 'region': 'Middle East & Africa', 'sector': 'Communication Services'},
        
        # Latin America
        {'ticker': 'VALE3.SA', 'name': 'Vale S.A.', 'country': 'Brazil', 'region': 'Latin America', 'sector': 'Basic Materials'},
        {'ticker': 'ITUB4.SA', 'name': 'Itaú Unibanco Holding', 'country': 'Brazil', 'region': 'Latin America', 'sector': 'Financial Services'},
        
        # Australia
        {'ticker': 'CBA.AX', 'name': 'Commonwealth Bank', 'country': 'Australia', 'region': 'Asia Pacific', 'sector': 'Financial Services'},
        {'ticker': 'CSL.AX', 'name': 'CSL Limited', 'country': 'Australia', 'region': 'Asia Pacific', 'sector': 'Healthcare'},
    ]
    
    return companies

def load_global_ipo_data():
    """Load comprehensive global IPO sample data"""
    try:
        companies = get_sample_global_companies()
        
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
                'Technology': 0.15,
                'Communication Services': 0.25,
                'Healthcare': -0.05,
                'Financial Services': 0.05,
                'Consumer Cyclical': 0.10,
                'Energy': 0.08,
                'Industrials': 0.12,
                'Basic Materials': 0.06,
                'Consumer Defensive': 0.03,
                'Utilities': 0.02,
                'Real Estate': -0.02
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
            exchange_mapping = {
                'United States': ['NASDAQ', 'NYSE'],
                'Netherlands': ['AMS'],
                'Germany': ['XETRA'],
                'Switzerland': ['SIX'],
                'France': ['EPA'],
                'Sweden': ['STO'],
                'Taiwan': ['TPE'],
                'China': ['SSE'],
                'Japan': ['TSE'],
                'South Korea': ['KRX'],
                'Singapore': ['SGX'],
                'India': ['NSE'],
                'Saudi Arabia': ['TADAWUL'],
                'South Africa': ['JSE'],
                'Brazil': ['B3'],
                'Australia': ['ASX']
            }
            
            exchanges = exchange_mapping.get(company['country'], ['UNKNOWN'])
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
        _save_to_database(ipo_data)
        
        logger.info(f"Loaded {len(ipo_data)} global IPO records covering {len(set(c['country'] for c in companies))} countries")
        return len(ipo_data)
        
    except Exception as e:
        logger.error(f"Error loading global sample data: {e}")
        return 0

def _save_to_database(ipo_data, db_path="data/ipo_analytics.db"):
    """Save IPO data to SQLite database"""
    try:
        conn = sqlite3.connect(db_path)
        
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
