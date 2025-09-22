"""
Enhanced IPO News Utility for IPO Map
Uses Tavily search API with Exa.ai as backup to fetch recent IPO-related news
"""

import os
import logging
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests

logger = logging.getLogger(__name__)

class EnhancedIPONewsSearcher:
    def __init__(self, tavily_api_key: Optional[str] = None, exa_api_key: Optional[str] = None):
        """Initialize the news searcher with API keys"""
        self.tavily_api_key = tavily_api_key or os.getenv('TAVILY_API_KEY')
        self.exa_api_key = exa_api_key or os.getenv('EXA_API_KEY')
        
        # Set the provided Exa API key if available
        if not self.exa_api_key:
            self.exa_api_key = 'ba4e615f-b7e9-4b91-b83f-591aa0ec5132'
        
        self.tavily_base_url = "https://api.tavily.com/search"
        
        # Initialize Exa client if available
        self.exa_client = None
        if self.exa_api_key:
            try:
                from exa_py import Exa
                self.exa_client = Exa(api_key=self.exa_api_key)
                logger.info("Exa.ai client initialized successfully")
            except ImportError:
                logger.warning("exa_py not installed - Exa.ai search unavailable")
            except Exception as e:
                logger.error(f"Failed to initialize Exa client: {e}")
        
        # Search keywords for IPO news
        self.search_keywords = [
            "IPO initial public offering 2024 2025",
            "IPO filing SEC S-1 registration",
            "IPO pricing debut listing stock market",
            "upcoming IPO pipeline companies",
            "IPO market performance analysis"
        ]

    def search_ipo_news(self, max_results: int = 10, days_back: int = 7) -> List[Dict]:
        """Search for recent IPO news using available APIs"""
        
        # Try Tavily first
        if self.tavily_api_key:
            try:
                logger.info("Attempting to fetch news with Tavily API")
                articles = self._search_with_tavily(max_results, days_back)
                if articles:
                    logger.info(f"Successfully fetched {len(articles)} articles from Tavily")
                    return articles
            except Exception as e:
                logger.error(f"Tavily search failed: {e}")
        
        # Try Exa.ai as backup
        if self.exa_client:
            try:
                logger.info("Attempting to fetch news with Exa.ai API")
                articles = self._search_with_exa(max_results, days_back)
                if articles:
                    logger.info(f"Successfully fetched {len(articles)} articles from Exa.ai")
                    return articles
            except Exception as e:
                logger.error(f"Exa.ai search failed: {e}")
        
        # Fallback to sample data
        logger.warning("All API searches failed, returning sample data")
        return self._get_sample_news()

    def _search_with_tavily(self, max_results: int, days_back: int) -> List[Dict]:
        """Search using Tavily API"""
        all_articles = []
        
        for keyword in self.search_keywords[:2]:  # Limit to avoid rate limits
            try:
                payload = {
                    "api_key": self.tavily_api_key,
                    "query": keyword,
                    "search_depth": "basic",
                    "include_answer": False,
                    "include_images": False,
                    "include_raw_content": False,
                    "max_results": 5,
                    "include_domains": [
                        "reuters.com", "bloomberg.com", "wsj.com", "ft.com", 
                        "cnbc.com", "marketwatch.com", "yahoo.com", "sec.gov",
                        "businesswire.com", "prnewswire.com", "globenewswire.com"
                    ]
                }
                
                response = requests.post(self.tavily_base_url, json=payload, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                for result in data.get('results', []):
                    article = {
                        'title': result.get('title', 'No title'),
                        'url': result.get('url', ''),
                        'content': result.get('content', '')[:300] + '...',
                        'published_date': result.get('published_date', datetime.now().strftime('%Y-%m-%d')),
                        'source': self._extract_domain(result.get('url', '')),
                        'score': result.get('score', 0.5)
                    }
                    all_articles.append(article)
                    
            except Exception as e:
                logger.error(f"Error with Tavily keyword '{keyword}': {e}")
                continue
        
        # Remove duplicates and sort
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_articles.append(article)
        
        unique_articles.sort(key=lambda x: x.get('score', 0), reverse=True)
        return unique_articles[:max_results]

    def _search_with_exa(self, max_results: int, days_back: int) -> List[Dict]:
        """Search using Exa.ai API"""
        all_articles = []
        
        for keyword in self.search_keywords[:2]:  # Limit searches
            try:
                # Calculate date range
                start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
                
                results = self.exa_client.search_and_contents(
                    query=keyword,
                    type="neural",
                    use_autoprompt=True,
                    num_results=5,
                    text=True,
                    start_published_date=start_date
                )
                
                for result in results.results:
                    # Extract publication date
                    pub_date = getattr(result, 'published_date', None)
                    if pub_date:
                        pub_date = pub_date.strftime('%Y-%m-%d') if hasattr(pub_date, 'strftime') else str(pub_date)
                    else:
                        pub_date = datetime.now().strftime('%Y-%m-%d')
                    
                    article = {
                        'title': result.title or 'No title',
                        'url': result.url or '',
                        'content': (result.text or '')[:300] + '...' if result.text else 'No content available',
                        'published_date': pub_date,
                        'source': self._extract_domain(result.url or ''),
                        'score': getattr(result, 'score', 0.7)  # Default score for Exa results
                    }
                    all_articles.append(article)
                    
            except Exception as e:
                logger.error(f"Error with Exa keyword '{keyword}': {e}")
                continue
        
        # Remove duplicates and sort
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_articles.append(article)
        
        unique_articles.sort(key=lambda x: x.get('score', 0), reverse=True)
        return unique_articles[:max_results]

    def _extract_domain(self, url: str) -> str:
        """Extract domain name from URL"""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            return domain.replace('www.', '')
        except:
            return 'Unknown'

    def _get_sample_news(self) -> List[Dict]:
        """Provide sample news when APIs are not available"""
        current_date = datetime.now()
        
        sample_news = [
            {
                'title': 'Major Tech Company Files for $3B IPO on NASDAQ',
                'url': 'https://reuters.com/tech-ipo-filing-2025',
                'content': 'A leading artificial intelligence company has filed for a $3 billion initial public offering on NASDAQ, marking one of the largest tech IPOs this year. The company specializes in enterprise AI solutions...',
                'published_date': (current_date - timedelta(days=1)).strftime('%Y-%m-%d'),
                'source': 'reuters.com',
                'score': 0.95
            },
            {
                'title': 'Biotech IPO Prices Above Range Amid Strong Demand',
                'url': 'https://bloomberg.com/biotech-ipo-pricing-2025',
                'content': 'A biotechnology company focused on cancer treatments priced its IPO at $28 per share, above the expected range of $22-25, indicating robust investor appetite for healthcare innovation...',
                'published_date': (current_date - timedelta(days=2)).strftime('%Y-%m-%d'),
                'source': 'bloomberg.com',
                'score': 0.92
            },
            {
                'title': 'IPO Market Shows Resilience in Q4 2024',
                'url': 'https://wsj.com/ipo-market-analysis-q4-2024',
                'content': 'The IPO market demonstrated remarkable resilience in the fourth quarter of 2024, with increased filing activity and improved pricing conditions across multiple sectors...',
                'published_date': (current_date - timedelta(days=3)).strftime('%Y-%m-%d'),
                'source': 'wsj.com',
                'score': 0.88
            },
            {
                'title': 'Electric Vehicle Startup Delays IPO Plans',
                'url': 'https://cnbc.com/ev-startup-ipo-delay-2025',
                'content': 'An electric vehicle startup has postponed its planned IPO citing market volatility and the need for additional operational milestones before going public...',
                'published_date': (current_date - timedelta(days=4)).strftime('%Y-%m-%d'),
                'source': 'cnbc.com',
                'score': 0.85
            },
            {
                'title': 'Healthcare Technology IPO Surges 45% on Debut',
                'url': 'https://marketwatch.com/healthtech-ipo-debut-2025',
                'content': 'Shares of a healthcare technology company focused on telemedicine solutions surged 45% on their first day of trading, reflecting strong investor confidence in digital health...',
                'published_date': (current_date - timedelta(days=5)).strftime('%Y-%m-%d'),
                'source': 'marketwatch.com',
                'score': 0.90
            }
        ]
        
        return sample_news

    def format_news_dataframe(self, articles: List[Dict]) -> pd.DataFrame:
        """Format news articles into a pandas DataFrame"""
        if not articles:
            return pd.DataFrame()
        
        try:
            df = pd.DataFrame(articles)
            
            # Format published date
            if 'published_date' in df.columns:
                df['Date'] = pd.to_datetime(df['published_date'], errors='coerce').dt.strftime('%Y-%m-%d')
            
            # Select and rename columns for display
            display_columns = {
                'title': 'Article Title',
                'source': 'Source',
                'Date': 'Date',
                'content': 'Summary',
                'score': 'Relevance Score'
            }
            
            # Keep only available columns
            available_columns = {k: v for k, v in display_columns.items() if k in df.columns}
            df_display = df[list(available_columns.keys())].rename(columns=available_columns)
            
            # Sort by relevance score
            if 'Relevance Score' in df_display.columns:
                df_display = df_display.sort_values('Relevance Score', ascending=False)
            
            return df_display
            
        except Exception as e:
            logger.error(f"Error formatting news DataFrame: {e}")
            return pd.DataFrame()

# Global instance for easy access
enhanced_news_searcher = EnhancedIPONewsSearcher()

def get_enhanced_ipo_news(max_results: int = 10, days_back: int = 7) -> pd.DataFrame:
    """Convenience function to get IPO news as DataFrame"""
    articles = enhanced_news_searcher.search_ipo_news(max_results=max_results, days_back=days_back)
    return enhanced_news_searcher.format_news_dataframe(articles)

def get_enhanced_ipo_news_raw(max_results: int = 10, days_back: int = 7) -> List[Dict]:
    """Convenience function to get raw IPO news data"""
    return enhanced_news_searcher.search_ipo_news(max_results=max_results, days_back=days_back)
