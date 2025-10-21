"""
Configuration module for ResearchIQ
Manages API keys, asset lists, and application settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "ResearchIQ/1.0")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Asset Lists
STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
    "NVDA", "META", "JPM", "BAC", "V",
    "MA", "WMT", "HD", "DIS", "NFLX"
]

CRYPTO = [
    "BTC-USD", "ETH-USD", "SOL-USD",
    "BNB-USD", "ADA-USD"
]

INDICES = [
    "^GSPC",  # S&P 500
    "^IXIC",  # Nasdaq Composite
    "^DJI"    # Dow Jones Industrial Average
]

COMMODITIES = [
    "GC=F",  # Gold Futures
    "SI=F"   # Silver Futures
]

# All supported assets
ALL_ASSETS = STOCKS + CRYPTO + INDICES + COMMODITIES

# Asset type mapping
ASSET_TYPES = {
    "stocks": STOCKS,
    "crypto": CRYPTO,
    "indices": INDICES,
    "commodities": COMMODITIES
}

# API Rate Limits
NEWSAPI_DAILY_LIMIT = 100  # Free tier limit
REDDIT_REQUEST_DELAY = 2   # Seconds between requests (be respectful)

# Analysis Parameters
RSI_PERIOD = 14
MA_PERIODS = [20, 50, 200]  # Moving average periods
VOLUME_LOOKBACK_DAYS = 30
NEWS_LOOKBACK_DAYS = 7
REDDIT_LOOKBACK_DAYS = 7
TRENDS_LOOKBACK_DAYS = 30

# Data Quality Confidence Levels
CONFIDENCE_HIGH = "HIGH"
CONFIDENCE_MEDIUM = "MEDIUM"
CONFIDENCE_LOW = "LOW"
CONFIDENCE_CONTEXT = "CONTEXT ONLY"
CONFIDENCE_AI = "AI-GENERATED"

# Subreddits to monitor for social signals
REDDIT_SUBREDDITS = {
    "stocks": ["wallstreetbets", "stocks", "investing"],
    "crypto": ["CryptoCurrency", "Bitcoin", "ethereum"],
    "indices": ["wallstreetbets", "stocks", "investing"],
    "commodities": ["wallstreetbets", "investing"]
}

# Fear & Greed Index API
FEAR_GREED_API_URL = "https://api.alternative.me/fng/"

# Application Settings
APP_NAME = "ResearchIQ"
APP_VERSION = "1.0.0"
TEMP_REPORTS_DIR = "../reports_temp"
MAX_STORED_REPORTS = 10  # Auto-delete older reports

# AI Settings (Gemini)
AI_CACHE_TTL_MINUTES = 60  # Cache AI insights for 1 hour
AI_MAX_RETRIES = 2  # Retry failed AI calls
AI_TIMEOUT_SECONDS = 10  # Timeout for AI API calls

# CORS Settings (update with your frontend URL in production)
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://invest-iq-wheat.vercel.app",  # Vercel frontend
    "*"  # Allow all for development (restrict in production)
]

def validate_ticker(ticker: str, asset_type: str = None) -> bool:
    """
    Validate if ticker is in supported assets list

    Args:
        ticker: Ticker symbol to validate
        asset_type: Optional asset type filter

    Returns:
        bool: True if ticker is supported, False otherwise
    """
    ticker = ticker.upper()

    if asset_type:
        return ticker in ASSET_TYPES.get(asset_type.lower(), [])

    return ticker in ALL_ASSETS

def get_subreddits_for_asset(asset_type: str) -> list:
    """
    Get relevant subreddits for asset type

    Args:
        asset_type: Type of asset (stocks, crypto, indices, commodities)

    Returns:
        list: List of subreddit names to search
    """
    return REDDIT_SUBREDDITS.get(asset_type.lower(), REDDIT_SUBREDDITS["stocks"])
