"""
yfinance Data Collector for ResearchIQ
Fetches price, volume, and company info from Yahoo Finance
Data Quality: HIGH - Real market data from established source
"""

import yfinance as yf
import pandas as pd
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_price_data(ticker: str, period: str = "3mo") -> Optional[Dict[str, Any]]:
    """
    Get historical price and volume data for a ticker

    Args:
        ticker: Stock ticker symbol (e.g., AAPL, BTC-USD, ^GSPC)
        period: Time period for historical data (default: 3mo)
                Options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

    Returns:
        dict: Price data including:
            - history: DataFrame with OHLCV data
            - current_price: Latest closing price
            - company_name: Full company/asset name
            - info: Additional asset information
        None if error occurs

    Data Quality: HIGH
    - Direct from Yahoo Finance
    - Reliable price and volume data
    - Suitable for technical analysis
    """
    try:
        logger.info(f"Fetching price data for {ticker}")

        # Create ticker object
        stock = yf.Ticker(ticker)

        # Get historical data
        hist = stock.history(period=period)

        if hist.empty:
            logger.error(f"No price data found for {ticker}")
            return None

        # Get asset info
        info = stock.info

        # Extract company/asset name
        company_name = info.get('longName') or info.get('shortName') or ticker

        # Get current price (latest close)
        current_price = float(hist['Close'].iloc[-1])

        # Get previous close for change calculation
        prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
        price_change = current_price - prev_close
        price_change_pct = (price_change / prev_close * 100) if prev_close != 0 else 0

        result = {
            "ticker": ticker,
            "company_name": company_name,
            "current_price": round(current_price, 2),
            "price_change": round(price_change, 2),
            "price_change_percent": round(price_change_pct, 2),
            "currency": info.get('currency', 'USD'),
            "history": hist,  # Full DataFrame for technical analysis
            "volume_current": int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0,
            "market_cap": info.get('marketCap'),
            "sector": info.get('sector'),
            "industry": info.get('industry'),
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"Successfully fetched data for {ticker}: ${current_price}")
        return result

    except Exception as e:
        logger.error(f"Error fetching price data for {ticker}: {str(e)}")
        return None

def get_ticker_info(ticker: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a ticker

    Args:
        ticker: Stock ticker symbol

    Returns:
        dict: Asset information or None if error
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "ticker": ticker,
            "name": info.get('longName') or info.get('shortName') or ticker,
            "sector": info.get('sector'),
            "industry": info.get('industry'),
            "description": info.get('longBusinessSummary', ''),
            "website": info.get('website'),
            "market_cap": info.get('marketCap'),
            "employees": info.get('fullTimeEmployees')
        }
    except Exception as e:
        logger.error(f"Error fetching info for {ticker}: {str(e)}")
        return None

def validate_ticker(ticker: str) -> bool:
    """
    Validate if a ticker symbol exists and has data

    Args:
        ticker: Ticker symbol to validate

    Returns:
        bool: True if ticker is valid, False otherwise
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        return not hist.empty
    except:
        return False

# Example usage and testing
if __name__ == "__main__":
    # Test with stock
    print("Testing AAPL...")
    aapl_data = get_price_data("AAPL")
    if aapl_data:
        print(f"✓ {aapl_data['company_name']}: ${aapl_data['current_price']}")

    # Test with crypto
    print("\nTesting BTC-USD...")
    btc_data = get_price_data("BTC-USD")
    if btc_data:
        print(f"✓ {btc_data['company_name']}: ${btc_data['current_price']}")

    # Test with index
    print("\nTesting ^GSPC...")
    spy_data = get_price_data("^GSPC")
    if spy_data:
        print(f"✓ {spy_data['company_name']}: ${spy_data['current_price']}")
