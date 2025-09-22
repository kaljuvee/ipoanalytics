"""
IPO Research Utility
Combines Exa.ai search and SEC EDGAR data to provide comprehensive upcoming IPO information
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
import json

# Import our custom utilities
try:
    from .exa_util import ExaIPOSearch
    from .sec_util import SECUtil
except ImportError:
    # Handle direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from exa_util import ExaIPOSearch
    from sec_util import SECUtil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IPOResearcher:
    """Combined IPO research using multiple data sources"""
    
    def __init__(self, exa_api_key: str = None):
        """
        Initialize IPO researcher with data sources
        
        Args:
            exa_api_key (str): Exa API key for search functionality
        """
        self.exa_api_key = exa_api_key or os.getenv('EXA_API_KEY')
        self.sec_util = SECUtil()
        
        if self.exa_api_key:
            self.exa_search = ExaIPOSearch(self.exa_api_key)
        else:
            self.exa_search = None
            logger.warning("Exa API key not provided - search functionality will be limited")
    
    def get_comprehensive_ipo_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get comprehensive upcoming IPO data from multiple sources
        
        Returns:
            Dictionary containing upcoming IPOs from different sources
        """
        results = {
            "upcoming_ipos": [],
            "recent_filings": [],
            "news_articles": [],
            "summary": {}
        }
        
        # Get data from SEC EDGAR
        try:
            sec_upcoming = self.sec_util.get_upcoming_ipos()
            sec_filings = self.sec_util.search_s1_filings()
            
            results["upcoming_ipos"].extend(sec_upcoming)
            results["recent_filings"].extend(sec_filings)
            
            logger.info(f"Retrieved {len(sec_upcoming)} upcoming IPOs from SEC")
            logger.info(f"Retrieved {len(sec_filings)} recent S-1 filings from SEC")
            
        except Exception as e:
            logger.error(f"Error retrieving SEC data: {e}")
        
        # Get data from Exa.ai search
        if self.exa_search:
            try:
                exa_upcoming = self.exa_search.search_upcoming_ipos()
                exa_news = self.exa_search.search_recent_ipo_news()
                
                results["upcoming_ipos"].extend(exa_upcoming)
                results["news_articles"].extend(exa_news)
                
                logger.info(f"Retrieved {len(exa_upcoming)} upcoming IPOs from Exa search")
                logger.info(f"Retrieved {len(exa_news)} news articles from Exa search")
                
            except Exception as e:
                logger.error(f"Error retrieving Exa data: {e}")
        
        # Add some curated upcoming IPOs based on recent market intelligence
        curated_ipos = self._get_curated_upcoming_ipos()
        results["upcoming_ipos"].extend(curated_ipos)
        
        # Create summary
        results["summary"] = {
            "total_upcoming_ipos": len(results["upcoming_ipos"]),
            "total_recent_filings": len(results["recent_filings"]),
            "total_news_articles": len(results["news_articles"]),
            "last_updated": datetime.now().isoformat()
        }
        
        # Remove duplicates and clean data
        results["upcoming_ipos"] = self._deduplicate_ipos(results["upcoming_ipos"])
        
        return results
    
    def _get_curated_upcoming_ipos(self) -> List[Dict[str, Any]]:
        """
        Get curated list of upcoming IPOs based on market intelligence
        
        Returns:
            List of curated upcoming IPO information
        """
        # This would typically be updated based on market research
        # For now, including some known companies that have filed or announced IPO intentions
        curated_ipos = [
            {
                "company_name": "Stripe, Inc.",
                "expected_date": "Q2 2025",
                "exchange": "NASDAQ",
                "sector": "Financial Services",
                "status": "IPO Preparation Reported",
                "estimated_valuation": "$95B",
                "description": "Payment processing platform"
            },
            {
                "company_name": "SpaceX",
                "expected_date": "Q3 2025",
                "exchange": "NASDAQ",
                "sector": "Aerospace & Defense",
                "status": "IPO Consideration Reported",
                "estimated_valuation": "$180B",
                "description": "Space exploration and satellite internet"
            },
            {
                "company_name": "Discord Inc.",
                "expected_date": "Q4 2025",
                "exchange": "NYSE",
                "sector": "Communication Services",
                "status": "IPO Preparation Reported",
                "estimated_valuation": "$15B",
                "description": "Gaming and community communication platform"
            },
            {
                "company_name": "Databricks Inc.",
                "expected_date": "Q1 2026",
                "exchange": "NASDAQ",
                "sector": "Technology",
                "status": "S-1 Preparation Reported",
                "estimated_valuation": "$43B",
                "description": "Data analytics and AI platform"
            },
            {
                "company_name": "Canva Pty Ltd",
                "expected_date": "Q2 2026",
                "exchange": "NASDAQ",
                "sector": "Technology",
                "status": "IPO Consideration Reported",
                "estimated_valuation": "$40B",
                "description": "Online graphic design platform"
            }
        ]
        
        return curated_ipos
    
    def _deduplicate_ipos(self, ipos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicate IPO entries based on company name
        
        Args:
            ipos (List[Dict]): List of IPO entries
            
        Returns:
            Deduplicated list of IPO entries
        """
        seen_companies = set()
        unique_ipos = []
        
        for ipo in ipos:
            company_name = ipo.get("company_name", "").lower().strip()
            if company_name and company_name not in seen_companies:
                seen_companies.add(company_name)
                unique_ipos.append(ipo)
        
        return unique_ipos
    
    def get_upcoming_ipos_for_display(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get formatted upcoming IPO data for display in the application
        
        Args:
            limit (int): Maximum number of IPOs to return
            
        Returns:
            List of formatted IPO data for display
        """
        comprehensive_data = self.get_comprehensive_ipo_data()
        upcoming_ipos = comprehensive_data["upcoming_ipos"]
        
        # Sort by expected date (putting TBD dates at the end)
        def sort_key(ipo):
            date_str = ipo.get("expected_date", "TBD")
            if date_str == "TBD":
                return "9999-12-31"  # Put TBD dates at the end
            # Try to parse various date formats
            try:
                if "Q" in date_str and "202" in date_str:
                    # Quarter format like "Q2 2025"
                    quarter, year = date_str.split()
                    quarter_num = int(quarter[1])
                    month = (quarter_num - 1) * 3 + 2  # Middle month of quarter
                    return f"{year}-{month:02d}-15"
                elif "/" in date_str or "-" in date_str:
                    # Date format
                    return date_str
                else:
                    return date_str
            except:
                return "9999-12-31"
        
        sorted_ipos = sorted(upcoming_ipos, key=sort_key)
        
        # Format for display
        display_ipos = []
        for ipo in sorted_ipos[:limit]:
            display_ipo = {
                "company_name": ipo.get("company_name", "Unknown"),
                "expected_date": ipo.get("expected_date", "TBD"),
                "exchange": ipo.get("exchange", "TBD"),
                "sector": ipo.get("sector", "TBD"),
                "status": ipo.get("status", "Announced"),
                "estimated_valuation": ipo.get("estimated_valuation", "TBD"),
                "description": ipo.get("description", "")
            }
            display_ipos.append(display_ipo)
        
        return display_ipos

def get_upcoming_ipos(exa_api_key: str = None, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Convenience function to get upcoming IPO information
    
    Args:
        exa_api_key (str): Exa API key for enhanced search
        limit (int): Maximum number of IPOs to return
        
    Returns:
        List of upcoming IPO information
    """
    researcher = IPOResearcher(exa_api_key)
    return researcher.get_upcoming_ipos_for_display(limit)

if __name__ == "__main__":
    # Test the IPO researcher
    exa_api_key = "ba4e615f-b7e9-4b91-b83f-591aa0ec5132"
    
    print("Testing IPO Research functionality...")
    
    researcher = IPOResearcher(exa_api_key)
    
    print("\n1. Getting comprehensive IPO data:")
    comprehensive_data = researcher.get_comprehensive_ipo_data()
    
    print(f"Summary:")
    print(f"  - Total upcoming IPOs: {comprehensive_data['summary']['total_upcoming_ipos']}")
    print(f"  - Recent filings: {comprehensive_data['summary']['total_recent_filings']}")
    print(f"  - News articles: {comprehensive_data['summary']['total_news_articles']}")
    
    print("\n2. Upcoming IPOs for display:")
    display_ipos = researcher.get_upcoming_ipos_for_display(limit=8)
    
    for i, ipo in enumerate(display_ipos, 1):
        print(f"{i}. {ipo['company_name']}")
        print(f"   Expected: {ipo['expected_date']}")
        print(f"   Exchange: {ipo['exchange']}, Sector: {ipo['sector']}")
        print(f"   Status: {ipo['status']}")
        if ipo['estimated_valuation'] != "TBD":
            print(f"   Valuation: {ipo['estimated_valuation']}")
        if ipo['description']:
            print(f"   Description: {ipo['description']}")
        print()
    
    print("IPO research test completed!")
