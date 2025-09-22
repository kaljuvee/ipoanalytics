import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class IPODatabase:
    """SQLite database manager for IPO Analytics"""
    
    def __init__(self, db_path: str = "data/ipo_analytics.db"):
        self.db_path = db_path
        # Ensure data directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create IPO data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ipo_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT UNIQUE NOT NULL,
                    company_name TEXT,
                    sector TEXT,
                    industry TEXT,
                    exchange TEXT,
                    country TEXT,
                    region TEXT,
                    ipo_date TEXT,
                    ipo_price REAL,
                    current_price REAL,
                    market_cap INTEGER,
                    price_change_since_ipo REAL,
                    volume INTEGER,
                    last_updated TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create performance metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL,
                    total_return REAL,
                    annualized_volatility REAL,
                    max_drawdown REAL,
                    days_since_ipo INTEGER,
                    high_52w REAL,
                    low_52w REAL,
                    avg_volume REAL,
                    calculated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ticker) REFERENCES ipo_data (ticker)
                )
            ''')
            
            # Create data refresh log table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS refresh_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    refresh_type TEXT,
                    status TEXT,
                    records_processed INTEGER,
                    error_message TEXT,
                    started_at TEXT,
                    completed_at TEXT
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_ticker ON ipo_data (ticker)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sector ON ipo_data (sector)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_exchange ON ipo_data (exchange)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_ipo_date ON ipo_data (ipo_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_market_cap ON ipo_data (market_cap)')
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    def insert_ipo_data(self, ipo_records: List[Dict]) -> int:
        """Insert or update IPO data records"""
        if not ipo_records:
            return 0
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            inserted_count = 0
            for record in ipo_records:
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO ipo_data 
                        (ticker, company_name, sector, industry, exchange, country, region, ipo_date, 
                         ipo_price, current_price, market_cap, price_change_since_ipo, 
                         volume, last_updated)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        record['ticker'],
                        record['company_name'],
                        record['sector'],
                        record['industry'],
                        record['exchange'],
                        record.get('country', 'Unknown'),
                        record.get('region', 'Other'),
                        record['ipo_date'],
                        record['ipo_price'],
                        record['current_price'],
                        record['market_cap'],
                        record['price_change_since_ipo'],
                        record['volume'],
                        record['last_updated']
                    ))
                    inserted_count += 1
                except Exception as e:
                    logger.error(f"Error inserting record for {record.get('ticker', 'unknown')}: {str(e)}")
                    
            conn.commit()
            logger.info(f"Inserted/updated {inserted_count} IPO records")
            return inserted_count
    
    def insert_performance_metrics(self, ticker: str, metrics: Dict) -> bool:
        """Insert performance metrics for a ticker"""
        if not metrics:
            return False
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO performance_metrics 
                    (ticker, total_return, annualized_volatility, max_drawdown, 
                     days_since_ipo, high_52w, low_52w, avg_volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    ticker,
                    metrics.get('total_return'),
                    metrics.get('annualized_volatility'),
                    metrics.get('max_drawdown'),
                    metrics.get('days_since_ipo'),
                    metrics.get('high_52w'),
                    metrics.get('low_52w'),
                    metrics.get('avg_volume')
                ))
                conn.commit()
                return True
            except Exception as e:
                logger.error(f"Error inserting performance metrics for {ticker}: {str(e)}")
                return False
    
    def get_ipo_data(self, year: int = None, exchange: str = None, 
                     sector: str = None, limit: int = None) -> pd.DataFrame:
        """Retrieve IPO data with optional filters"""
        
        query = "SELECT * FROM ipo_data WHERE 1=1"
        params = []
        
        if year:
            query += " AND strftime('%Y', ipo_date) = ?"
            params.append(str(year))
            
        if exchange:
            query += " AND exchange = ?"
            params.append(exchange)
            
        if sector:
            query += " AND sector = ?"
            params.append(sector)
            
        query += " ORDER BY market_cap DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=params)
            
        return df
    
    def get_sector_summary(self, year: int = None) -> pd.DataFrame:
        """Get sector-wise summary statistics"""
        
        query = '''
            SELECT 
                sector,
                COUNT(*) as count,
                AVG(price_change_since_ipo) as avg_performance,
                SUM(market_cap) as total_market_cap,
                AVG(market_cap) as avg_market_cap,
                MIN(price_change_since_ipo) as min_performance,
                MAX(price_change_since_ipo) as max_performance
            FROM ipo_data 
            WHERE 1=1
        '''
        
        params = []
        if year:
            query += " AND strftime('%Y', ipo_date) = ?"
            params.append(str(year))
            
        query += " GROUP BY sector ORDER BY total_market_cap DESC"
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=params)
            
        return df
    
    def get_exchange_summary(self, year: int = None) -> pd.DataFrame:
        """Get exchange-wise summary statistics"""
        
        query = '''
            SELECT 
                exchange,
                COUNT(*) as count,
                AVG(price_change_since_ipo) as avg_performance,
                SUM(market_cap) as total_market_cap,
                AVG(market_cap) as avg_market_cap
            FROM ipo_data 
            WHERE 1=1
        '''
        
        params = []
        if year:
            query += " AND strftime('%Y', ipo_date) = ?"
            params.append(str(year))
            
        query += " GROUP BY exchange ORDER BY total_market_cap DESC"
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=params)
            
        return df
    
    def get_top_performers(self, limit: int = 10, year: int = None) -> pd.DataFrame:
        """Get top performing IPOs"""
        
        query = '''
            SELECT ticker, company_name, sector, exchange, ipo_date, 
                   price_change_since_ipo, market_cap
            FROM ipo_data 
            WHERE 1=1
        '''
        
        params = []
        if year:
            query += " AND strftime('%Y', ipo_date) = ?"
            params.append(str(year))
            
        query += " ORDER BY price_change_since_ipo DESC LIMIT ?"
        params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=params)
            
        return df
    
    def get_worst_performers(self, limit: int = 10, year: int = None) -> pd.DataFrame:
        """Get worst performing IPOs"""
        
        query = '''
            SELECT ticker, company_name, sector, exchange, ipo_date, 
                   price_change_since_ipo, market_cap
            FROM ipo_data 
            WHERE 1=1
        '''
        
        params = []
        if year:
            query += " AND strftime('%Y', ipo_date) = ?"
            params.append(str(year))
            
        query += " ORDER BY price_change_since_ipo ASC LIMIT ?"
        params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=params)
            
        return df
    
    def log_refresh(self, refresh_type: str, status: str, records_processed: int = 0, 
                   error_message: str = None, started_at: str = None) -> int:
        """Log data refresh operations"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO refresh_log 
                (refresh_type, status, records_processed, error_message, started_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                refresh_type,
                status,
                records_processed,
                error_message,
                started_at or datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            log_id = cursor.lastrowid
            conn.commit()
            return log_id
    
    def get_last_refresh(self) -> Optional[Dict]:
        """Get information about the last data refresh"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM refresh_log 
                ORDER BY completed_at DESC 
                LIMIT 1
            ''')
            
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            
        return None
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Count total records
            cursor.execute("SELECT COUNT(*) FROM ipo_data")
            total_ipos = cursor.fetchone()[0]
            
            # Count by year
            cursor.execute('''
                SELECT strftime('%Y', ipo_date) as year, COUNT(*) as count
                FROM ipo_data 
                GROUP BY year 
                ORDER BY year DESC
            ''')
            by_year = dict(cursor.fetchall())
            
            # Count by exchange
            cursor.execute('''
                SELECT exchange, COUNT(*) as count
                FROM ipo_data 
                GROUP BY exchange 
                ORDER BY count DESC
            ''')
            by_exchange = dict(cursor.fetchall())
            
            # Count by sector
            cursor.execute('''
                SELECT sector, COUNT(*) as count
                FROM ipo_data 
                GROUP BY sector 
                ORDER BY count DESC
            ''')
            by_sector = dict(cursor.fetchall())
            
        return {
            'total_ipos': total_ipos,
            'by_year': by_year,
            'by_exchange': by_exchange,
            'by_sector': by_sector
        }
    
    def clear_data(self, table: str = None):
        """Clear data from specified table or all tables"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if table:
                cursor.execute(f"DELETE FROM {table}")
                logger.info(f"Cleared data from {table} table")
            else:
                cursor.execute("DELETE FROM performance_metrics")
                cursor.execute("DELETE FROM ipo_data")
                cursor.execute("DELETE FROM refresh_log")
                logger.info("Cleared all data from database")
                
            conn.commit()
