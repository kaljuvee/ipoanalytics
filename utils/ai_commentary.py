"""
AI Commentary Utility for IPO Map
Uses LangChain and OpenAI to generate insights on IPO performance patterns
"""

import os
import logging
import pandas as pd
from typing import Dict, List, Optional
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

logger = logging.getLogger(__name__)

class IPOCommentaryGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the commentary generator with OpenAI API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logger.warning("OpenAI API key not provided - commentary generation will be limited")
            self.llm = None
        else:
            try:
                self.llm = OpenAI(
                    openai_api_key=self.api_key,
                    temperature=0.7,
                    max_tokens=1000
                )
                logger.info("OpenAI LLM initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI LLM: {e}")
                self.llm = None
        
        # Define the analysis prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["country_data", "sector_data", "timeframe"],
            template="""
            As a financial analyst specializing in IPO markets, analyze the following IPO performance data and provide insights:

            TIMEFRAME: {timeframe}

            COUNTRY PERFORMANCE DATA:
            {country_data}

            SECTOR PERFORMANCE DATA:
            {sector_data}

            Please provide a comprehensive analysis covering:

            1. **Regional Performance Patterns**: Identify which countries/regions are showing the strongest and weakest IPO performance, and explain potential reasons.

            2. **Sector Analysis**: Highlight which sectors are outperforming or underperforming, and discuss market dynamics driving these trends.

            3. **Market Insights**: Provide reasoning for the performance patterns, considering factors like:
               - Economic conditions and monetary policy
               - Market sentiment and investor appetite
               - Sector-specific trends and disruptions
               - Geopolitical factors affecting regional markets

            4. **Investment Implications**: Suggest what these patterns might mean for future IPO investors and market participants.

            Keep the analysis concise but insightful, focusing on actionable insights and clear explanations of performance drivers.
            """
        )
        
        if self.llm:
            self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        else:
            self.chain = None

    def prepare_country_data(self, df: pd.DataFrame) -> str:
        """Prepare country performance data for analysis"""
        if df.empty:
            return "No country data available"
        
        try:
            # Calculate country-level statistics
            country_stats = df.groupby('country').agg({
                'price_change_since_ipo': ['mean', 'count'],
                'market_cap': 'sum'
            }).round(4)
            
            # Flatten column names
            country_stats.columns = ['avg_performance', 'ipo_count', 'total_market_cap']
            
            # Sort by performance
            country_stats = country_stats.sort_values('avg_performance', ascending=False)
            
            # Format the data for the prompt
            country_summary = []
            for country, row in country_stats.head(10).iterrows():
                performance_pct = row['avg_performance'] * 100
                market_cap_b = row['total_market_cap'] / 1e9
                country_summary.append(
                    f"- {country}: {performance_pct:.1f}% avg performance, "
                    f"{int(row['ipo_count'])} IPOs, ${market_cap_b:.1f}B total market cap"
                )
            
            return "\n".join(country_summary)
            
        except Exception as e:
            logger.error(f"Error preparing country data: {e}")
            return "Error processing country data"

    def prepare_sector_data(self, df: pd.DataFrame) -> str:
        """Prepare sector performance data for analysis"""
        if df.empty:
            return "No sector data available"
        
        try:
            # Calculate sector-level statistics
            sector_stats = df.groupby('sector').agg({
                'price_change_since_ipo': ['mean', 'count'],
                'market_cap': 'sum'
            }).round(4)
            
            # Flatten column names
            sector_stats.columns = ['avg_performance', 'ipo_count', 'total_market_cap']
            
            # Sort by performance
            sector_stats = sector_stats.sort_values('avg_performance', ascending=False)
            
            # Format the data for the prompt
            sector_summary = []
            for sector, row in sector_stats.iterrows():
                performance_pct = row['avg_performance'] * 100
                market_cap_b = row['total_market_cap'] / 1e9
                sector_summary.append(
                    f"- {sector}: {performance_pct:.1f}% avg performance, "
                    f"{int(row['ipo_count'])} IPOs, ${market_cap_b:.1f}B total market cap"
                )
            
            return "\n".join(sector_summary)
            
        except Exception as e:
            logger.error(f"Error preparing sector data: {e}")
            return "Error processing sector data"

    def generate_commentary(self, df: pd.DataFrame, timeframe: str = "Last 3 years") -> str:
        """Generate AI commentary on IPO performance patterns"""
        if not self.chain:
            return self._get_fallback_commentary(df, timeframe)
        
        try:
            # Prepare data for analysis
            country_data = self.prepare_country_data(df)
            sector_data = self.prepare_sector_data(df)
            
            # Generate commentary using LangChain
            response = self.chain.run(
                country_data=country_data,
                sector_data=sector_data,
                timeframe=timeframe
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating AI commentary: {e}")
            return self._get_fallback_commentary(df, timeframe)

    def _get_fallback_commentary(self, df: pd.DataFrame, timeframe: str) -> str:
        """Provide fallback commentary when AI is not available"""
        if df.empty:
            return "No data available for analysis."
        
        try:
            # Basic statistical analysis
            total_ipos = len(df)
            avg_performance = df['price_change_since_ipo'].mean() * 100
            
            # Top performing country
            country_performance = df.groupby('country')['price_change_since_ipo'].mean()
            top_country = country_performance.idxmax()
            top_country_perf = country_performance.max() * 100
            
            # Top performing sector
            sector_performance = df.groupby('sector')['price_change_since_ipo'].mean()
            top_sector = sector_performance.idxmax()
            top_sector_perf = sector_performance.max() * 100
            
            # Bottom performers
            worst_country = country_performance.idxmin()
            worst_country_perf = country_performance.min() * 100
            worst_sector = sector_performance.idxmin()
            worst_sector_perf = sector_performance.min() * 100
            
            commentary = f"""
            ## IPO Market Analysis - {timeframe}

            **Market Overview:**
            Analyzing {total_ipos} IPOs with an average performance of {avg_performance:.1f}% since listing.

            **Regional Performance:**
            - **Best Performing Region:** {top_country} leads with {top_country_perf:.1f}% average returns
            - **Underperforming Region:** {worst_country} shows {worst_country_perf:.1f}% average returns

            **Sector Analysis:**
            - **Top Sector:** {top_sector} sector delivers {top_sector_perf:.1f}% average performance
            - **Challenging Sector:** {worst_sector} sector faces headwinds with {worst_sector_perf:.1f}% returns

            **Key Insights:**
            The performance disparity across regions and sectors reflects varying market conditions, investor sentiment, and economic fundamentals. Strong performers likely benefit from favorable market dynamics and investor confidence, while underperformers may face sector-specific challenges or regional economic pressures.

            *Note: AI-powered detailed analysis is temporarily unavailable. This summary provides basic statistical insights.*
            """
            
            return commentary.strip()
            
        except Exception as e:
            logger.error(f"Error generating fallback commentary: {e}")
            return "Unable to generate market commentary at this time."

# Global instance for easy access
commentary_generator = IPOCommentaryGenerator()

def get_ipo_commentary(df: pd.DataFrame, timeframe: str = "Last 3 years") -> str:
    """Convenience function to generate IPO commentary"""
    return commentary_generator.generate_commentary(df, timeframe)
