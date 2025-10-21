"""
Technical Analysis Engine for ResearchIQ
Calculates technical indicators from price data
Data Quality: HIGH - Calculated from real market data
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional, Dict, Any
import sys
import os

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import RSI_PERIOD, MA_PERIODS, VOLUME_LOOKBACK_DAYS, CONFIDENCE_HIGH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_rsi(prices: pd.Series, period: int = RSI_PERIOD) -> float:
    """
    Calculate Relative Strength Index (RSI)

    Args:
        prices: Series of closing prices
        period: RSI period (default: 14)

    Returns:
        float: RSI value (0-100)
    """
    # Calculate price changes
    delta = prices.diff()

    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)

    # Calculate average gains and losses
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()

    # Calculate RS and RSI
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))

    return float(rsi.iloc[-1])

def calculate_moving_averages(prices: pd.Series, periods: list = MA_PERIODS) -> Dict[str, float]:
    """
    Calculate multiple moving averages

    Args:
        prices: Series of closing prices
        periods: List of periods to calculate (default: [20, 50, 200])

    Returns:
        dict: Moving averages {period: value}
    """
    mas = {}
    for period in periods:
        if len(prices) >= period:
            ma = prices.rolling(window=period).mean().iloc[-1]
            mas[f"MA_{period}"] = round(float(ma), 2)
        else:
            mas[f"MA_{period}"] = None

    return mas

def analyze_volume(volume_series: pd.Series, lookback_days: int = VOLUME_LOOKBACK_DAYS) -> Dict[str, Any]:
    """
    Analyze volume trends

    Args:
        volume_series: Series of volume data
        lookback_days: Number of days to analyze

    Returns:
        dict: Volume analysis
    """
    if len(volume_series) < 2:
        return {
            "current_volume": 0,
            "avg_volume": 0,
            "status": "insufficient data"
        }

    # Get recent volume
    recent_volume = volume_series.iloc[-lookback_days:] if len(volume_series) >= lookback_days else volume_series

    current_volume = int(volume_series.iloc[-1])
    avg_volume = int(recent_volume.mean())

    # Determine status
    if current_volume > avg_volume * 1.5:
        status = "elevated (high activity)"
    elif current_volume > avg_volume * 1.2:
        status = "above average"
    elif current_volume < avg_volume * 0.8:
        status = "below average"
    else:
        status = "average"

    return {
        "current_volume": current_volume,
        "avg_volume": avg_volume,
        "status": status,
        "vs_average_pct": round(((current_volume - avg_volume) / avg_volume * 100), 1) if avg_volume > 0 else 0
    }

def get_momentum_signal(rsi: float, current_price: float, mas: Dict[str, float]) -> str:
    """
    Determine overall momentum signal from indicators

    Args:
        rsi: RSI value
        current_price: Current price
        mas: Moving averages dict

    Returns:
        str: Overall signal (bullish, bearish, neutral)
    """
    signals = []

    # RSI signal
    if rsi > 70:
        signals.append("overbought")
    elif rsi > 55:
        signals.append("bullish")
    elif rsi < 30:
        signals.append("oversold")
    elif rsi < 45:
        signals.append("bearish")
    else:
        signals.append("neutral")

    # Moving average signals
    ma_signals = 0
    for key, ma_value in mas.items():
        if ma_value is not None:
            if current_price > ma_value:
                ma_signals += 1
            else:
                ma_signals -= 1

    # Overall assessment
    if "overbought" in signals:
        overall = "overbought (approaching resistance)"
    elif "oversold" in signals:
        overall = "oversold (approaching support)"
    elif ma_signals >= 2 and "bullish" in signals:
        overall = "bullish momentum"
    elif ma_signals <= -2 and "bearish" in signals:
        overall = "bearish momentum"
    elif ma_signals >= 1:
        overall = "moderate bullish"
    elif ma_signals <= -1:
        overall = "moderate bearish"
    else:
        overall = "neutral"

    return overall

def analyze_technical(price_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Perform complete technical analysis on price data

    Args:
        price_data: Price data dict from yfinance_api.get_price_data()

    Returns:
        dict: Complete technical analysis including:
            - rsi: RSI analysis
            - moving_averages: MA analysis
            - volume: Volume analysis
            - overall_signal: Momentum assessment
            - confidence: Data quality level
        None if insufficient data

    Data Quality: HIGH
    - Calculated from real price data
    - Standard technical indicators
    - Reliable for momentum assessment
    - NOT predictive, descriptive only
    """
    try:
        if not price_data or 'history' not in price_data:
            logger.error("Invalid price data for technical analysis")
            return None

        hist = price_data['history']

        if len(hist) < 20:
            logger.warning("Insufficient price history for technical analysis")
            return None

        # Extract data
        prices = hist['Close']
        volume = hist['Volume'] if 'Volume' in hist.columns else pd.Series([0])

        # Calculate indicators
        rsi = calculate_rsi(prices)
        mas = calculate_moving_averages(prices)
        volume_analysis = analyze_volume(volume)

        # Get current price
        current_price = price_data.get('current_price', prices.iloc[-1])

        # Overall momentum signal
        momentum = get_momentum_signal(rsi, current_price, mas)

        # RSI interpretation
        if rsi >= 70:
            rsi_signal = "overbought"
            rsi_interpretation = "May face selling pressure, consider overbought"
        elif rsi >= 60:
            rsi_signal = "bullish"
            rsi_interpretation = "Strong bullish momentum"
        elif rsi >= 40:
            rsi_signal = "neutral"
            rsi_interpretation = "Balanced momentum, no strong trend"
        elif rsi >= 30:
            rsi_signal = "bearish"
            rsi_interpretation = "Weak momentum, bearish bias"
        else:
            rsi_signal = "oversold"
            rsi_interpretation = "May find support, consider oversold"

        # MA position analysis
        ma_position = {}
        for key, value in mas.items():
            if value is not None:
                if current_price > value:
                    ma_position[key] = "above"
                else:
                    ma_position[key] = "below"
            else:
                ma_position[key] = "N/A"

        result = {
            "rsi": {
                "value": round(rsi, 2),
                "signal": rsi_signal,
                "interpretation": rsi_interpretation
            },
            "moving_averages": {
                "values": mas,
                "position": ma_position,
                "current_price": round(current_price, 2)
            },
            "volume": volume_analysis,
            "overall_signal": momentum,
            "confidence": CONFIDENCE_HIGH,
            "data_quality_note": "Calculated from real market data - reliable technical indicators",
            "disclaimer": "Technical analysis is descriptive, not predictive. Past performance does not guarantee future results."
        }

        logger.info(f"Technical analysis complete: RSI={rsi:.1f}, Momentum={momentum}")
        return result

    except Exception as e:
        logger.error(f"Error in technical analysis: {str(e)}")
        return None

# Example usage and testing
if __name__ == "__main__":
    # This would normally be called with data from yfinance_api
    # Test data structure
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from data_sources.yfinance_api import get_price_data

    print("Testing technical analysis with AAPL...")
    price_data = get_price_data("AAPL")

    if price_data:
        analysis = analyze_technical(price_data)
        if analysis:
            print(f"\n✓ Technical Analysis Results:")
            print(f"  RSI: {analysis['rsi']['value']} ({analysis['rsi']['signal']})")
            print(f"  Moving Averages: {analysis['moving_averages']['values']}")
            print(f"  Volume: {analysis['volume']['status']}")
            print(f"  Overall: {analysis['overall_signal']}")
        else:
            print("✗ Analysis failed")
    else:
        print("✗ Could not fetch price data")
