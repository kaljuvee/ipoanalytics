"""
Enhanced Global Data Loader for IPO Analytics
Integrates global yfinance utility with database operations
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from global_yfinance_util import GlobalIPODataFetcher
from database import IPODatabase
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

def load_comprehensive_global_ipo_data(max_per_region: int = 100) -> int:
    """
    Load comprehensive global IPO data from all regions using yfinance
    
    Args:
        max_per_region: Maximum number of IPOs to fetch per region
        
    Returns:
        Number of records successfully loaded
    """
    logger.info("Starting comprehensive global IPO data loading")
    
    # Initialize components
    fetcher = GlobalIPODataFetcher()
    db = IPODatabase()
    
    total_loaded = 0
    
    try:
        # Fetch data from all regions
        logger.info("Fetching IPO data from all global regions")
        all_ipos = fetcher.fetch_all_global_ipos(max_per_region)
        
        if not all_ipos:
            logger.warning("No IPO data fetched")
            return 0
        
        # Insert data into database
        logger.info(f"Inserting {len(all_ipos)} IPO records into database")
        records_inserted = db.insert_ipo_data(all_ipos)
        
        total_loaded = records_inserted
        logger.info(f"Successfully loaded {total_loaded} global IPO records")
        
        # Log summary by region
        region_summary = {}
        for ipo in all_ipos:
            region = ipo.get('region', 'Unknown')
            region_summary[region] = region_summary.get(region, 0) + 1
        
        logger.info("Regional distribution:")
        for region, count in region_summary.items():
            logger.info(f"  {region}: {count} IPOs")
        
        return total_loaded
        
    except Exception as e:
        logger.error(f"Error loading global IPO data: {e}")
        return 0

def load_regional_ipo_data(region: str, max_ipos: int = 50) -> int:
    """
    Load IPO data for a specific region
    
    Args:
        region: Region name (Americas, EMEA, APAC)
        max_ipos: Maximum number of IPOs to fetch
        
    Returns:
        Number of records successfully loaded
    """
    logger.info(f"Loading IPO data for {region} region")
    
    # Initialize components
    fetcher = GlobalIPODataFetcher()
    db = IPODatabase()
    
    try:
        # Fetch regional data
        regional_ipos = fetcher.fetch_regional_ipos(region, max_ipos)
        
        if not regional_ipos:
            logger.warning(f"No IPO data fetched for {region}")
            return 0
        
        # Insert data into database
        records_inserted = db.insert_ipo_data(regional_ipos)
        
        logger.info(f"Successfully loaded {records_inserted} IPO records for {region}")
        return records_inserted
        
    except Exception as e:
        logger.error(f"Error loading {region} IPO data: {e}")
        return 0

def get_exchange_coverage_report() -> Dict:
    """
    Generate a report of exchange coverage by region
    
    Returns:
        Dictionary with exchange coverage information
    """
    fetcher = GlobalIPODataFetcher()
    all_exchanges = fetcher.get_all_exchanges()
    
    report = {
        'total_exchanges': sum(len(exchanges) for exchanges in all_exchanges.values()),
        'regions': {},
        'generated_at': datetime.now().isoformat()
    }
    
    for region, exchanges in all_exchanges.items():
        # Get unique countries for this region
        countries = set()
        for exchange in exchanges:
            country = fetcher.get_country_from_exchange(exchange)
            if country != 'Unknown':
                countries.add(country)
        
        report['regions'][region] = {
            'exchange_count': len(exchanges),
            'country_count': len(countries),
            'exchanges': exchanges,
            'countries': sorted(list(countries))
        }
    
    return report

def update_global_ipo_database(force_refresh: bool = False) -> Dict:
    """
    Update the global IPO database with latest data
    
    Args:
        force_refresh: Whether to force a complete refresh
        
    Returns:
        Dictionary with update results
    """
    logger.info("Starting global IPO database update")
    
    db = IPODatabase()
    
    # Check last refresh
    last_refresh = db.get_last_refresh()
    
    if not force_refresh and last_refresh:
        last_refresh_time = datetime.fromisoformat(last_refresh['completed_at'])
        hours_since_refresh = (datetime.now() - last_refresh_time).total_seconds() / 3600
        
        if hours_since_refresh < 24:  # Don't refresh more than once per day
            logger.info(f"Database was refreshed {hours_since_refresh:.1f} hours ago, skipping update")
            return {
                'status': 'skipped',
                'reason': 'Recent refresh found',
                'last_refresh': last_refresh['completed_at'],
                'records_loaded': 0
            }
    
    # Perform comprehensive data load
    start_time = datetime.now()
    records_loaded = load_comprehensive_global_ipo_data(max_per_region=150)
    
    # Log the refresh
    db.log_refresh(
        refresh_type="COMPREHENSIVE_GLOBAL_REFRESH",
        status="SUCCESS" if records_loaded > 0 else "PARTIAL",
        records_processed=records_loaded,
        started_at=start_time.isoformat()
    )
    
    return {
        'status': 'completed',
        'records_loaded': records_loaded,
        'started_at': start_time.isoformat(),
        'completed_at': datetime.now().isoformat()
    }

# Backward compatibility functions
def load_global_ipo_data() -> int:
    """Backward compatibility function"""
    return load_comprehensive_global_ipo_data()

if __name__ == "__main__":
    # Test the enhanced global loader
    print("Testing Enhanced Global IPO Data Loader")
    print("=" * 50)
    
    # Generate exchange coverage report
    print("\n1. Exchange Coverage Report:")
    report = get_exchange_coverage_report()
    print(f"Total exchanges covered: {report['total_exchanges']}")
    
    for region, data in report['regions'].items():
        print(f"\n{region}:")
        print(f"  - {data['exchange_count']} exchanges")
        print(f"  - {data['country_count']} countries")
        print(f"  - Sample countries: {', '.join(data['countries'][:5])}")
    
    # Test loading a small sample
    print(f"\n2. Testing data loading (small sample):")
    records_loaded = load_comprehensive_global_ipo_data(max_per_region=10)
    print(f"Loaded {records_loaded} IPO records")
    
    print("\nEnhanced global loader test completed!")
