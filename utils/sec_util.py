"""
SEC EDGAR API Utility Module
Provides functions to access SEC EDGAR data for IPO analysis
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SECUtil:
    """Utility class for accessing SEC EDGAR data"""
    
    BASE_URL = "https://data.sec.gov"
    HEADERS = {
        'User-Agent': 'IPO Map Application (contact@predictive-labs.com)',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'data.sec.gov'
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        
    def get_company_submissions(self, cik: str) -> Dict[str, Any]:
        """
        Get company submission history from SEC EDGAR API
        
        Args:
            cik (str): Company's Central Index Key (10 digits with leading zeros)
            
        Returns:
            Dict containing company submission data
        """
        # Ensure CIK is 10 digits with leading zeros
        cik = str(cik).zfill(10)
        url = f"{self.BASE_URL}/submissions/CIK{cik}.json"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching submissions for CIK {cik}: {e}")
            return {}
    
    def search_s1_filings(self, days_back: int = 90) -> List[Dict[str, Any]]:
        """
        Search for recent S-1 filings (IPO registration statements)
        
        Args:
            days_back (int): Number of days to look back for filings
            
        Returns:
            List of S-1 filings with company information
        """
        s1_filings = []
        
        # Get recent filings from the bulk data
        # Note: This is a simplified approach - in production, you'd want to
        # use the bulk submissions.zip file for better performance
        
        # For now, we'll use a list of known recent IPO companies
        # In a full implementation, you would parse the bulk submissions data
        recent_ipo_companies = [
            {"cik": "0001326801", "name": "Reddit, Inc.", "ticker": "RDDT"},
            {"cik": "0001018724", "name": "Amazon.com, Inc.", "ticker": "AMZN"},
            {"cik": "0000320193", "name": "Apple Inc.", "ticker": "AAPL"},
        ]
        
        for company in recent_ipo_companies:
            try:
                submissions = self.get_company_submissions(company["cik"])
                if submissions:
                    # Look for S-1 filings
                    filings = submissions.get("filings", {}).get("recent", {})
                    forms = filings.get("form", [])
                    dates = filings.get("filingDate", [])
                    accession_numbers = filings.get("accessionNumber", [])
                    
                    for i, form in enumerate(forms):
                        if form in ["S-1", "S-1/A"]:  # S-1 and S-1 amendments
                            filing_date = dates[i] if i < len(dates) else ""
                            accession = accession_numbers[i] if i < len(accession_numbers) else ""
                            
                            s1_filings.append({
                                "company_name": company["name"],
                                "ticker": company["ticker"],
                                "cik": company["cik"],
                                "form": form,
                                "filing_date": filing_date,
                                "accession_number": accession
                            })
                
                # Rate limiting - SEC requires reasonable request rates
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing company {company['name']}: {e}")
                continue
        
        return s1_filings
    
    def get_upcoming_ipos(self) -> List[Dict[str, Any]]:
        """
        Get upcoming IPO information
        Note: This is a placeholder - SEC doesn't provide future IPO dates
        Real implementation would combine S-1 filings with other data sources
        
        Returns:
            List of upcoming IPO information
        """
        # This would typically involve:
        # 1. Finding recent S-1 filings
        # 2. Parsing effectiveness dates
        # 3. Cross-referencing with IPO calendar services
        
        upcoming_ipos = [
            {
                "company_name": "Example Tech Corp",
                "expected_date": "2025-10-15",
                "exchange": "NASDAQ",
                "sector": "Technology",
                "status": "S-1 Filed"
            },
            {
                "company_name": "BioPharm Solutions Inc",
                "expected_date": "2025-11-02",
                "exchange": "NYSE",
                "sector": "Healthcare",
                "status": "S-1/A Filed"
            },
            {
                "company_name": "Green Energy Systems",
                "expected_date": "2025-11-20",
                "exchange": "NASDAQ",
                "sector": "Energy",
                "status": "Registration Statement Filed"
            }
        ]
        
        return upcoming_ipos
    
    def get_company_info_by_ticker(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get company information by ticker symbol
        Note: This requires mapping ticker to CIK first
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            Company information if found
        """
        # In a full implementation, you'd maintain a ticker-to-CIK mapping
        # or use the company tickers JSON file from SEC
        ticker_to_cik = {
            "RDDT": "0001326801",
            "AMZN": "0000320193",
            "AAPL": "0000320193"
        }
        
        cik = ticker_to_cik.get(ticker.upper())
        if cik:
            return self.get_company_submissions(cik)
        
        return None

def get_recent_s1_filings(days_back: int = 30) -> List[Dict[str, Any]]:
    """
    Convenience function to get recent S-1 filings
    
    Args:
        days_back (int): Number of days to look back
        
    Returns:
        List of recent S-1 filings
    """
    sec_util = SECUtil()
    return sec_util.search_s1_filings(days_back)

def get_upcoming_ipo_calendar() -> List[Dict[str, Any]]:
    """
    Convenience function to get upcoming IPO calendar
    
    Returns:
        List of upcoming IPO information
    """
    sec_util = SECUtil()
    return sec_util.get_upcoming_ipos()

if __name__ == "__main__":
    # Test the SEC utility
    sec_util = SECUtil()
    
    print("Testing SEC EDGAR API access...")
    
    # Test company submissions
    print("\n1. Testing company submissions (Apple):")
    apple_data = sec_util.get_company_submissions("0000320193")
    if apple_data:
        print(f"Company: {apple_data.get('name', 'N/A')}")
        print(f"CIK: {apple_data.get('cik', 'N/A')}")
        print(f"Recent filings count: {len(apple_data.get('filings', {}).get('recent', {}).get('form', []))}")
    
    # Test S-1 search
    print("\n2. Testing S-1 filings search:")
    s1_filings = sec_util.search_s1_filings()
    print(f"Found {len(s1_filings)} S-1 filings")
    for filing in s1_filings[:3]:
        print(f"  - {filing['company_name']} ({filing['ticker']}): {filing['form']} on {filing['filing_date']}")
    
    # Test upcoming IPOs
    print("\n3. Testing upcoming IPOs:")
    upcoming = sec_util.get_upcoming_ipos()
    print(f"Found {len(upcoming)} upcoming IPOs")
    for ipo in upcoming:
        print(f"  - {ipo['company_name']}: {ipo['expected_date']} ({ipo['status']})")
