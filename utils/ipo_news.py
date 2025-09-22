"""
IPO News Utility for IPO Map
Uses Tavily search API to fetch recent IPO-related news and articles
"""

import os
import logging
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests

logger = logging.getLogger(__name__)

class IPONewsSearcher:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the news searcher with Tavily API key"""
        self.api_key = api_key or os.getenv('TAVILY_API_KEY')
        if not self.api_key:
            logger.warning("Tavily API key not provided - news search will be limited")
        
        self.base_url = "https://api.tavily.com/search"
        
        # Best practice keywords for IPO news search
        self.search_keywords = [
            "IPO initial public offering",
            "IPO filing SEC S-1",
            "IPO pricing debut listing",
            "IPO market performance",
            "upcoming IPO pipeline",
            "IPO withdrawal postponed",
            "IPO oversubscribed demand",
            "IPO underwriter investment bank",
            "IPO valuation market cap",
            "IPO secondary offering"
        ]

    def search_ipo_news(self, max_results: int = 10, days_back: int = 7) -> List[Dict]:
        """Search for recent IPO news using Tavily API"""
        if not self.api_key:
            return self._get_sample_news()
        
        try:
            all_articles = []
            
            # Search with multiple keyword combinations
            for keyword in self.search_keywords[:3]:  # Limit to avoid rate limits
                articles = self._search_with_keyword(keyword, max_results=5, days_back=days_back)
                all_articles.extend(articles)
            
            # Remove duplicates based on URL
            seen_urls = set()
            unique_articles = []
            for article in all_articles:
                if article.get('url') not in seen_urls:
                    seen_urls.add(article.get('url'))
                    unique_articles.append(article)
            
            # Sort by published date (most recent first)
            unique_articles.sort(key=lambda x: x.get('published_date', ''), reverse=True)
            
            return unique_articles[:max_results]
            
        except Exception as e:
            logger.error(f"Error searching IPO news: {e}")
            return self._get_sample_news()

    def _search_with_keyword(self, keyword: str, max_results: int = 5, days_back: int = 7) -> List[Dict]:
        """Search for news with a specific keyword"""
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            payload = {
                "api_key": self.api_key,
                "query": keyword,
                "search_depth": "basic",
                "include_answer": False,
                "include_images": False,
                "include_raw_content": False,
                "max_results": max_results,
                "include_domains": [
                    "reuters.com", "bloomberg.com", "wsj.com", "ft.com", 
                    "cnbc.com", "marketwatch.com", "yahoo.com", "sec.gov",
                    "businesswire.com", "prnewswire.com", "globenewswire.com"
                ]
            }
            
            response = requests.post(self.base_url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for result in data.get('results', []):
                article = {
                    'title': result.get('title', 'No title'),
                    'url': result.get('url', ''),
                    'content': result.get('content', '')[:300] + '...',  # Truncate content
                    'published_date': result.get('published_date', ''),
                    'source': self._extract_domain(result.get('url', '')),
                    'score': result.get('score', 0)
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            logger.error(f"Error searching with keyword '{keyword}': {e}")
            return []

    def _extract_domain(self, url: str) -> str:
        """Extract domain name from URL"""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            return domain.replace('www.', '')
        except:
            return 'Unknown'

    def _get_sample_news(self) -> List[Dict]:
        """Provide sample news when API is not available"""
        sample_news = [
            {
                'title': 'Tech Startup Files for $2B IPO on NASDAQ',
                'url': 'https://example.com/tech-ipo-filing',
                'content': 'A major technology startup has filed for an initial public offering worth $2 billion, marking one of the largest tech IPOs this year...',
                'published_date': '2025-09-21',
                'source': 'reuters.com',
                'score': 0.95
            },
            {
                'title': 'Biotech Company Prices IPO Above Expected Range',
                'url': 'https://example.com/biotech-ipo-pricing',
                'content': 'A biotechnology company priced its IPO at $25 per share, above the expected range of $20-23, indicating strong investor demand...',
                'published_date': '2025-09-20',
                'source': 'bloomberg.com',
                'score': 0.92
            },
            {
                'title': 'IPO Market Shows Signs of Recovery in Q3',
                'url': 'https://example.com/ipo-market-recovery',
                'content': 'The IPO market is showing signs of recovery with increased filing activity and improved pricing conditions in the third quarter...',
                'published_date': '2025-09-19',
                'source': 'wsj.com',
                'score': 0.88
            },
            {
                'title': 'Electric Vehicle Maker Postpones IPO Plans',
                'url': 'https://example.com/ev-ipo-postponed',
                'content': 'An electric vehicle manufacturer has postponed its IPO plans citing market volatility and investor sentiment concerns...',
                'published_date': '2025-09-18',
                'source': 'cnbc.com',
                'score': 0.85
            },
            {
                'title': 'Healthcare IPO Debuts with 40% First-Day Pop',
                'url': 'https://example.com/healthcare-ipo-debut',
                'content': 'A healthcare technology company saw its shares surge 40% on its first day of trading, reflecting strong investor appetite for the sector...',
                'published_date': '2025-09-17',
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
            # Create DataFrame
            df = pd.DataFrame(articles)
            
            # Add clickable links for Streamlit
            if 'url' in df.columns and 'title' in df.columns:
                df['Title (Link)'] = df.apply(
                    lambda row: f"[{row['title']}]({row['url']})", axis=1
                )
            
            # Format published date
            if 'published_date' in df.columns:
                df['Published'] = pd.to_datetime(df['published_date'], errors='coerce').dt.strftime('%Y-%m-%d')
            
            # Select and rename columns for display
            display_columns = {
                'Title (Link)': 'Article Title',
                'source': 'Source',
                'Published': 'Date',
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
news_searcher = IPONewsSearcher()

def get_ipo_news(max_results: int = 10, days_back: int = 7) -> pd.DataFrame:
    """Convenience function to get IPO news as DataFrame"""
    articles = news_searcher.search_ipo_news(max_results=max_results, days_back=days_back)
    return news_searcher.format_news_dataframe(articles)

def get_ipo_news_raw(max_results: int = 10, days_back: int = 7) -> List[Dict]:
    """Convenience function to get raw IPO news data"""
    return news_searcher.search_ipo_news(max_results=max_results, days_back=days_back)
