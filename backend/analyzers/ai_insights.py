"""
AI Insights Generator for ResearchIQ
Uses Google Gemini to generate subtle, value-add analysis
Data Quality: AI-GENERATED - Educational context only
"""

import logging
import json
from typing import Optional, Dict, Any, List
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import (
    GEMINI_API_KEY,
    CONFIDENCE_AI,
    AI_MAX_RETRIES,
    AI_TIMEOUT_SECONDS,
    AI_CACHE_TTL_MINUTES
)
from utils.cache import generate_cache_key, get_cached, set_cache

# Import Gemini
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini AI configured successfully")
else:
    logger.warning("Gemini API key not found - AI insights will be unavailable")


def _call_gemini(prompt: str, temperature: float = 0.3) -> Optional[str]:
    """
    Call Gemini API with retry logic

    Args:
        prompt: Prompt to send to Gemini
        temperature: Creativity level (0.0-1.0, lower = more focused)

    Returns:
        str: AI response or None if failed
    """
    if not GEMINI_API_KEY:
        return None

    for attempt in range(AI_MAX_RETRIES):
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=500,  # Keep responses concise
                ),
                request_options={'timeout': AI_TIMEOUT_SECONDS}
            )

            if response and response.text:
                return response.text.strip()

        except Exception as e:
            logger.warning(f"Gemini API call failed (attempt {attempt + 1}/{AI_MAX_RETRIES}): {e}")

            if attempt < AI_MAX_RETRIES - 1:
                continue
            else:
                logger.error(f"All Gemini API attempts failed: {e}")
                return None

    return None


def generate_technical_insight(
    ticker: str,
    technical_data: Dict[str, Any],
    price_data: Dict[str, Any]
) -> Optional[str]:
    """
    Generate AI insight on technical analysis patterns

    Args:
        ticker: Ticker symbol
        technical_data: Technical analysis results
        price_data: Price data

    Returns:
        str: One-line technical insight or None
    """
    # Check cache first
    cache_key = generate_cache_key(ticker, "ai_technical", technical_data)
    cached = get_cached(cache_key)
    if cached:
        return cached

    try:
        rsi = technical_data.get('rsi', {})
        ma = technical_data.get('moving_averages', {})
        volume = technical_data.get('volume', {})
        overall_signal = technical_data.get('overall_signal', 'neutral')

        current_price = price_data.get('current_price', 0)
        price_change_pct = price_data.get('price_change_percent', 0)

        prompt = f"""You are a technical analysis AI assistant for an educational research tool.

Analyze this technical data and provide ONE specific, actionable observation (max 15 words):

Asset: {ticker}
Current Price: ${current_price} ({price_change_pct:+.2f}%)
RSI: {rsi.get('value', 'N/A')} ({rsi.get('signal', 'N/A')})
Moving Averages: {ma.get('position', {})}
Volume: {volume.get('status', 'N/A')}
Overall Signal: {overall_signal}

Focus on:
- Divergences or unusual patterns
- Cross-signal anomalies
- Notable momentum shifts
- Risk factors (overbought/oversold extremes)

Keep it:
- Specific and unique (not just restating the data)
- Educational tone (use "suggests" not "will")
- One sentence max
- NO investment advice

If nothing notable, return: null"""

        response = _call_gemini(prompt, temperature=0.2)

        if response and response.lower() not in ['null', 'none', 'n/a']:
            # Cache result
            set_cache(cache_key, response, ttl_minutes=AI_CACHE_TTL_MINUTES)
            return response

        return None

    except Exception as e:
        logger.error(f"Error generating technical insight: {e}")
        return None


def generate_news_sentiment(
    ticker: str,
    news_data: Optional[List[Dict[str, Any]]]
) -> Optional[Dict[str, Any]]:
    """
    Generate AI sentiment analysis from news headlines

    Args:
        ticker: Ticker symbol
        news_data: List of news headlines

    Returns:
        dict: Sentiment analysis with score and themes, or None
    """
    if not news_data or len(news_data) == 0:
        return None

    # Check cache
    headlines_snapshot = [h.get('title', '')[:50] for h in news_data[:5]]  # First 50 chars of top 5
    cache_key = generate_cache_key(ticker, "ai_news", headlines_snapshot)
    cached = get_cached(cache_key)
    if cached:
        return cached

    try:
        headlines = [article.get('title', '') for article in news_data[:10]]
        headlines_text = '\n'.join([f"{i+1}. {h}" for i, h in enumerate(headlines)])

        prompt = f"""You are a financial news sentiment analyzer for an educational research tool.

Analyze these news headlines about {ticker}:

{headlines_text}

Provide analysis as JSON:
{{
  "sentiment": "Positive" or "Neutral" or "Negative",
  "key_themes": ["theme1", "theme2"],  // Max 2 themes
  "notable_event": "one sentence about most important event or null"
}}

Focus on:
- Overall sentiment direction
- Main themes (earnings, products, legal, partnerships, etc.)
- Any notable/outlier events

Keep themes concise (2-3 words each). No investment advice."""

        response = _call_gemini(prompt, temperature=0.3)

        if response:
            # Try to parse JSON
            try:
                # Extract JSON from response (handle markdown code blocks)
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    result = json.loads(json_str)

                    # Cache result
                    set_cache(cache_key, result, ttl_minutes=AI_CACHE_TTL_MINUTES)
                    return result
            except json.JSONDecodeError as e:
                logger.warning(f"Could not parse Gemini JSON response: {e}")

        return None

    except Exception as e:
        logger.error(f"Error generating news sentiment: {e}")
        return None


def generate_cross_signal_analysis(
    ticker: str,
    technical_data: Dict[str, Any],
    sentiment_data: Dict[str, Any],
    price_data: Dict[str, Any]
) -> Optional[List[str]]:
    """
    Generate AI cross-signal analysis combining all data sources

    This is the KEY value-add: AI spots contradictions and anomalies
    across multiple data sources that pure math misses.

    Args:
        ticker: Ticker symbol
        technical_data: Technical analysis
        sentiment_data: Sentiment analysis
        price_data: Price data

    Returns:
        list: 2-3 key insights or None
    """
    # Check cache
    cache_snapshot = {
        'tech': technical_data.get('overall_signal'),
        'sent': sentiment_data.get('overall_sentiment', {}).get('assessment'),
        'price': price_data.get('price_change_percent')
    }
    cache_key = generate_cache_key(ticker, "ai_cross_signal", cache_snapshot)
    cached = get_cached(cache_key)
    if cached:
        return cached

    try:
        # Extract key data points
        rsi = technical_data.get('rsi', {}).get('value', 50)
        tech_signal = technical_data.get('overall_signal', 'neutral')
        volume_status = technical_data.get('volume', {}).get('status', 'average')

        fg_value = sentiment_data.get('market_sentiment', {}).get('value', 50)
        fg_class = sentiment_data.get('market_sentiment', {}).get('classification', 'Neutral')
        reddit_mentions = sentiment_data.get('social_signals', {}).get('total_mentions', 0)
        reddit_vs_baseline = sentiment_data.get('social_signals', {}).get('vs_baseline', 'average')
        overall_sentiment = sentiment_data.get('overall_sentiment', {}).get('assessment', 'neutral')

        current_price = price_data.get('current_price', 0)
        price_change = price_data.get('price_change_percent', 0)

        prompt = f"""You are an AI co-analyst for an educational investment research tool.

Analyze this data for {ticker} and identify 2-3 specific, notable insights:

TECHNICAL:
- Signal: {tech_signal}
- RSI: {rsi}
- Volume: {volume_status}

SENTIMENT:
- Overall: {overall_sentiment}
- Fear & Greed: {fg_value} ({fg_class})
- Reddit mentions: {reddit_mentions} ({reddit_vs_baseline})

PRICE:
- Current: ${current_price}
- Change: {price_change:+.2f}%

Your task: Identify CROSS-SIGNAL patterns and anomalies:
- Divergences (tech says X, sentiment says Y)
- Unusual combinations (e.g., bullish tech + extreme greed = risk)
- Social media spikes (potential FOMO/volatility)
- Risk factors that pure math misses

Provide 2-3 insights as JSON array:
["Insight 1 (max 20 words)", "Insight 2", "Insight 3"]

Requirements:
- Each insight must be specific and actionable
- Focus on what's UNUSUAL or noteworthy
- Use educational language ("data suggests", "indicates")
- NO generic statements
- NO investment advice
- If nothing notable, return: []"""

        response = _call_gemini(prompt, temperature=0.4)

        if response:
            try:
                # Extract JSON array
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    insights = json.loads(json_str)

                    if isinstance(insights, list) and len(insights) > 0:
                        # Cache result
                        set_cache(cache_key, insights, ttl_minutes=AI_CACHE_TTL_MINUTES)
                        return insights

            except json.JSONDecodeError as e:
                logger.warning(f"Could not parse cross-signal JSON: {e}")

        return None

    except Exception as e:
        logger.error(f"Error generating cross-signal analysis: {e}")
        return None


def generate_price_momentum_insight(
    ticker: str,
    price_data: Dict[str, Any],
    technical_data: Dict[str, Any]
) -> Optional[str]:
    """Generate insight about price momentum and trend strength"""
    cache_key = generate_cache_key(ticker, "ai_momentum", price_data)
    cached = get_cached(cache_key)
    if cached:
        return cached

    try:
        price_change = price_data.get('price_change_percent', 0)
        rsi = technical_data.get('rsi', {}).get('value', 50)
        volume_status = technical_data.get('volume', {}).get('status', 'average')

        prompt = f"""Analyze price momentum for {ticker}:
- Price change: {price_change:+.2f}%
- RSI: {rsi}
- Volume: {volume_status}

Provide ONE specific momentum insight (max 15 words). Focus on trend strength, exhaustion signals, or momentum divergences. Use "suggests" not "will". Return null if nothing notable."""

        response = _call_gemini(prompt, temperature=0.2)
        if response and response.lower() not in ['null', 'none']:
            set_cache(cache_key, response, ttl_minutes=AI_CACHE_TTL_MINUTES)
            return response
        return None
    except:
        return None

def generate_support_resistance_insight(
    ticker: str,
    price_data: Dict[str, Any],
    technical_data: Dict[str, Any]
) -> Optional[str]:
    """Generate insight about support/resistance levels"""
    cache_key = generate_cache_key(ticker, "ai_levels", price_data)
    cached = get_cached(cache_key)
    if cached:
        return cached

    try:
        current = price_data.get('current_price', 0)
        ma_values = technical_data.get('moving_averages', {}).get('values', {})

        prompt = f"""Identify support/resistance for {ticker}:
- Current: ${current}
- MA20: {ma_values.get('MA_20', 'N/A')}
- MA50: {ma_values.get('MA_50', 'N/A')}

Provide ONE specific insight about key levels (max 15 words). Focus on nearby support/resistance or breakout levels. Educational tone. Return null if nothing notable."""

        response = _call_gemini(prompt, temperature=0.2)
        if response and response.lower() not in ['null', 'none']:
            set_cache(cache_key, response, ttl_minutes=AI_CACHE_TTL_MINUTES)
            return response
        return None
    except:
        return None

def generate_volume_anomaly_insight(
    ticker: str,
    technical_data: Dict[str, Any]
) -> Optional[str]:
    """Generate insight about volume anomalies"""
    cache_key = generate_cache_key(ticker, "ai_volume", technical_data)
    cached = get_cached(cache_key)
    if cached:
        return cached

    try:
        volume = technical_data.get('volume', {})
        status = volume.get('status', 'average')
        vs_avg_pct = volume.get('vs_average_pct', 0)

        prompt = f"""Analyze volume for {ticker}:
- Status: {status}
- vs Average: {vs_avg_pct:+.1f}%

Provide ONE specific insight about volume (max 15 words). Focus on unusual patterns, conviction signals, or liquidity concerns. Return null if nothing notable."""

        response = _call_gemini(prompt, temperature=0.2)
        if response and response.lower() not in ['null', 'none']:
            set_cache(cache_key, response, ttl_minutes=AI_CACHE_TTL_MINUTES)
            return response
        return None
    except:
        return None

def generate_risk_assessment_insight(
    ticker: str,
    risk_data: Optional[Dict[str, Any]],
    options_data: Optional[Dict[str, Any]]
) -> Optional[str]:
    """Generate insight about risk factors"""
    if not risk_data and not options_data:
        return None

    cache_key = generate_cache_key(ticker, "ai_risk", {**({'risk': risk_data} if risk_data else {}), **({'options': options_data} if options_data else {})})
    cached = get_cached(cache_key)
    if cached:
        return cached

    try:
        risk_level = risk_data.get('risk_level', 'N/A') if risk_data else 'N/A'
        volatility = risk_data.get('volatility_30d', 'N/A') if risk_data else 'N/A'
        put_call = options_data.get('put_call_ratio', 'N/A') if options_data else 'N/A'

        prompt = f"""Assess risk for {ticker}:
- Risk Level: {risk_level}
- 30d Volatility: {volatility}%
- Put/Call Ratio: {put_call}

Provide ONE specific risk insight (max 15 words). Focus on notable risk factors or hedging activity. Educational tone. Return null if nothing notable."""

        response = _call_gemini(prompt, temperature=0.2)
        if response and response.lower() not in ['null', 'none']:
            set_cache(cache_key, response, ttl_minutes=AI_CACHE_TTL_MINUTES)
            return response
        return None
    except:
        return None

async def generate_ai_insights(
    ticker: str,
    price_data: Dict[str, Any],
    technical_data: Optional[Dict[str, Any]],
    sentiment_data: Dict[str, Any],
    news_data: Optional[List[Dict[str, Any]]],
    risk_data: Optional[Dict[str, Any]] = None,
    options_data: Optional[Dict[str, Any]] = None,
    insider_data: Optional[Dict[str, Any]] = None,
    institutional_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate all AI insights for the report (expanded to 6-7 insights)

    Args:
        ticker: Ticker symbol
        price_data: Price data
        technical_data: Technical analysis
        sentiment_data: Sentiment analysis
        news_data: News headlines
        risk_data: Risk metrics (new)
        options_data: Options sentiment (new)
        insider_data: Insider trading (new)
        institutional_data: Institutional ownership (new)

    Returns:
        dict: AI insights with all components
    """
    try:
        logger.info(f"Generating enhanced AI insights for {ticker}...")

        result = {
            "confidence": CONFIDENCE_AI,
            "disclaimer": "AI-generated insights for educational purposes only. Not financial advice.",
            "technical_insight": None,
            "news_sentiment": None,
            "cross_signal_analysis": None,
            "price_momentum_insight": None,
            "support_resistance_insight": None,
            "volume_anomaly_insight": None,
            "risk_assessment_insight": None
        }

        # Generate all insights (existing + new)
        if technical_data:
            result["technical_insight"] = generate_technical_insight(ticker, technical_data, price_data)
            result["price_momentum_insight"] = generate_price_momentum_insight(ticker, price_data, technical_data)
            result["support_resistance_insight"] = generate_support_resistance_insight(ticker, price_data, technical_data)
            result["volume_anomaly_insight"] = generate_volume_anomaly_insight(ticker, technical_data)

        if news_data and len(news_data) > 0:
            result["news_sentiment"] = generate_news_sentiment(ticker, news_data)

        if technical_data:
            result["cross_signal_analysis"] = generate_cross_signal_analysis(ticker, technical_data, sentiment_data, price_data)

        # New risk assessment insight
        result["risk_assessment_insight"] = generate_risk_assessment_insight(ticker, risk_data, options_data)

        logger.info(f"Enhanced AI insights generated for {ticker}")
        return result

    except Exception as e:
        logger.error(f"Error generating AI insights for {ticker}: {e}")
        return {
            "confidence": CONFIDENCE_AI,
            "status": "unavailable",
            "error": "AI insights could not be generated",
            "disclaimer": "AI analysis unavailable. Report contains traditional analysis only."
        }


# Example usage and testing
if __name__ == "__main__":
    import asyncio

    print("Testing AI insights generation...")

    # Sample data
    sample_price = {
        "current_price": 178.25,
        "price_change_percent": 2.15
    }

    sample_technical = {
        "rsi": {"value": 68, "signal": "bullish"},
        "moving_averages": {
            "position": {"MA_20": "above", "MA_50": "above", "MA_200": "below"}
        },
        "volume": {"status": "elevated"},
        "overall_signal": "bullish momentum"
    }

    sample_sentiment = {
        "market_sentiment": {"value": 75, "classification": "Greed"},
        "social_signals": {
            "total_mentions": 450,
            "vs_baseline": "high (3x+ average)"
        },
        "overall_sentiment": {"assessment": "positive"}
    }

    sample_news = [
        {"title": "Apple announces record iPhone sales"},
        {"title": "AAPL stock price surges on earnings beat"},
    ]

    async def test():
        insights = await generate_ai_insights(
            "AAPL",
            sample_price,
            sample_technical,
            sample_sentiment,
            sample_news
        )
        print(f"\n✓ AI Insights Generated:")
        print(f"  Technical: {insights.get('technical_insight')}")
        print(f"  News Sentiment: {insights.get('news_sentiment')}")
        print(f"  Cross-Signal: {insights.get('cross_signal_analysis')}")

    asyncio.run(test())
