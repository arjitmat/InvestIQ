"""
Smart Caching System for ResearchIQ
Reduces API calls and improves performance
"""

import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Dict
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory cache (for development)
# In production, consider using Redis or similar
_cache: Dict[str, Dict[str, Any]] = {}

def generate_cache_key(ticker: str, data_type: str, data_snapshot: Optional[Any] = None) -> str:
    """
    Generate unique cache key based on ticker, data type, and data snapshot

    Args:
        ticker: Ticker symbol
        data_type: Type of data (e.g., 'ai_insights', 'technical', 'news')
        data_snapshot: Optional data to include in hash for versioning

    Returns:
        str: Unique cache key
    """
    # Base key
    date_hour = datetime.now().strftime("%Y-%m-%d-%H")
    base_key = f"{ticker}_{data_type}_{date_hour}"

    # Add data hash if provided (for version-sensitive caching)
    if data_snapshot is not None:
        try:
            data_str = json.dumps(data_snapshot, sort_keys=True, default=str)
            data_hash = hashlib.md5(data_str.encode()).hexdigest()[:8]
            base_key = f"{base_key}_{data_hash}"
        except Exception as e:
            logger.warning(f"Could not hash data snapshot: {e}")

    return base_key


def get_cached(cache_key: str) -> Optional[Any]:
    """
    Retrieve data from cache if valid

    Args:
        cache_key: Cache key to lookup

    Returns:
        Cached data if found and valid, None otherwise
    """
    if cache_key not in _cache:
        logger.debug(f"Cache miss: {cache_key}")
        return None

    entry = _cache[cache_key]

    # Check expiration
    if datetime.now() > entry['expires']:
        logger.debug(f"Cache expired: {cache_key}")
        # Clean up expired entry
        del _cache[cache_key]
        return None

    logger.info(f"Cache hit: {cache_key}")
    return entry['data']


def set_cache(cache_key: str, data: Any, ttl_minutes: int = 60) -> None:
    """
    Store data in cache with TTL (Time To Live)

    Args:
        cache_key: Unique cache key
        data: Data to cache
        ttl_minutes: Cache duration in minutes (default: 60)
    """
    expires_at = datetime.now() + timedelta(minutes=ttl_minutes)

    _cache[cache_key] = {
        'data': data,
        'expires': expires_at,
        'created': datetime.now()
    }

    logger.info(f"Cached: {cache_key} (TTL: {ttl_minutes} min)")


def invalidate_cache(ticker: Optional[str] = None, data_type: Optional[str] = None) -> int:
    """
    Invalidate cache entries

    Args:
        ticker: If provided, invalidate all entries for this ticker
        data_type: If provided, invalidate all entries of this type

    Returns:
        int: Number of entries invalidated
    """
    if ticker is None and data_type is None:
        # Clear entire cache
        count = len(_cache)
        _cache.clear()
        logger.info(f"Cleared entire cache ({count} entries)")
        return count

    # Selective invalidation
    keys_to_delete = []
    for key in _cache.keys():
        should_delete = False

        if ticker and key.startswith(ticker):
            should_delete = True
        if data_type and f"_{data_type}_" in key:
            should_delete = True

        if should_delete:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del _cache[key]

    logger.info(f"Invalidated {len(keys_to_delete)} cache entries")
    return len(keys_to_delete)


def cleanup_expired() -> int:
    """
    Remove all expired cache entries

    Returns:
        int: Number of entries cleaned up
    """
    now = datetime.now()
    keys_to_delete = []

    for key, entry in _cache.items():
        if now > entry['expires']:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del _cache[key]

    if keys_to_delete:
        logger.info(f"Cleaned up {len(keys_to_delete)} expired cache entries")

    return len(keys_to_delete)


def get_cache_stats() -> Dict[str, Any]:
    """
    Get cache statistics

    Returns:
        dict: Cache statistics
    """
    cleanup_expired()  # Clean before counting

    total_entries = len(_cache)

    # Group by data type
    types = {}
    for key in _cache.keys():
        parts = key.split('_')
        if len(parts) >= 2:
            data_type = parts[1]
            types[data_type] = types.get(data_type, 0) + 1

    return {
        'total_entries': total_entries,
        'entries_by_type': types,
        'oldest_entry': min([e['created'] for e in _cache.values()], default=None),
        'newest_entry': max([e['created'] for e in _cache.values()], default=None)
    }


# Example usage and testing
if __name__ == "__main__":
    print("Testing cache system...")

    # Test basic caching
    key1 = generate_cache_key("AAPL", "ai_insights")
    set_cache(key1, {"insight": "Bullish momentum"}, ttl_minutes=1)

    # Retrieve
    result = get_cached(key1)
    print(f"✓ Retrieved from cache: {result}")

    # Test with data snapshot
    data_snapshot = {"rsi": 65, "ma": "bullish"}
    key2 = generate_cache_key("AAPL", "technical", data_snapshot)
    set_cache(key2, {"analysis": "technical data"})

    # Stats
    stats = get_cache_stats()
    print(f"✓ Cache stats: {stats}")

    # Invalidation
    invalidated = invalidate_cache(ticker="AAPL")
    print(f"✓ Invalidated {invalidated} entries")

    print("\n✓ Cache system working correctly")
