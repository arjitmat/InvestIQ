"""
Google Trends Data Collector for ResearchIQ
Tracks search interest over time
Data Quality: MEDIUM - Directional signal of retail interest
"""

from pytrends.request import TrendReq
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import sys
import os
import pandas as pd
import time

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import TRENDS_LOOKBACK_DAYS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_search_interest(
    query: str,
    days: int = TRENDS_LOOKBACK_DAYS
) -> Optional[Dict[str, Any]]:
    """
    Get Google search interest trend for a query

    Args:
        query: Search term (company name or ticker)
        days: Number of days to look back (default: 30)

    Returns:
        dict: Search trend data including:
            - trend_data: Time series of interest (0-100)
            - current_interest: Latest interest level
            - avg_interest: Average over period
            - trend_direction: Rising, falling, or stable
        None if error

    Data Quality: MEDIUM
    - Relative search volume (0-100 scale)
    - Good for tracking retail interest changes
    - Directional signal, not absolute metric
    - Free, no API key needed
    """
    try:
        logger.info(f"Fetching Google Trends for '{query}'")

        # Initialize pytrends
        pytrends = TrendReq(hl='en-US', tz=360)

        # Calculate timeframe
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Build payload
        # timeframe format: 'YYYY-MM-DD YYYY-MM-DD'
        timeframe = f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}"

        pytrends.build_payload(
            kw_list=[query],
            timeframe=timeframe,
            geo='US'  # Focus on US market
        )

        # Get interest over time
        interest_df = pytrends.interest_over_time()

        if interest_df.empty or query not in interest_df.columns:
            logger.warning(f"No trends data found for {query}")
            return {
                "query": query,
                "current_interest": 0,
                "avg_interest": 0,
                "trend_direction": "no data",
                "data_quality_note": "Insufficient search volume or data unavailable"
            }

        # Extract trend values
        trend_values = interest_df[query].values
        current_interest = int(trend_values[-1]) if len(trend_values) > 0 else 0
        avg_interest = int(trend_values.mean())

        # Determine trend direction
        if len(trend_values) >= 7:
            recent_avg = trend_values[-7:].mean()
            earlier_avg = trend_values[-14:-7].mean() if len(trend_values) >= 14 else avg_interest

            if recent_avg > earlier_avg * 1.2:
                trend_direction = "rising"
            elif recent_avg < earlier_avg * 0.8:
                trend_direction = "falling"
            else:
                trend_direction = "stable"
        else:
            trend_direction = "stable"

        # Calculate change percentage
        if len(trend_values) >= 2:
            prev_interest = trend_values[-8] if len(trend_values) >= 8 else trend_values[0]
            change_pct = ((current_interest - prev_interest) / prev_interest * 100) if prev_interest > 0 else 0
        else:
            change_pct = 0

        result = {
            "query": query,
            "current_interest": current_interest,
            "avg_interest": avg_interest,
            "trend_direction": trend_direction,
            "change_pct_7d": round(change_pct, 1),
            "timeframe_days": days,
            "timestamp": datetime.now().isoformat(),
            "data_quality_note": "Relative search interest (0-100 scale)"
        }

        logger.info(f"Trends for {query}: {current_interest}/100 ({trend_direction})")
        return result

    except Exception as e:
        logger.error(f"Error fetching Google Trends for {query}: {str(e)}")
        # Return minimal data instead of None to avoid breaking analysis
        return {
            "query": query,
            "current_interest": 0,
            "avg_interest": 0,
            "trend_direction": "no data",
            "error": str(e),
            "data_quality_note": "Error fetching trends data"
        }

def get_related_queries(query: str) -> Optional[Dict[str, Any]]:
    """
    Get related trending queries (bonus feature)

    Args:
        query: Search term

    Returns:
        dict: Related queries and topics or None if error
    """
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(kw_list=[query], timeframe='now 7-d', geo='US')

        # Get related queries
        related = pytrends.related_queries()

        if not related or query not in related:
            return None

        query_data = related[query]

        return {
            "top_queries": query_data.get('top', pd.DataFrame()).head(5).to_dict('records') if 'top' in query_data else [],
            "rising_queries": query_data.get('rising', pd.DataFrame()).head(5).to_dict('records') if 'rising' in query_data else []
        }

    except Exception as e:
        logger.error(f"Error fetching related queries: {str(e)}")
        return None

# Example usage and testing
if __name__ == "__main__":
    # Test with company name
    print("Testing Google Trends with 'Apple stock'...")
    apple_trends = get_search_interest("Apple stock")

    if apple_trends:
        print(f"✓ Current interest: {apple_trends['current_interest']}/100")
        print(f"  Trend: {apple_trends['trend_direction']}")
        print(f"  7-day change: {apple_trends['change_pct_7d']}%")

    # Test with ticker
    print("\nTesting with 'Tesla'...")
    tesla_trends = get_search_interest("Tesla")

    if tesla_trends:
        print(f"✓ Current interest: {tesla_trends['current_interest']}/100")
        print(f"  Trend: {tesla_trends['trend_direction']}")

    # Small delay between requests to be respectful
    time.sleep(2)

    # Test with crypto
    print("\nTesting with 'Bitcoin'...")
    btc_trends = get_search_interest("Bitcoin")

    if btc_trends:
        print(f"✓ Current interest: {btc_trends['current_interest']}/100")
        print(f"  Trend: {btc_trends['trend_direction']}")
