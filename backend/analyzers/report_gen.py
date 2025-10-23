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
    ai_insights: Optional[Dict[str, Any]] = None,
    risk_data: Optional[Dict[str, Any]] = None,
    options_data: Optional[Dict[str, Any]] = None,
    insider_data: Optional[Dict[str, Any]] = None,
    institutional_data: Optional[Dict[str, Any]] = None
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
        risk_data: Risk metrics (volatility, beta, etc.)
        options_data: Options sentiment (put/call ratio)
        insider_data: Insider trading activity
        institutional_data: Institutional ownership

    Returns:
        dict: Complete report data ready for frontend/PDF
    """
    try:
        logger.info(f"Generating report for {ticker}")

        # Build report structure
        report = {
            "metadata": _build_metadata(ticker, price_data),
            "technical_analysis": _format_technical(technical_analysis),
            "risk_metrics": _format_risk(risk_data),
            "options_sentiment": _format_options(options_data),
            "institutional_ownership": _format_institutional(institutional_data),
            "insider_trading": _format_insider(insider_data),
            "sentiment_analysis": _format_sentiment(sentiment_analysis),
            "news_headlines": _format_news(news_data),
            "ai_insights": _format_ai_insights(ai_insights),
            "summary": _generate_summary(ticker, price_data, technical_analysis, sentiment_analysis, risk_data),
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
        "price_momentum_insight": ai_insights.get('price_momentum_insight'),
        "support_resistance_insight": ai_insights.get('support_resistance_insight'),
        "volume_anomaly_insight": ai_insights.get('volume_anomaly_insight'),
        "news_sentiment": ai_insights.get('news_sentiment'),
        "cross_signal_analysis": ai_insights.get('cross_signal_analysis'),
        "risk_assessment_insight": ai_insights.get('risk_assessment_insight'),
        "disclaimer": ai_insights.get('disclaimer', 'AI-generated insights for educational purposes only.')
    }

def _format_risk(risk_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Format risk metrics section"""
    if not risk_data:
        return {
            "confidence": "UNAVAILABLE",
            "status": "unavailable",
            "note": "Risk metrics data not available for this asset"
        }

    return {
        "confidence": risk_data.get('confidence', 'HIGH'),
        "status": "available",
        "volatility_30d": risk_data.get('volatility_30d'),
        "volatility_90d": risk_data.get('volatility_90d'),
        "beta": risk_data.get('beta'),
        "high_52w": risk_data.get('high_52w'),
        "low_52w": risk_data.get('low_52w'),
        "pct_from_high": risk_data.get('pct_from_high'),
        "pct_from_low": risk_data.get('pct_from_low'),
        "risk_score": risk_data.get('risk_score'),
        "risk_level": risk_data.get('risk_level')
    }

def _format_options(options_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Format options sentiment section"""
    if not options_data:
        return {
            "confidence": "UNAVAILABLE",
            "status": "unavailable",
            "note": "Options data not available for this asset (may not have listed options)"
        }

    return {
        "confidence": options_data.get('confidence', 'MEDIUM'),
        "status": "available",
        "put_call_ratio": options_data.get('put_call_ratio'),
        "sentiment": options_data.get('sentiment'),
        "interpretation": options_data.get('interpretation'),
        "call_volume": options_data.get('call_volume'),
        "put_volume": options_data.get('put_volume'),
        "expiration": options_data.get('expiration')
    }

def _format_institutional(institutional_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Format institutional ownership section"""
    if not institutional_data:
        return {
            "confidence": "UNAVAILABLE",
            "status": "unavailable",
            "note": "Institutional ownership data not available for this asset"
        }

    return {
        "confidence": institutional_data.get('confidence', 'MEDIUM'),
        "status": "available",
        "total_institutional_shares": institutional_data.get('total_institutional_shares'),
        "top_holders": institutional_data.get('top_holders', []),
        "holder_count": institutional_data.get('holder_count')
    }

def _format_insider(insider_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Format insider trading section"""
    if not insider_data:
        return {
            "confidence": "UNAVAILABLE",
            "status": "unavailable",
            "note": "Insider trading data not available for this asset"
        }

    return {
        "confidence": insider_data.get('confidence', 'MEDIUM'),
        "status": "available",
        "buy_transactions": insider_data.get('buy_transactions'),
        "sell_transactions": insider_data.get('sell_transactions'),
        "buy_value": insider_data.get('buy_value'),
        "sell_value": insider_data.get('sell_value'),
        "sentiment": insider_data.get('sentiment'),
        "interpretation": insider_data.get('interpretation'),
        "note": insider_data.get('note', '')
    }

def _generate_summary(
    ticker: str,
    price_data: Dict[str, Any],
    technical: Optional[Dict[str, Any]],
    sentiment: Dict[str, Any],
    risk_data: Optional[Dict[str, Any]] = None
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

    # Risk summary
    if risk_data:
        risk_level = risk_data.get('risk_level', 'Unknown')
        volatility = risk_data.get('volatility_30d', 0)
        parts.append(
            f"Risk assessment: {risk_level} ({volatility:.1f}% annualized volatility)."
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
        "This analysis combines technical indicators, risk metrics, and public sentiment data for research purposes only."
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
