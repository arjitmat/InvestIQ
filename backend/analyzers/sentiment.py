"""
Sentiment Aggregation Engine for ResearchIQ
Combines sentiment signals from multiple sources
Data Quality: MEDIUM to LOW - Directional signals, use with caution
"""

import logging
from typing import Optional, Dict, Any
import sys
import os

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import CONFIDENCE_MEDIUM, CONFIDENCE_LOW, CONFIDENCE_CONTEXT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def aggregate_sentiment(
    ticker: str,
    fear_greed_data: Optional[Dict[str, Any]],
    trends_data: Optional[Dict[str, Any]],
    reddit_data: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Aggregate sentiment signals from multiple sources

    Args:
        ticker: Ticker symbol being analyzed
        fear_greed_data: Fear & Greed Index data
        trends_data: Google Trends data
        reddit_data: Reddit mention data

    Returns:
        dict: Aggregated sentiment analysis with:
            - market_sentiment: Fear & Greed interpretation
            - retail_interest: Google Trends analysis
            - social_signals: Reddit mention analysis
            - overall_sentiment: Combined assessment
            - confidence_levels: Quality indicators

    Data Quality: MIXED
    - Market sentiment: MEDIUM (established metric)
    - Retail interest: MEDIUM (search trends)
    - Social signals: LOW (volume only)
    """
    try:
        logger.info(f"Aggregating sentiment for {ticker}")

        result = {
            "ticker": ticker,
            "market_sentiment": _process_fear_greed(fear_greed_data),
            "retail_interest": _process_trends(trends_data),
            "social_signals": _process_reddit(reddit_data),
            "disclaimer": "Sentiment data is directional only. Not suitable for investment decisions."
        }

        # Calculate overall sentiment score (if all data available)
        overall = _calculate_overall_sentiment(fear_greed_data, trends_data, reddit_data)
        result["overall_sentiment"] = overall

        logger.info(f"Sentiment aggregation complete for {ticker}")
        return result

    except Exception as e:
        logger.error(f"Error aggregating sentiment for {ticker}: {str(e)}")
        return {
            "ticker": ticker,
            "error": str(e),
            "market_sentiment": {"status": "unavailable"},
            "retail_interest": {"status": "unavailable"},
            "social_signals": {"status": "unavailable"}
        }

def _process_fear_greed(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process Fear & Greed Index data

    Returns:
        dict: Formatted market sentiment analysis
    """
    if not data:
        return {
            "status": "unavailable",
            "confidence": CONFIDENCE_MEDIUM,
            "note": "Fear & Greed Index data not available"
        }

    return {
        "value": data.get('value', 50),
        "classification": data.get('classification', 'Neutral'),
        "interpretation": data.get('interpretation', 'Market sentiment neutral'),
        "confidence": CONFIDENCE_MEDIUM,
        "note": "Market-wide sentiment indicator (crypto markets)",
        "source": "alternative.me Fear & Greed Index"
    }

def _process_trends(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process Google Trends data

    Returns:
        dict: Formatted retail interest analysis
    """
    if not data or data.get('current_interest', 0) == 0:
        return {
            "status": "unavailable",
            "confidence": CONFIDENCE_MEDIUM,
            "note": "Google Trends data not available"
        }

    current = data.get('current_interest', 0)
    trend = data.get('trend_direction', 'stable')
    change_pct = data.get('change_pct_7d', 0)

    # Interpret interest level
    if current >= 75:
        interest_level = "very high"
        interpretation = "Extremely elevated retail interest - high attention"
    elif current >= 50:
        interest_level = "high"
        interpretation = "Elevated retail interest - significant attention"
    elif current >= 25:
        interest_level = "moderate"
        interpretation = "Moderate retail interest - average attention"
    else:
        interest_level = "low"
        interpretation = "Low retail interest - below average attention"

    return {
        "current_interest": current,
        "interest_level": interest_level,
        "trend_direction": trend,
        "change_7d_pct": change_pct,
        "interpretation": interpretation,
        "confidence": CONFIDENCE_MEDIUM,
        "note": "Relative search interest (0-100 scale)",
        "source": "Google Trends"
    }

def _process_reddit(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process Reddit mention data

    Returns:
        dict: Formatted social signals analysis
    """
    if not data:
        return {
            "status": "unavailable",
            "confidence": CONFIDENCE_LOW,
            "note": "Reddit mention data not available"
        }

    mentions = data.get('total_mentions', 0)
    vs_baseline = data.get('vs_baseline', 'average')
    breakdown = data.get('subreddit_breakdown', {})

    # Interpret mention volume
    if "high" in vs_baseline.lower():
        interpretation = "High social media attention - significant discussion volume"
    elif "elevated" in vs_baseline.lower():
        interpretation = "Elevated social media attention - above average discussion"
    elif "low" in vs_baseline.lower():
        interpretation = "Low social media attention - minimal discussion"
    else:
        interpretation = "Average social media attention - normal discussion levels"

    return {
        "total_mentions": mentions,
        "vs_baseline": vs_baseline,
        "subreddit_breakdown": breakdown,
        "interpretation": interpretation,
        "confidence": CONFIDENCE_LOW,
        "note": "Volume signal only - NOT sentiment quality analysis",
        "caveat": "Use for attention spike detection, not investment decisions",
        "source": f"Reddit ({', '.join(breakdown.keys())})"
    }

def _calculate_overall_sentiment(
    fear_greed_data: Optional[Dict[str, Any]],
    trends_data: Optional[Dict[str, Any]],
    reddit_data: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Calculate overall sentiment combining all signals

    Returns:
        dict: Overall sentiment assessment
    """
    scores = []

    # Fear & Greed contribution (weight: 0.5)
    if fear_greed_data and 'value' in fear_greed_data:
        fg_value = fear_greed_data['value']
        # Normalize to -1 to 1 scale
        fg_score = (fg_value - 50) / 50  # 0 = -1 (extreme fear), 100 = 1 (extreme greed)
        scores.append(("market", fg_score, 0.5))

    # Trends contribution (weight: 0.3)
    if trends_data and trends_data.get('current_interest', 0) > 0:
        trend_direction = trends_data.get('trend_direction', 'stable')
        if trend_direction == 'rising':
            trend_score = 0.5
        elif trend_direction == 'falling':
            trend_score = -0.5
        else:
            trend_score = 0
        scores.append(("retail", trend_score, 0.3))

    # Reddit contribution (weight: 0.2)
    if reddit_data and reddit_data.get('total_mentions', 0) > 0:
        vs_baseline = reddit_data.get('vs_baseline', 'average')
        if "high" in vs_baseline.lower():
            reddit_score = 0.5
        elif "low" in vs_baseline.lower():
            reddit_score = -0.3
        else:
            reddit_score = 0
        scores.append(("social", reddit_score, 0.2))

    if not scores:
        return {
            "status": "insufficient data",
            "note": "Not enough sentiment data available for overall assessment"
        }

    # Calculate weighted average
    total_weight = sum(weight for _, _, weight in scores)
    weighted_sum = sum(score * weight for _, score, weight in scores)
    overall_score = weighted_sum / total_weight if total_weight > 0 else 0

    # Interpret overall sentiment
    if overall_score >= 0.4:
        assessment = "positive"
        description = "Multiple signals suggest positive sentiment"
    elif overall_score >= 0.1:
        assessment = "moderately positive"
        description = "Signals lean slightly positive"
    elif overall_score <= -0.4:
        assessment = "negative"
        description = "Multiple signals suggest negative sentiment"
    elif overall_score <= -0.1:
        assessment = "moderately negative"
        description = "Signals lean slightly negative"
    else:
        assessment = "neutral"
        description = "Mixed signals, no clear sentiment direction"

    return {
        "assessment": assessment,
        "score": round(overall_score, 2),
        "description": description,
        "signals_used": [name for name, _, _ in scores],
        "note": "Directional signal only - combines market, retail, and social sentiment",
        "caveat": "Sentiment is not predictive. Use as supporting context only."
    }

# Example usage and testing
if __name__ == "__main__":
    # Test with sample data
    sample_fg = {"value": 65, "classification": "Greed", "interpretation": "Market in greed territory"}
    sample_trends = {"current_interest": 45, "trend_direction": "rising", "change_pct_7d": 12}
    sample_reddit = {"total_mentions": 150, "vs_baseline": "elevated (1.5x+ average)", "subreddit_breakdown": {"wallstreetbets": 100, "stocks": 50}}

    print("Testing sentiment aggregation...")
    result = aggregate_sentiment("AAPL", sample_fg, sample_trends, sample_reddit)

    if result:
        print(f"\n✓ Sentiment Analysis:")
        print(f"  Market: {result['market_sentiment'].get('classification', 'N/A')}")
        print(f"  Retail Interest: {result['retail_interest'].get('interest_level', 'N/A')}")
        print(f"  Social: {result['social_signals'].get('vs_baseline', 'N/A')}")
        print(f"  Overall: {result['overall_sentiment'].get('assessment', 'N/A')}")
