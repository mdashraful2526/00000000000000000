# 🤖 Telegram OTC Trading Bot

একটি শক্তিশালী Telegram bot যা OTC এবং Real Market trading signals প্রদান করে 1-minute candlestick charts সহ।

## ✨ Features

- 📊 **Real-time Market Data**: Binance API থেকে live data
- 🎯 **OTC Market Simulation**: Realistic OTC market data generation
- 📈 **1-Minute Charts**: Professional candlestick charts
- 🚦 **Trading Signals**: UP/DOWN signals with timing
- ⏰ **Time-based Predictions**: Next candle predictions
- 🔄 **Real-time Updates**: Auto-refresh functionality

## 🚀 Quick Setup

### 1. Bot Token পাওয়ার জন্য:
1. Telegram এ @BotFather এ যান
2. `/newbot` command দিন
3. Bot এর নাম দিন (যেমন: "My OTC Trading Bot")
4. Username দিন (যেমন: "my_otc_trading_bot")
5. Token copy করুন

### 2. Files Setup:

```
telegram-otc-bot/
├── bot.py              # Main bot file
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── .env               # Environment variables
├── setup.py           # Setup script
├── README.md          # This file
└── charts/            # Chart images (auto-created)
```

### 3. Installation Steps:

#### Step 1: Download Files
সব files একটি folder এ রাখুন (যেমন: `telegram-otc-bot`)

#### Step 2: Python Environment Setup
```bash
# Virtual environment তৈরি করুন
python -m venv otc_bot_env

# Activate করুন
# Windows:
otc_bot_env\Scripts\activate
# Linux/Mac:
source otc_bot_env/bin/activate
```

#### Step 3: Dependencies Install
```bash
pip install -r requirements.txt
```

#### Step 4: Environment Variables Setup
`.env` file edit করুন:
```bash
BOT_TOKEN=your_actual_bot_token_here
```

#### Step 5: Run the Bot
```bash
python bot.py
```

## 📁 File Structure এবং Naming:

### File Names (exact যেমন দেওয়া হয়েছে):
- `bot.py` - Main bot script
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (secret)
- `setup.py` - Installation script
- `README.md` - Documentation

### Folder Structure:
```
your-project-folder/
├── bot.py
├── config.py  
├── requirements.txt
├── .env
├── setup.py
├── README.md
└── charts/ (auto-created)
```

## 🔧 Configuration

### .env File:
```bash
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
COINAPI_KEY=optional_api_key
DEBUG=False
```

### config.py এ Settings:
- Chart colors, sizes
- Trading pairs lists
- API endpoints
- Signal settings

## 🎮 Bot Commands:

- `/start` - Bot শুরু করুন
- **OTC Markets** - OTC trading pairs
- **Real Markets** - Cryptocurrency pairs
- **Active Signals** - Recent signals দেখুন

## 📊 Supported Markets:

### OTC Pairs:
- AUDCAD OTC, EURUSD OTC, GBPUSD OTC
- AUDNZD OTC, EURJPY OTC, NZDUSD OTC
- AUDUSD OTC, AUDCHF OTC, CADJPY OTC
- GBPAUD OTC, USDCAD OTC, USDJPY OTC

### Real Crypto Pairs:
- BTCUSDT, ETHUSDT, BNBUSDT
- ADAUSDT, XRPUSDT, SOLUSDT
- DOTUSDT, LINKUSDT, LTCUSDT
- AVAXUSDT, MATICUSDT, UNIUSDT

## 🔄 How It Works:

1. **Market Data**: Real API data + simulated OTC data
2. **Chart Generation**: Matplotlib ile professional charts
3. **Signal Generation**: Moving average based signals
4. **Time Tracking**: 1-minute candle timing
5. **Signal Storage**: Recent signals memory তে রাখা হয়

## 🚀 Deployment Options:

### Local Run:
```bash
python bot.py
```

### Cloud Deployment:
- **Heroku**: `Procfile` add করুন
- **Railway**: Direct deploy
- **DigitalOcean**: VPS এ run করুন
- **PythonAnywhere**: Scheduled tasks

### Heroku Deployment:
```bash
# Procfile তৈরি করুন:
echo "worker: python bot.py" > Procfile

# Deploy:
git init
git add .
git commit -m "Initial commit"
heroku create your-bot-name
git push heroku main
heroku ps:scale worker=1
```

## 🐛 Troubleshooting:

### Common Issues:
1. **Bot Token Error**: `.env` file check করুন
2. **Chart Error**: matplotlib install check করুন
3. **API Error**: Internet connection check করুন
4. **Permission Error**: Bot admin করুন group এ

### Debug Mode:
```python
# config.py তে DEBUG = True করুন
DEBUG = True
LOG_LEVEL = "DEBUG"
```

### Log Check:
```bash
# Terminal এ logs দেখুন
python bot.py
```

## 📱 Bot Usage:

### User Interaction:
1. `/start` command দিন
2. Market select করুন (OTC/Real)
3. Trading pair choose করুন
4. Chart এবং current price দেখুন
5. "Get Signal" button এ click করুন
6. UP/DOWN signal পাবেন timing সহ

### Signal Format:
```
🎯 Trading Signal Generated

📊 BTCUSDT
💰 Entry Price: $43,250.75
🎯 Signal: 🟢 UP
⏰ Signal Time: 14:25:30
⏳ Next Candle: 14:26:30

*Signal valid for next 1-minute candle*
```

## 🔐 Security:

### Environment Variables:
- Never commit `.env` file
- Use strong bot tokens
- Rotate API keys regularly

### .gitignore File:
```
.env
__pycache__/
*.pyc
charts/
logs/
```

## 🌐 Web Hosting:

### Free Options:
- **Railway**: Easy deployment
- **Render**: Free tier available  
- **Fly.io**: Free allowance
- **PythonAnywhere**: Free account

### Paid Options:
- **Heroku**: $7/month
- **DigitalOcean**: $5/month VPS
- **AWS EC2**: Pay per use
- **Google Cloud**: Free credits

## 📈 Advanced Features:

### Custom Indicators:
```python
# bot.py তে add করুন
def calculate_rsi(prices, period=14):
    # RSI calculation
    pass

def bollinger_bands(prices, period=20):
    # Bollinger bands calculation  
    pass
```

### Database Integration:
```python
# SQLite database for signal history
import sqlite3

def save_signal_to_db(signal_data):
    # Save signals to database
    pass
```

### Multiple Timeframes:
```python
# 5min, 15min, 1hour charts
TIMEFRAMES = {
    '1m': '1m',
    '5m': '5m', 
    '15m': '15m',
    '1h': '1h'
}
```

## 🎨 Customization:

### Chart Styling:
```python
# config.py তে colors change করুন
CHART_COLORS = {
    'background': '#000000',  # Black background
    'candle_up': '#00ff00',   # Green candles
    'candle_down': '#ff0000', # Red candles
    'text': '#ffffff'         # White text
}
```

### Add More Pairs:
```python
# config.py তে নতুন pairs add করুন
OTC_PAIRS.append("GBPJPY OTC")
REAL_PAIRS.append("DOGEUSDT")
```

## 📞 Support:

### Common Commands:
- `/start` - Start bot
- `/help` - Show help (optional)
- `/status` - Bot status (optional)

### Bot Maintenance:
- Regular API key rotation
- Monitor error logs
- Update dependencies monthly
- Backup signal data

## 🚀 Deployment Steps Summary:

1. **Create folder**: `mkdir telegram-otc-bot`
2. **Copy files**: All 6 files নিয়ে folder এ রাখুন
3. **Install Python**: Python 3.8+ install করুন
4. **Create venv**: `python -m venv otc_bot_env`
5. **Activate venv**: Platform অনুযায়ী activate করুন
6. **Install deps**: `pip install -r requirements.txt`
7. **Set token**: `.env` file এ bot token add করুন
8. **Run bot**: `python bot.py`
9. **Test**: Telegram এ bot test করুন
10. **Deploy**: Cloud platform এ deploy করুন

## 🎯 Production Ready:

### Performance:
- Async operations for speed
- Memory efficient chart generation  
- API rate limiting handled
- Error handling implemented

### Reliability:
- Automatic restart on errors
- Data validation
- Timeout handling
- Graceful shutdown

---

## 📋 File Checklist:

✅ `bot.py` - Main bot code  
✅ `config.py` - Configuration  
✅ `requirements.txt` - Dependencies  
✅ `.env` - Environment variables  
✅ `setup.py` - Installation script  
✅ `README.md` - Documentation  

**Total Files**: 6 files
**Estimated Setup Time**: 10-15 minutes
**Skill Level**: Beginner friendly

---

🎉 **Your OTC Trading Bot is ready to use!**

For questions or support, check the troubleshooting section or review the error logs.
