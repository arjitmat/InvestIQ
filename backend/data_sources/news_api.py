"""
NewsAPI Data Collector for ResearchIQ
Fetches recent news headlines about assets
Data Quality: CONTEXT ONLY - Limited by free tier (100/day), not comprehensive
"""

import requests
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import NEWSAPI_KEY, NEWS_LOOKBACK_DAYS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_news_headlines(query: str, days: int = NEWS_LOOKBACK_DAYS) -> Optional[List[Dict[str, Any]]]:
    """
    Get recent news headlines for a given query/ticker

    Args:
        query: Search query (typically company name or ticker)
        days: Number of days to look back (default: 7)

    Returns:
        list: List of news articles with headline, source, date
        None if error or no API key

    Data Quality: CONTEXT ONLY
    - Free tier: 100 requests/day
    - Limited coverage (not comprehensive)
    - Headlines only, not full articles
    - Use for awareness, not deep analysis
    """
    if not NEWSAPI_KEY:
        logger.warning("NewsAPI key not configured. Skipping news collection.")
        return None

    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # NewsAPI endpoint
        url = "https://newsapi.org/v2/everything"

        # Parameters
        params = {
            "q": query,
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": 10,  # Limit to 10 most recent
            "apiKey": NEWSAPI_KEY
        }

        logger.info(f"Fetching news for query: {query}")

        # Make request
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 429:
            logger.error("NewsAPI rate limit exceeded (100/day)")
            return None

        if response.status_code != 200:
            logger.error(f"NewsAPI error: {response.status_code}")
            return None

        data = response.json()

        if data.get('status') != 'ok':
            logger.error(f"NewsAPI response not ok: {data.get('message')}")
            return None

        articles = data.get('articles', [])

        if not articles:
            logger.info(f"No news found for {query}")
            return []

        # Format articles
        formatted_articles = []
        for article in articles:
            formatted_articles.append({
                "title": article.get('title'),
                "source": article.get('source', {}).get('name'),
                "url": article.get('url'),
                "published_at": article.get('publishedAt'),
                "description": article.get('description')
            })

        logger.info(f"Found {len(formatted_articles)} news articles for {query}")
        return formatted_articles

    except requests.exceptions.Timeout:
        logger.error(f"NewsAPI request timeout for {query}")
        return None
    except Exception as e:
        logger.error(f"Error fetching news for {query}: {str(e)}")
        return None

def get_headlines_for_ticker(ticker: str, company_name: str = None) -> Optional[List[Dict[str, Any]]]:
    """
    Get news headlines for a ticker, trying both ticker and company name

    Args:
        ticker: Ticker symbol
        company_name: Full company name (optional, improves results)

    Returns:
        list: News articles or None if error
    """
    # Try company name first if available (better results)
    if company_name:
        results = get_news_headlines(company_name)
        if results:
            return results

    # Fallback to ticker symbol
    # Clean ticker for better search (remove special chars like ^, =F)
    clean_ticker = ticker.replace('^', '').replace('-USD', '').replace('=F', '')
    return get_news_headlines(clean_ticker)

# Example usage and testing
if __name__ == "__main__":
    # Test with company name
    print("Testing NewsAPI with 'Apple'...")
    apple_news = get_news_headlines("Apple")

    if apple_news:
        print(f"✓ Found {len(apple_news)} articles")
        if apple_news:
            print(f"  Latest: {apple_news[0]['title']}")
    elif apple_news is None:
        print("✗ API key not configured or error occurred")
    else:
        print("  No articles found")

    # Test with ticker
    print("\nTesting with ticker 'TSLA'...")
    tesla_news = get_headlines_for_ticker("TSLA", "Tesla")

    if tesla_news:
        print(f"✓ Found {len(tesla_news)} articles")
        if tesla_news:
            print(f"  Latest: {tesla_news[0]['title']}")
