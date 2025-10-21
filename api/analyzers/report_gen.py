"""
Report Generation Module for ResearchIQ
Formats all analysis data into structured report
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
import sys
import os

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import APP_NAME, APP_VERSION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_report_data(
    ticker: str,
    price_data: Dict[str, Any],
    technical_analysis: Optional[Dict[str, Any]],
    sentiment_analysis: Dict[str, Any],
    news_data: Optional[list],
    ai_insights: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate complete structured report from all analysis components

    Args:
        ticker: Ticker symbol
        price_data: Price data from yfinance
        technical_analysis: Technical indicators analysis
        sentiment_analysis: Aggregated sentiment
        news_data: News headlines
        ai_insights: AI-generated insights (optional)

    Returns:
        dict: Complete report data ready for frontend/PDF
    """
    try:
        logger.info(f"Generating report for {ticker}")

        # Build report structure
        report = {
            "metadata": _build_metadata(ticker, price_data),
            "technical_analysis": _format_technical(technical_analysis),
            "sentiment_analysis": _format_sentiment(sentiment_analysis),
            "news_headlines": _format_news(news_data),
            "ai_insights": _format_ai_insights(ai_insights),
            "summary": _generate_summary(ticker, price_data, technical_analysis, sentiment_analysis),
            "disclaimer": _get_disclaimer(),
            "generated_at": datetime.now().isoformat(),
            "app_info": {
                "name": APP_NAME,
                "version": APP_VERSION
            }
        }

        logger.info(f"Report generated successfully for {ticker}")
        return report

    except Exception as e:
        logger.error(f"Error generating report for {ticker}: {str(e)}")
        raise

def _build_metadata(ticker: str, price_data: Dict[str, Any]) -> Dict[str, Any]:
    """Build report metadata section"""
    return {
        "ticker": ticker,
        "company_name": price_data.get('company_name', ticker),
        "current_price": price_data.get('current_price', 0),
        "price_change": price_data.get('price_change', 0),
        "price_change_percent": price_data.get('price_change_percent', 0),
        "currency": price_data.get('currency', 'USD'),
        "market_cap": price_data.get('market_cap'),
        "sector": price_data.get('sector'),
        "industry": price_data.get('industry'),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

def _format_technical(technical: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Format technical analysis section"""
    if not technical:
        return {
            "confidence": "UNAVAILABLE",
            "status": "Technical analysis data not available",
            "data": None
        }

    return {
        "confidence": technical.get('confidence', 'HIGH'),
        "rsi": technical.get('rsi', {}),
        "moving_averages": technical.get('moving_averages', {}),
        "volume": technical.get('volume', {}),
        "overall_signal": technical.get('overall_signal', 'neutral'),
        "data_quality_note": technical.get('data_quality_note', ''),
        "disclaimer": technical.get('disclaimer', '')
    }

def _format_sentiment(sentiment: Dict[str, Any]) -> Dict[str, Any]:
    """Format sentiment analysis section"""
    return {
        "market_sentiment": {
            "data": sentiment.get('market_sentiment', {}),
            "confidence": sentiment.get('market_sentiment', {}).get('confidence', 'MEDIUM')
        },
        "retail_interest": {
            "data": sentiment.get('retail_interest', {}),
            "confidence": sentiment.get('retail_interest', {}).get('confidence', 'MEDIUM')
        },
        "social_signals": {
            "data": sentiment.get('social_signals', {}),
            "confidence": sentiment.get('social_signals', {}).get('confidence', 'LOW')
        },
        "overall_sentiment": sentiment.get('overall_sentiment', {}),
        "disclaimer": sentiment.get('disclaimer', '')
    }

def _format_news(news_data: Optional[list]) -> Dict[str, Any]:
    """Format news headlines section"""
    if not news_data:
        return {
            "confidence": "CONTEXT ONLY",
            "status": "limited",
            "headlines": [],
            "note": "News data unavailable or limited by API constraints"
        }

    # Format headlines
    formatted_headlines = []
    for article in news_data[:10]:  # Limit to 10 headlines
        formatted_headlines.append({
            "title": article.get('title', 'No title'),
            "source": article.get('source', 'Unknown'),
            "published_at": article.get('published_at', ''),
            "url": article.get('url', '')
        })

    return {
        "confidence": "CONTEXT ONLY",
        "status": "available",
        "headlines": formatted_headlines,
        "count": len(formatted_headlines),
        "note": "Limited coverage - free tier API constraints. For context only."
    }

def _format_ai_insights(ai_insights: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Format AI insights section"""
    if not ai_insights or ai_insights.get('status') == 'unavailable':
        return {
            "confidence": "AI-GENERATED",
            "status": "unavailable",
            "note": "AI insights could not be generated. Report contains traditional analysis only."
        }

    return {
        "confidence": ai_insights.get('confidence', 'AI-GENERATED'),
        "status": "available",
        "technical_insight": ai_insights.get('technical_insight'),
        "news_sentiment": ai_insights.get('news_sentiment'),
        "cross_signal_analysis": ai_insights.get('cross_signal_analysis'),
        "disclaimer": ai_insights.get('disclaimer', 'AI-generated insights for educational purposes only.')
    }

def _generate_summary(
    ticker: str,
    price_data: Dict[str, Any],
    technical: Optional[Dict[str, Any]],
    sentiment: Dict[str, Any]
) -> str:
    """
    Generate executive summary paragraph

    Returns:
        str: Natural language summary of analysis
    """
    company_name = price_data.get('company_name', ticker)
    current_price = price_data.get('current_price', 0)
    price_change_pct = price_data.get('price_change_percent', 0)

    # Build summary components
    parts = []

    # Price info
    direction = "up" if price_change_pct > 0 else "down"
    parts.append(
        f"{company_name} ({ticker}) is trading at ${current_price:.2f}, "
        f"{direction} {abs(price_change_pct):.2f}%."
    )

    # Technical summary
    if technical:
        rsi_value = technical.get('rsi', {}).get('value', 50)
        overall_signal = technical.get('overall_signal', 'neutral')
        parts.append(
            f"Technical indicators show {overall_signal} with RSI at {rsi_value:.1f}."
        )

    # Sentiment summary
    overall_sentiment = sentiment.get('overall_sentiment', {})
    if overall_sentiment and 'assessment' in overall_sentiment:
        sentiment_assessment = overall_sentiment['assessment']
        parts.append(
            f"Sentiment analysis suggests {sentiment_assessment} signals from market and retail data."
        )

    # Caveat
    parts.append(
        "This analysis combines technical indicators with public sentiment data for research purposes only."
    )

    return " ".join(parts)

def _get_disclaimer() -> Dict[str, Any]:
    """Get comprehensive disclaimer"""
    return {
        "title": "Important Disclaimer",
        "sections": [
            {
                "heading": "Educational Purpose Only",
                "content": "ResearchIQ is an educational research tool built as a portfolio project. This is NOT financial advice, investment recommendations, or a professional analysis service."
            },
            {
                "heading": "Data Limitations",
                "content": "This tool uses free public APIs with known constraints. Data quality varies by source. Technical analysis is HIGH confidence (real market data), while sentiment signals are MEDIUM to LOW confidence (directional only)."
            },
            {
                "heading": "Not Suitable for Investment Decisions",
                "content": "The analysis provided is for research and educational purposes only. It should not be used as the basis for actual investment decisions."
            },
            {
                "heading": "No Warranty",
                "content": "This tool is provided as-is with no warranty of accuracy, completeness, or fitness for any purpose. Use at your own risk."
            },
            {
                "heading": "Consult Professionals",
                "content": "For investment decisions, consult licensed financial professionals. Past performance does not guarantee future results."
            }
        ]
    }

# Example usage and testing
if __name__ == "__main__":
    # Test with sample data
    sample_price = {
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "current_price": 178.25,
        "price_change": 2.15,
        "price_change_percent": 1.22,
        "currency": "USD"
    }

    sample_technical = {
        "confidence": "HIGH",
        "rsi": {"value": 62.5, "signal": "bullish"},
        "moving_averages": {"values": {"MA_20": 175.0, "MA_50": 172.0}},
        "volume": {"status": "above average"},
        "overall_signal": "bullish momentum"
    }

    sample_sentiment = {
        "market_sentiment": {"classification": "Greed", "confidence": "MEDIUM"},
        "retail_interest": {"interest_level": "high", "confidence": "MEDIUM"},
        "social_signals": {"vs_baseline": "elevated", "confidence": "LOW"},
        "overall_sentiment": {"assessment": "moderately positive"}
    }

    sample_news = [
        {"title": "Apple announces new product", "source": "TechCrunch", "published_at": "2025-10-21"}
    ]

    print("Testing report generation...")
    report = generate_report_data("AAPL", sample_price, sample_technical, sample_sentiment, sample_news)

    if report:
        print(f"\n✓ Report Generated:")
        print(f"  Ticker: {report['metadata']['ticker']}")
        print(f"  Price: ${report['metadata']['current_price']}")
        print(f"  Technical Signal: {report['technical_analysis']['overall_signal']}")
        print(f"  Sentiment: {report['sentiment_analysis']['overall_sentiment'].get('assessment', 'N/A')}")
        print(f"  News: {report['news_headlines']['count']} headlines")
        print(f"\nSummary: {report['summary']}")
