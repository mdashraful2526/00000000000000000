# market_data.py
import requests
import datetime
from config import MARKET_API_KEY
import random

# Sample market pairs
OTC_MARKETS = [
    "AED/CNY", "AUD/CAD", "BHD/CNY",
    "EUR/USD", "GBP/USD", "AUD/NZD",
    "IZD/USD", "EUR/JPY", "CAD/JPY",
    "JD/USD", "AUD/CHF", "GBP/AUD"
]

REAL_MARKETS = [
    "BTC/USD", "ETH/USD", "XRP/USD",
    "LTC/USD", "BNB/USD", "ADA/USD",
    "DOT/USD", "LINK/USD", "BCH/USD"
]

def fetch_market_data(market_type: str, hour: int) -> list:
    """Fetch market data based on type and time"""
    if market_type == 'OTC':
        pairs = OTC_MARKETS
    else:
        pairs = REAL_MARKETS
    
    # In a real implementation, you would call the API here
    # For demonstration, we'll return random data
    return simulate_api_call(pairs, hour)

def simulate_api_call(pairs: list, hour: int) -> list:
    """Simulate API call with time-based data"""
    # This is where you would normally call your market data API
    # For now, we'll just return the pairs with simulated changes
    
    # Seed random with hour for consistent(ish) results
    random.seed(hour)
    
    # Return about 60% of the pairs randomly
    sample_size = max(4, int(len(pairs) * 0.6))
    return random.sample(pairs, sample_size)
