"""
Fear & Greed Index Data Collector for ResearchIQ
Fetches market-wide sentiment indicator
Data Quality: MEDIUM - Established metric, market-wide context
"""

import requests
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import sys
import os

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import FEAR_GREED_API_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_fear_greed_index() -> Optional[Dict[str, Any]]:
    """
    Get current Fear & Greed Index for crypto market

    Returns:
        dict: Fear & Greed data including:
            - value: Index value (0-100)
            - value_classification: Label (Extreme Fear, Fear, Neutral, Greed, Extreme Greed)
            - timestamp: When the data was fetched
        None if error

    Data Quality: MEDIUM
    - Established sentiment metric
    - Based on volatility, volume, social media, surveys, dominance
    - Market-wide indicator (not asset-specific)
    - Good for overall market context
    - Free public API, no auth needed
    """
    try:
        logger.info("Fetching Fear & Greed Index...")

        # Make API request
        response = requests.get(FEAR_GREED_API_URL, params={"limit": 1}, timeout=10)

        if response.status_code != 200:
            logger.error(f"Fear & Greed API error: HTTP {response.status_code}")
            return None

        data = response.json()

        if 'data' not in data or not data['data']:
            logger.error("No data in Fear & Greed API response")
            return None

        # Extract latest reading
        latest = data['data'][0]

        value = int(latest.get('value', 50))
        classification = latest.get('value_classification', 'Neutral')

        # Interpret the value
        interpretation = ""
        if value <= 25:
            interpretation = "Extreme Fear - Market may be oversold, potential buying opportunity"
        elif value <= 45:
            interpretation = "Fear - Investors are worried, bearish sentiment"
        elif value <= 55:
            interpretation = "Neutral - Market sentiment balanced"
        elif value <= 75:
            interpretation = "Greed - Investors becoming confident, bullish sentiment"
        else:
            interpretation = "Extreme Greed - Market may be overbought, caution advised"

        result = {
            "value": value,
            "classification": classification,
            "interpretation": interpretation,
            "timestamp": datetime.now().isoformat(),
            "data_quality_note": "Market-wide sentiment indicator (crypto markets)",
            "source": "alternative.me Fear & Greed Index"
        }

        logger.info(f"Fear & Greed Index: {value} ({classification})")
        return result

    except requests.exceptions.Timeout:
        logger.error("Fear & Greed API request timeout")
        return None
    except Exception as e:
        logger.error(f"Error fetching Fear & Greed Index: {str(e)}")
        return None

def get_historical_fear_greed(days: int = 30) -> Optional[Dict[str, Any]]:
    """
    Get historical Fear & Greed Index values (bonus feature)

    Args:
        days: Number of days of historical data to fetch

    Returns:
        dict: Historical data or None if error
    """
    try:
        response = requests.get(FEAR_GREED_API_URL, params={"limit": days}, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        if 'data' not in data or not data['data']:
            return None

        # Format historical data
        historical = []
        for entry in data['data']:
            historical.append({
                "value": int(entry.get('value', 50)),
                "classification": entry.get('value_classification', 'Neutral'),
                "timestamp": entry.get('timestamp')
            })

        # Calculate average and trend
        values = [entry['value'] for entry in historical]
        avg_value = sum(values) / len(values) if values else 50

        # Determine trend
        if len(values) >= 7:
            recent_avg = sum(values[:7]) / 7
            if recent_avg > avg_value + 10:
                trend = "increasing (more greed)"
            elif recent_avg < avg_value - 10:
                trend = "decreasing (more fear)"
            else:
                trend = "stable"
        else:
            trend = "insufficient data"

        return {
            "historical_data": historical,
            "average_value": round(avg_value, 1),
            "trend": trend,
            "period_days": days
        }

    except Exception as e:
        logger.error(f"Error fetching historical Fear & Greed: {str(e)}")
        return None

# Example usage and testing
if __name__ == "__main__":
    # Test current index
    print("Testing Fear & Greed Index...")
    current = get_fear_greed_index()

    if current:
        print(f"✓ Fear & Greed Index: {current['value']}/100")
        print(f"  Classification: {current['classification']}")
        print(f"  Interpretation: {current['interpretation']}")
    else:
        print("✗ Failed to fetch Fear & Greed Index")

    # Test historical (optional)
    print("\nTesting historical data...")
    historical = get_historical_fear_greed(days=7)

    if historical:
        print(f"✓ 7-day average: {historical['average_value']}/100")
        print(f"  Trend: {historical['trend']}")
