# config.py - Configuration File
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Telegram Bot Configuration
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7332093108:AAHnMI33B7ecpFGTOxrpbGUNGrUD-aJ1vS4")
    
    # API URLs
    BINANCE_API_URL = "https://api.binance.com/api/v3"
    COINAPI_URL = "https://rest.coinapi.io/v1"
    
    # API Keys (Optional)
    COINAPI_KEY = os.getenv("COINAPI_KEY", "")
    
    # Bot Settings
    MAX_SIGNALS_HISTORY = 100
    CHART_WIDTH = 12
    CHART_HEIGHT = 6
    CHART_DPI = 100
    
    # Trading Pairs
    OTC_PAIRS = [
        "AUDCAD OTC", "AEDCNY OTC", "AUDCAD OTC", "BHDCNY OTC",
        "EURUSD OTC", "GBPUSD OTC", "AUDNZD OTC", "EURJPY OTC",
        "NZDUSD OTC", "AUDUSD OTC", "AUDCHF OTC", "CADJPY OTC",
        "GBPAUD OTC", "USDCAD OTC", "USDJPY OTC", "EURGBP OTC"
    ]
    
    REAL_PAIRS = [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT",
        "SOLUSDT", "DOTUSDT", "LINKUSDT", "LTCUSDT", "AVAXUSDT",
        "MATICUSDT", "UNIUSDT", "ATOMUSDT", "FTMUSDT", "NEARUSDT"
    ]
    
    # Chart Colors
    CHART_COLORS = {
        'background': '#1e1e1e',
        'candle_up': '#00ff00',
        'candle_down': '#ff0000',
        'text': 'white',
        'grid': '#333333'
    }
    
    # Signal Settings
    SIGNAL_EXPIRY_MINUTES = 1
    MIN_PRICE_CHANGE = 0.0001
    
    # Database (if needed)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trading_bot.db")

# Create config instance
config = Config()
