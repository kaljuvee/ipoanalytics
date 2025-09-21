#!/usr/bin/env python3
"""
Script to update database schema and add sample European IPO data
"""

import sqlite3
import json
from datetime import datetime, date
import random

def update_database_schema():
    """Update database schema to include country column and add sample data"""
    
    # Connect to database
    conn = sqlite3.connect('/home/ubuntu/IPOAnalytics/data/ipo_analytics.db')
    cursor = conn.cursor()
    
    # Check current schema
    cursor.execute("PRAGMA table_info(ipo_data)")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"Current columns: {columns}")
    
    # Add country column if it doesn't exist
    if 'country' not in columns:
        print("Adding country column...")
        cursor.execute("ALTER TABLE ipo_data ADD COLUMN country TEXT")
        
        # Update existing US data with country
        cursor.execute("UPDATE ipo_data SET country = 'United States' WHERE country IS NULL")
        print("Updated existing records with United States country")
    
    # Sample European IPO data
    european_ipos = [
        # United Kingdom - LSE
        {"ticker": "FRAS.L", "company_name": "Fraser Group PLC", "country": "United Kingdom", "exchange": "LSE", "sector": "Consumer Cyclical"},
        {"ticker": "WEIR.L", "company_name": "Weir Group PLC", "country": "United Kingdom", "exchange": "LSE", "sector": "Industrials"},
        {"ticker": "AUTO.L", "company_name": "Auto Trader Group PLC", "country": "United Kingdom", "exchange": "AIM", "sector": "Technology"},
        
        # Germany - XETRA
        {"ticker": "SAP.DE", "company_name": "SAP SE", "country": "Germany", "exchange": "XETRA", "sector": "Technology"},
        {"ticker": "SIE.DE", "company_name": "Siemens AG", "country": "Germany", "exchange": "FSE", "sector": "Industrials"},
        {"ticker": "BAS.DE", "company_name": "BASF SE", "country": "Germany", "exchange": "FRA", "sector": "Basic Materials"},
        
        # France - EPA
        {"ticker": "MC.PA", "company_name": "LVMH Moët Hennessy", "country": "France", "exchange": "EPA", "sector": "Consumer Cyclical"},
        {"ticker": "OR.PA", "company_name": "L'Oréal SA", "country": "France", "exchange": "EURONEXT", "sector": "Consumer Defensive"},
        {"ticker": "BNP.PA", "company_name": "BNP Paribas SA", "country": "France", "exchange": "PAR", "sector": "Financial Services"},
        
        # Netherlands - AMS
        {"ticker": "ASML.AS", "company_name": "ASML Holding NV", "country": "Netherlands", "exchange": "AMS", "sector": "Technology"},
        {"ticker": "INGA.AS", "company_name": "ING Groep NV", "country": "Netherlands", "exchange": "AMS", "sector": "Financial Services"},
        
        # Italy - BIT
        {"ticker": "UCG.MI", "company_name": "UniCredit SpA", "country": "Italy", "exchange": "BIT", "sector": "Financial Services"},
        {"ticker": "ENI.MI", "company_name": "Eni SpA", "country": "Italy", "exchange": "MIL", "sector": "Energy"},
        
        # Spain - BME
        {"ticker": "SAN.MC", "company_name": "Banco Santander SA", "country": "Spain", "exchange": "BME", "sector": "Financial Services"},
        {"ticker": "TEF.MC", "company_name": "Telefónica SA", "country": "Spain", "exchange": "MCE", "sector": "Communication Services"},
        {"ticker": "ITX.MC", "company_name": "Inditex SA", "country": "Spain", "exchange": "MAD", "sector": "Consumer Cyclical"},
        
        # Switzerland - SIX
        {"ticker": "NESN.SW", "company_name": "Nestlé SA", "country": "Switzerland", "exchange": "SIX", "sector": "Consumer Defensive"},
        {"ticker": "ROG.SW", "company_name": "Roche Holding AG", "country": "Switzerland", "exchange": "VTX", "sector": "Healthcare"},
        
        # Nordic Countries
        {"ticker": "VOLV-B.ST", "company_name": "Volvo AB", "country": "Sweden", "exchange": "STO", "sector": "Consumer Cyclical"},
        {"ticker": "ERIC-B.ST", "company_name": "Telefonaktiebolaget LM Ericsson", "country": "Sweden", "exchange": "STO", "sector": "Technology"},
        {"ticker": "NOKIA.HE", "company_name": "Nokia Corporation", "country": "Finland", "exchange": "HEL", "sector": "Technology"},
        {"ticker": "DSV.CO", "company_name": "DSV A/S", "country": "Denmark", "exchange": "CPH", "sector": "Industrials"},
        {"ticker": "EQNR.OL", "company_name": "Equinor ASA", "country": "Norway", "exchange": "OSL", "sector": "Energy"},
        
        # Other European
        {"ticker": "PKN.WA", "company_name": "PKN Orlen SA", "country": "Poland", "exchange": "WSE", "sector": "Energy"},
        {"ticker": "MOL.BU", "company_name": "MOL Hungarian Oil", "country": "Hungary", "exchange": "BUD", "sector": "Energy"},
        {"ticker": "CEZ.PR", "company_name": "CEZ AS", "country": "Czech Republic", "exchange": "PRA", "sector": "Utilities"},
        {"ticker": "OPAP.AT", "company_name": "OPAP SA", "country": "Greece", "exchange": "ATH", "sector": "Consumer Cyclical"},
        {"ticker": "EDP.LS", "company_name": "EDP - Energias de Portugal", "country": "Portugal", "exchange": "LIS", "sector": "Utilities"},
        {"ticker": "UCB.BR", "company_name": "UCB SA", "country": "Belgium", "exchange": "BRU", "sector": "Healthcare"},
        {"ticker": "OMV.VI", "company_name": "OMV AG", "country": "Austria", "exchange": "VIE", "sector": "Energy"},
        {"ticker": "TLG.TL", "company_name": "Tallinna Kaubamaja", "country": "Estonia", "exchange": "TAL", "sector": "Consumer Cyclical"},
        {"ticker": "GRG.RG", "company_name": "Grindeks AS", "country": "Latvia", "exchange": "RIG", "sector": "Healthcare"},
        {"ticker": "LNA.VS", "company_name": "Linas Agro Group", "country": "Lithuania", "exchange": "VSE", "sector": "Consumer Defensive"}
    ]
    
    # Add sample data
    for ipo in european_ipos:
        # Generate realistic sample data
        ipo_price = random.uniform(10, 100)
        current_price = ipo_price * random.uniform(0.5, 3.0)  # -50% to +200% performance
        market_cap = random.randint(1000000000, 100000000000)  # 1B to 100B
        price_change = (current_price - ipo_price) / ipo_price
        volume = random.randint(100000, 10000000)
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO ipo_data 
                (ticker, company_name, sector, industry, exchange, country, ipo_date, 
                 ipo_price, current_price, market_cap, price_change_since_ipo, volume, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ipo["ticker"],
                ipo["company_name"],
                ipo["sector"],
                ipo["sector"],  # Using sector as industry for simplicity
                ipo["exchange"],
                ipo["country"],
                "2024-09-20",  # Sample IPO date in 2024
                ipo_price,
                current_price,
                market_cap,
                price_change,
                volume,
                datetime.now().isoformat()
            ))
            print(f"Added {ipo['ticker']} - {ipo['company_name']} ({ipo['country']})")
        except Exception as e:
            print(f"Error adding {ipo['ticker']}: {e}")
    
    conn.commit()
    
    # Check results
    cursor.execute("SELECT COUNT(*) FROM ipo_data")
    total_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT DISTINCT country FROM ipo_data WHERE country IS NOT NULL")
    countries = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT DISTINCT exchange FROM ipo_data")
    exchanges = [row[0] for row in cursor.fetchall()]
    
    print(f"\nDatabase updated successfully!")
    print(f"Total IPO records: {total_count}")
    print(f"Countries: {', '.join(sorted(countries))}")
    print(f"Exchanges: {', '.join(sorted(exchanges))}")
    
    conn.close()

if __name__ == "__main__":
    update_database_schema()
