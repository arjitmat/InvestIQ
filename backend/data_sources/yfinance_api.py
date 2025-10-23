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

def get_options_sentiment(ticker: str) -> Optional[Dict[str, Any]]:
    """
    Get options market sentiment via Put/Call ratio

    Args:
        ticker: Stock ticker symbol

    Returns:
        dict: Options sentiment data including put/call ratio
        None if options data unavailable
    """
    try:
        logger.info(f"Fetching options sentiment for {ticker}")
        stock = yf.Ticker(ticker)

        # Get options expirations
        expirations = stock.options
        if not expirations or len(expirations) == 0:
            logger.warning(f"No options data available for {ticker}")
            return None

        # Get nearest expiration
        nearest_exp = expirations[0]
        opt_chain = stock.option_chain(nearest_exp)

        # Calculate put/call ratio by volume
        calls = opt_chain.calls
        puts = opt_chain.puts

        call_volume = calls['volume'].sum() if 'volume' in calls.columns else 0
        put_volume = puts['volume'].sum() if 'volume' in puts.columns else 0

        if call_volume == 0:
            return None

        put_call_ratio = round(put_volume / call_volume, 2)

        # Interpret ratio
        if put_call_ratio > 1.0:
            sentiment = "bearish"
            interpretation = "More puts than calls - traders hedging/expecting decline"
        elif put_call_ratio > 0.7:
            sentiment = "neutral-bearish"
            interpretation = "Elevated put activity - some hedging"
        elif put_call_ratio < 0.5:
            sentiment = "bullish"
            interpretation = "More calls than puts - traders expecting upside"
        else:
            sentiment = "neutral"
            interpretation = "Balanced put/call activity"

        return {
            "put_call_ratio": put_call_ratio,
            "sentiment": sentiment,
            "interpretation": interpretation,
            "call_volume": int(call_volume),
            "put_volume": int(put_volume),
            "expiration": nearest_exp,
            "confidence": "MEDIUM"
        }

    except Exception as e:
        logger.warning(f"Could not fetch options data for {ticker}: {str(e)}")
        return None

def get_institutional_ownership(ticker: str) -> Optional[Dict[str, Any]]:
    """
    Get institutional ownership and recent changes

    Args:
        ticker: Stock ticker symbol

    Returns:
        dict: Institutional ownership data
        None if unavailable
    """
    try:
        logger.info(f"Fetching institutional ownership for {ticker}")
        stock = yf.Ticker(ticker)

        # Get institutional holders
        holders = stock.institutional_holders

        if holders is None or holders.empty:
            logger.warning(f"No institutional data for {ticker}")
            return None

        # Calculate total shares held
        total_shares = holders['Shares'].sum()

        # Get top holders
        top_5 = holders.head(5)[['Holder', 'Shares', '% Out']].to_dict('records')

        # Format percentages
        for holder in top_5:
            holder['Shares'] = int(holder['Shares'])
            if isinstance(holder['% Out'], (int, float)):
                holder['% Out'] = round(holder['% Out'] * 100, 2)

        return {
            "total_institutional_shares": int(total_shares),
            "top_holders": top_5,
            "holder_count": len(holders),
            "confidence": "MEDIUM"
        }

    except Exception as e:
        logger.warning(f"Could not fetch institutional data for {ticker}: {str(e)}")
        return None

def get_risk_metrics(ticker: str) -> Optional[Dict[str, Any]]:
    """
    Calculate risk metrics from price history and info

    Args:
        ticker: Stock ticker symbol

    Returns:
        dict: Risk assessment metrics
        None if error
    """
    try:
        logger.info(f"Calculating risk metrics for {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info

        # Get 1 year of history for volatility
        hist = stock.history(period="1y")

        if hist.empty:
            return None

        # Calculate volatility (annualized standard deviation of returns)
        returns = hist['Close'].pct_change().dropna()
        volatility_30d = returns.tail(30).std() * (252 ** 0.5) * 100  # Annualized
        volatility_90d = returns.tail(90).std() * (252 ** 0.5) * 100

        # Get beta from info
        beta = info.get('beta')

        # Calculate 52-week high/low
        high_52w = hist['High'].max()
        low_52w = hist['Low'].min()
        current = hist['Close'].iloc[-1]

        # Distance from 52w high/low
        pct_from_high = round(((current - high_52w) / high_52w) * 100, 2)
        pct_from_low = round(((current - low_52w) / low_52w) * 100, 2)

        # Risk score (0-100, higher = riskier)
        risk_score = min(100, int((volatility_30d / 50) * 100))

        if risk_score < 30:
            risk_level = "Low"
        elif risk_score < 60:
            risk_level = "Moderate"
        else:
            risk_level = "High"

        return {
            "volatility_30d": round(volatility_30d, 2),
            "volatility_90d": round(volatility_90d, 2),
            "beta": round(beta, 2) if beta else None,
            "high_52w": round(high_52w, 2),
            "low_52w": round(low_52w, 2),
            "pct_from_high": pct_from_high,
            "pct_from_low": pct_from_low,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence": "HIGH"
        }

    except Exception as e:
        logger.warning(f"Could not calculate risk metrics for {ticker}: {str(e)}")
        return None

def get_insider_trading(ticker: str) -> Optional[Dict[str, Any]]:
    """
    Get insider trading activity (buys/sells by executives)

    Args:
        ticker: Stock ticker symbol

    Returns:
        dict: Insider trading activity
        None if unavailable
    """
    try:
        logger.info(f"Fetching insider trading for {ticker}")
        stock = yf.Ticker(ticker)

        # Get insider transactions
        insiders = stock.insider_transactions

        if insiders is None or insiders.empty:
            logger.warning(f"No insider trading data for {ticker}")
            return None

        # Get recent transactions (last 6 months)
        recent = insiders.head(20)

        # Count buys vs sells
        buys = 0
        sells = 0
        buy_value = 0
        sell_value = 0

        for _, row in recent.iterrows():
            shares = row.get('Shares', 0)
            value = row.get('Value', 0) or 0

            # Determine if buy or sell (positive shares = buy)
            if shares > 0:
                buys += 1
                buy_value += abs(value)
            else:
                sells += 1
                sell_value += abs(value)

        # Determine sentiment
        if buys > sells * 2:
            sentiment = "bullish"
            interpretation = "Significant insider buying - executives confident"
        elif sells > buys * 2:
            sentiment = "bearish"
            interpretation = "Heavy insider selling - potential concern"
        else:
            sentiment = "neutral"
            interpretation = "Mixed insider activity"

        return {
            "buy_transactions": buys,
            "sell_transactions": sells,
            "buy_value": int(buy_value),
            "sell_value": int(sell_value),
            "sentiment": sentiment,
            "interpretation": interpretation,
            "confidence": "MEDIUM",
            "note": "Based on recent insider filings (last 6 months)"
        }

    except Exception as e:
        logger.warning(f"Could not fetch insider trading for {ticker}: {str(e)}")
        return None

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
