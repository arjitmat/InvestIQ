"""
Reddit API Data Collector for ResearchIQ
Tracks mention volume on investing subreddits
Data Quality: LOW - Volume signal only, not sentiment quality
"""

import praw
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import sys
import os
import time

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    REDDIT_REQUEST_DELAY,
    REDDIT_LOOKBACK_DAYS,
    get_subreddits_for_asset
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_mention_volume(
    ticker: str,
    asset_type: str = "stocks",
    days: int = REDDIT_LOOKBACK_DAYS
) -> Optional[Dict[str, Any]]:
    """
    Get mention volume for a ticker across relevant subreddits

    Args:
        ticker: Ticker symbol to search for
        asset_type: Type of asset (stocks, crypto, indices, commodities)
        days: Number of days to look back

    Returns:
        dict: Mention statistics including:
            - total_mentions: Count of mentions found
            - subreddit_breakdown: Mentions per subreddit
            - vs_baseline: Comparison to average (if available)
            - timeframe: Search timeframe
        None if error or no API credentials

    Data Quality: LOW - DIRECTIONAL ONLY
    - Volume count, not sentiment analysis
    - Free Reddit API = basic search only
    - Use for attention spike detection
    - NOT for investment decisions
    """
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        logger.warning("Reddit API credentials not configured. Skipping Reddit collection.")
        return None

    try:
        # Initialize Reddit API
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )

        # Get relevant subreddits for asset type
        subreddits_to_search = get_subreddits_for_asset(asset_type)

        logger.info(f"Searching Reddit for '{ticker}' in {subreddits_to_search}")

        # Clean ticker for search (remove special chars)
        search_term = ticker.replace('^', '').replace('-USD', '').replace('=F', '')

        # Track mentions
        total_mentions = 0
        subreddit_breakdown = {}

        # Calculate time threshold
        time_threshold = datetime.now() - timedelta(days=days)

        # Search each subreddit
        for subreddit_name in subreddits_to_search:
            try:
                subreddit = reddit.subreddit(subreddit_name)

                # Search for ticker mentions
                mentions = 0
                for submission in subreddit.search(search_term, time_filter="week", limit=100):
                    # Check if within timeframe
                    post_time = datetime.fromtimestamp(submission.created_utc)
                    if post_time >= time_threshold:
                        # Check if ticker appears in title or body
                        title_lower = submission.title.lower()
                        selftext_lower = submission.selftext.lower()
                        search_lower = search_term.lower()

                        if search_lower in title_lower or search_lower in selftext_lower:
                            mentions += 1

                subreddit_breakdown[subreddit_name] = mentions
                total_mentions += mentions

                # Be respectful to Reddit API - delay between requests
                time.sleep(REDDIT_REQUEST_DELAY)

            except Exception as e:
                logger.warning(f"Error searching r/{subreddit_name}: {str(e)}")
                subreddit_breakdown[subreddit_name] = 0
                continue

        # Calculate baseline comparison (rough estimate)
        # Baseline: ~10-50 mentions per week for average stock
        baseline_mentions = 30
        vs_baseline = "average"

        if total_mentions > baseline_mentions * 3:
            vs_baseline = "high (3x+ average)"
        elif total_mentions > baseline_mentions * 1.5:
            vs_baseline = "elevated (1.5x+ average)"
        elif total_mentions < baseline_mentions * 0.5:
            vs_baseline = "low (below average)"

        result = {
            "ticker": ticker,
            "total_mentions": total_mentions,
            "subreddit_breakdown": subreddit_breakdown,
            "vs_baseline": vs_baseline,
            "timeframe_days": days,
            "searched_subreddits": subreddits_to_search,
            "timestamp": datetime.now().isoformat(),
            "data_quality_note": "Volume signal only - not sentiment analysis"
        }

        logger.info(f"Reddit mentions for {ticker}: {total_mentions} ({vs_baseline})")
        return result

    except Exception as e:
        logger.error(f"Error fetching Reddit data for {ticker}: {str(e)}")
        return None

def get_trending_tickers(subreddit_name: str = "wallstreetbets", limit: int = 10) -> Optional[List[str]]:
    """
    Get trending ticker mentions from a subreddit (bonus feature)

    Args:
        subreddit_name: Subreddit to check
        limit: Number of hot posts to scan

    Returns:
        list: List of ticker symbols mentioned or None if error
    """
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        return None

    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )

        subreddit = reddit.subreddit(subreddit_name)
        trending = []

        for submission in subreddit.hot(limit=limit):
            # Simple ticker extraction (look for $TICKER pattern)
            import re
            tickers = re.findall(r'\$([A-Z]{2,5})\b', submission.title + " " + submission.selftext)
            trending.extend(tickers)

        # Return unique tickers
        return list(set(trending))

    except Exception as e:
        logger.error(f"Error getting trending tickers: {str(e)}")
        return None

# Example usage and testing
if __name__ == "__main__":
    # Test with stock
    print("Testing Reddit API with AAPL...")
    aapl_mentions = get_mention_volume("AAPL", asset_type="stocks")

    if aapl_mentions:
        print(f"✓ AAPL mentions: {aapl_mentions['total_mentions']} ({aapl_mentions['vs_baseline']})")
        print(f"  Breakdown: {aapl_mentions['subreddit_breakdown']}")
    elif aapl_mentions is None:
        print("✗ Reddit API not configured or error occurred")

    # Test with crypto
    print("\nTesting with BTC...")
    btc_mentions = get_mention_volume("BTC", asset_type="crypto")

    if btc_mentions:
        print(f"✓ BTC mentions: {btc_mentions['total_mentions']} ({btc_mentions['vs_baseline']})")
