import requests
import random
from datetime import datetime
import config
import pytz

# নমুনা মার্কেট ডেটা
OTC_PAIRS = ["AUD/CAD", "EUR/USD", "GBP/USD", "USD/JPY"]
FOREX_PAIRS = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]
CRYPTO_PAIRS = ["BTC/USD", "ETH/USD", "BNB/USD", "XRP/USD"]

def get_alpha_vantage_data(pair):
    """Alpha Vantage API থেকে ডেটা নেবে"""
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={pair}&apikey={config.ALPHA_VANTAGE_API}"
        response = requests.get(url)
        data = response.json()
        return data.get('Global Quote', {})
    except Exception as e:
        print(f"Alpha Vantage error: {e}")
        return None

def get_market_data(market_type, hour):
    """মার্কেট ডেটা ফেচ করবে"""
    # রিয়েল API ব্যবহার না করা পর্যন্ত নমুনা ডেটা দেবে
    if market_type == 'forex':
        pairs = FOREX_PAIRS
    elif market_type == 'crypto':
        pairs = CRYPTO_PAIRS
    else:
        pairs = OTC_PAIRS
    
    # সময়ের ভিত্তিতে ডেটা জেনারেট করবে (প্রোডাকশনে রিয়েল API ব্যবহার করুন)
    random.seed(hour)  # একই সময়ের জন্য একই ডেটা দেবে
    
    market_data = []
    for pair in pairs:
        base_price = 100 + (hour * 0.5)
        change = round(random.uniform(-2.0, 2.0), 2)
        current_price = round(base_price * (1 + change/100), 4)
        
        market_data.append({
            'pair': pair,
            'price': current_price,
            'change': change
        })
    
    return market_data
