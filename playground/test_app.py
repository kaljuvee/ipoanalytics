#!/usr/bin/env python3
"""
Test script for IPO Analytics application
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from yfinance_util import IPODataFetcher, format_market_cap, format_percentage
from database import IPODatabase
from datetime import datetime

def test_database_connection():
    """Test database initialization and connection"""
    print("🔍 Testing database connection...")
    try:
        db = IPODatabase()
        stats = db.get_database_stats()
        print(f"✅ Database connected successfully")
        print(f"   Total IPOs in database: {stats['total_ipos']}")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def test_data_fetcher():
    """Test Yahoo Finance data fetching"""
    print("\n🔍 Testing Yahoo Finance data fetcher...")
    try:
        fetcher = IPODataFetcher()
        
        # Test with a few known tickers
        test_tickers = ["RDDT", "ARM", "SMCI"]
        
        for ticker in test_tickers:
            print(f"   Testing {ticker}...")
            info = fetcher.get_stock_info(ticker)
            if info:
                print(f"   ✅ {ticker}: {info['company_name']} - {format_market_cap(info['market_cap'])}")
            else:
                print(f"   ⚠️ {ticker}: No data available")
        
        return True
    except Exception as e:
        print(f"❌ Data fetcher test failed: {str(e)}")
        return False

def test_ipo_data_fetch():
    """Test IPO data fetching and database insertion"""
    print("\n🔍 Testing IPO data fetch and database insertion...")
    try:
        db = IPODatabase()
        fetcher = IPODataFetcher()
        
        # Fetch sample IPO data
        print("   Fetching IPO data...")
        ipo_data = fetcher.get_nasdaq_nyse_ipos(year=2024)
        
        if ipo_data:
            print(f"   ✅ Fetched {len(ipo_data)} IPO records")
            
            # Insert into database
            records_inserted = db.insert_ipo_data(ipo_data)
            print(f"   ✅ Inserted {records_inserted} records into database")
            
            # Test data retrieval
            df = db.get_ipo_data(year=2024)
            print(f"   ✅ Retrieved {len(df)} records from database")
            
            if len(df) > 0:
                print("\n📊 Sample data:")
                for _, row in df.head(3).iterrows():
                    print(f"   {row['ticker']}: {row['company_name']} - {format_percentage(row['price_change_since_ipo'])}")
            
            return True
        else:
            print("   ⚠️ No IPO data fetched")
            return False
            
    except Exception as e:
        print(f"❌ IPO data test failed: {str(e)}")
        return False

def test_sector_analysis():
    """Test sector analysis functionality"""
    print("\n🔍 Testing sector analysis...")
    try:
        db = IPODatabase()
        
        # Get sector summary
        sector_df = db.get_sector_summary(year=2024)
        
        if len(sector_df) > 0:
            print(f"   ✅ Found {len(sector_df)} sectors")
            print("\n📈 Top sectors by market cap:")
            for _, row in sector_df.head(3).iterrows():
                print(f"   {row['sector']}: {row['count']} IPOs, {format_percentage(row['avg_performance'])} avg performance")
            return True
        else:
            print("   ⚠️ No sector data available")
            return False
            
    except Exception as e:
        print(f"❌ Sector analysis test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting IPO Analytics Test Suite")
    print("=" * 50)
    
    tests = [
        test_database_connection,
        test_data_fetcher,
        test_ipo_data_fetch,
        test_sector_analysis
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! The IPO Analytics app is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the error messages above.")
    
    return passed == total

if __name__ == "__main__":
    main()
