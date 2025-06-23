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
# config
