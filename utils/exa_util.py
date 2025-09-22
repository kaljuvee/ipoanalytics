"""
Exa AI Utility Module
Uses Exa.ai search engine to find upcoming IPO information
"""

import os
from exa_py import Exa
from typing import List, Dict, Any
import json
import re
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExaIPOSearch:
    """Utility class for searching upcoming IPO information using Exa.ai"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize Exa search client
        
        Args:
            api_key (str): Exa API key, defaults to environment variable
        """
        self.api_key = api_key or os.getenv('EXA_API_KEY')
        if not self.api_key:
            raise ValueError("EXA_API_KEY must be provided or set as environment variable")
        
        self.exa = Exa(api_key=self.api_key)
    
    def search_upcoming_ipos(self, num_results: int = 20) -> List[Dict[str, Any]]:
        """
        Search for upcoming IPO information using Exa.ai
        
        Args:
            num_results (int): Number of search results to retrieve
            
        Returns:
            List of upcoming IPO information
        """
        try:
            # Search for upcoming IPOs
            search_query = "upcoming IPO calendar 2024 2025 scheduled companies going public"
            
            results = self.exa.search_and_contents(
                query=search_query,
                type="neural",
                use_autoprompt=True,
                num_results=num_results,
                text=True
            )
            
            upcoming_ipos = []
            
            for result in results.results:
                # Extract IPO information from the content
                ipo_info = self._extract_ipo_info(result.text, result.url, result.title)
                if ipo_info:
                    upcoming_ipos.extend(ipo_info)
            
            return upcoming_ipos
            
        except Exception as e:
            logger.error(f"Error searching for upcoming IPOs: {e}")
            return []
    
    def search_recent_ipo_news(self, num_results: int = 15) -> List[Dict[str, Any]]:
        """
        Search for recent IPO news and announcements
        
        Args:
            num_results (int): Number of search results to retrieve
            
        Returns:
            List of recent IPO news
        """
        try:
            search_query = "IPO filing S-1 registration statement SEC 2024 2025"
            
            results = self.exa.search_and_contents(
                query=search_query,
                type="neural",
                use_autoprompt=True,
                num_results=num_results,
                text=True,
                start_published_date="2024-01-01"
            )
            
            ipo_news = []
            
            for result in results.results:
                news_info = {
                    "title": result.title,
                    "url": result.url,
                    "published_date": getattr(result, 'published_date', None),
                    "summary": result.text[:500] + "..." if len(result.text) > 500 else result.text
                }
                ipo_news.append(news_info)
            
            return ipo_news
            
        except Exception as e:
            logger.error(f"Error searching for IPO news: {e}")
            return []
    
    def _extract_ipo_info(self, text: str, url: str, title: str) -> List[Dict[str, Any]]:
        """
        Extract IPO information from search result text
        
        Args:
            text (str): Content text from search result
            url (str): Source URL
            title (str): Result title
            
        Returns:
            List of extracted IPO information
        """
        ipos = []
        
        # Common patterns for IPO information
        date_patterns = [
            r'(\w+\s+\d{1,2},?\s+202[4-5])',  # Month DD, YYYY
            r'(\d{1,2}[/-]\d{1,2}[/-]202[4-5])',  # MM/DD/YYYY or MM-DD-YYYY
            r'(Q[1-4]\s+202[4-5])',  # Q1 2024, etc.
        ]
        
        company_patterns = [
            r'([A-Z][a-zA-Z\s&,.-]+(?:Inc\.?|Corp\.?|LLC|Ltd\.?|Co\.?))',
            r'([A-Z][a-zA-Z\s&,.-]+(?:Technologies?|Systems?|Solutions?|Group|Holdings?))',
        ]
        
        # Try to extract company names and dates
        companies = []
        dates = []
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            companies.extend([match.strip() for match in matches if len(match.strip()) > 5])
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            dates.extend(matches)
        
        # Remove duplicates and clean up
        companies = list(set(companies))[:5]  # Limit to 5 companies per result
        dates = list(set(dates))[:3]  # Limit to 3 dates per result
        
        # Create IPO entries
        for i, company in enumerate(companies):
            expected_date = dates[i] if i < len(dates) else "TBD"
            
            # Try to determine exchange and sector from context
            exchange = "TBD"
            sector = "TBD"
            
            if "NASDAQ" in text.upper():
                exchange = "NASDAQ"
            elif "NYSE" in text.upper():
                exchange = "NYSE"
            
            # Simple sector detection
            if any(word in text.lower() for word in ['tech', 'software', 'ai', 'data']):
                sector = "Technology"
            elif any(word in text.lower() for word in ['bio', 'pharma', 'medical', 'health']):
                sector = "Healthcare"
            elif any(word in text.lower() for word in ['financial', 'bank', 'fintech']):
                sector = "Financial Services"
            
            ipos.append({
                "company_name": company,
                "expected_date": expected_date,
                "exchange": exchange,
                "sector": sector,
                "status": "Announced",
                "source_url": url,
                "source_title": title
            })
        
        return ipos

def search_upcoming_ipos_with_exa(api_key: str = None) -> List[Dict[str, Any]]:
    """
    Convenience function to search for upcoming IPOs using Exa.ai
    
    Args:
        api_key (str): Exa API key
        
    Returns:
        List of upcoming IPO information
    """
    try:
        exa_search = ExaIPOSearch(api_key)
        return exa_search.search_upcoming_ipos()
    except Exception as e:
        logger.error(f"Error in Exa IPO search: {e}")
        return []

def get_ipo_news_with_exa(api_key: str = None) -> List[Dict[str, Any]]:
    """
    Convenience function to get recent IPO news using Exa.ai
    
    Args:
        api_key (str): Exa API key
        
    Returns:
        List of recent IPO news
    """
    try:
        exa_search = ExaIPOSearch(api_key)
        return exa_search.search_recent_ipo_news()
    except Exception as e:
        logger.error(f"Error in Exa IPO news search: {e}")
        return []

if __name__ == "__main__":
    # Test the Exa utility
    import sys
    
    api_key = "ba4e615f-b7e9-4b91-b83f-591aa0ec5132"  # Test key from user
    
    print("Testing Exa.ai IPO search...")
    
    try:
        exa_search = ExaIPOSearch(api_key)
        
        print("\n1. Searching for upcoming IPOs:")
        upcoming_ipos = exa_search.search_upcoming_ipos(num_results=10)
        print(f"Found {len(upcoming_ipos)} upcoming IPO entries")
        
        for ipo in upcoming_ipos[:5]:  # Show first 5
            print(f"  - {ipo['company_name']}")
            print(f"    Expected: {ipo['expected_date']}")
            print(f"    Exchange: {ipo['exchange']}, Sector: {ipo['sector']}")
            print(f"    Source: {ipo['source_title'][:60]}...")
            print()
        
        print("\n2. Searching for recent IPO news:")
        ipo_news = exa_search.search_recent_ipo_news(num_results=5)
        print(f"Found {len(ipo_news)} news articles")
        
        for news in ipo_news[:3]:  # Show first 3
            print(f"  - {news['title'][:80]}...")
            print(f"    URL: {news['url']}")
            print(f"    Summary: {news['summary'][:100]}...")
            print()
            
    except Exception as e:
        print(f"Error testing Exa search: {e}")
        sys.exit(1)
