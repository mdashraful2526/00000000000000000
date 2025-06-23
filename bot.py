# bot.py - Main Telegram Bot File
import asyncio
import logging
from datetime import datetime, timedelta
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import aiohttp
import random
from typing import Dict, List
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = "7332093108:AAHnMI33B7ecpFGTOxrpbGUNGrUD-aJ1vS4"
BINANCE_API_URL = "https://api.binance.com/api/v3"

class OTCTradingBot:
    def __init__(self):
        self.active_trades = {}
        self.price_data = {}
        self.signals = {}
        
        # OTC pairs list
        self.otc_pairs = [
            "AUDCAD OTC", "AEDCNY OTC", "AUDCAD OTC", "BHDCNY OTC",
            "EURUSD OTC", "GBPUSD OTC", "AUDNZD OTC", "EURJPY OTC",
            "NZDUSD OTC", "AUDUSD OTC", "AUDCHF OTC", "CADJPY OTC",
            "GBPAUD OTC"
        ]
        
        # Real market pairs
        self.real_pairs = [
            "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT",
            "SOLUSDT", "DOTUSDT", "LINKUSDT", "LTCUSDT", "AVAXUSDT"
        ]

    async def get_real_market_data(self, symbol: str) -> Dict:
        """Get real market data from Binance API"""
        try:
            async with aiohttp.ClientSession() as session:
                # Get current price
                price_url = f"{BINANCE_API_URL}/ticker/price?symbol={symbol}"
                async with session.get(price_url) as response:
                    price_data = await response.json()
                
                # Get kline data for 1 minute
                kline_url = f"{BINANCE_API_URL}/klines?symbol={symbol}&interval=1m&limit=100"
                async with session.get(kline_url) as response:
                    kline_data = await response.json()
                
                return {
                    "symbol": symbol,
                    "price": float(price_data["price"]),
                    "klines": kline_data,
                    "timestamp": datetime.now()
                }
        except Exception as e:
            logger.error(f"Error fetching real market data: {e}")
            return None

    def generate_otc_data(self, symbol: str) -> Dict:
        """Generate simulated OTC market data"""
        base_price = random.uniform(0.5, 2.0)
        
        # Generate 100 candles for chart
        klines = []
        current_price = base_price
        
        for i in range(100):
            open_price = current_price
            # Generate realistic price movement
            change = random.uniform(-0.02, 0.02) * open_price
            close_price = open_price + change
            high_price = max(open_price, close_price) + random.uniform(0, 0.01) * open_price
            low_price = min(open_price, close_price) - random.uniform(0, 0.01) * open_price
            volume = random.uniform(1000, 10000)
            
            timestamp = int((datetime.now() - timedelta(minutes=100-i)).timestamp() * 1000)
            
            klines.append([
                timestamp,
                str(open_price),
                str(high_price),
                str(low_price),
                str(close_price),
                str(volume),
                timestamp + 60000,
                "0",
                0,
                "0",
                "0",
                "0"
            ])
            
            current_price = close_price
        
        return {
            "symbol": symbol,
            "price": current_price,
            "klines": klines,
            "timestamp": datetime.now()
        }

    def create_chart(self, data: Dict, symbol: str) -> BytesIO:
        """Create candlestick chart"""
        try:
            klines = data["klines"]
            
            # Extract OHLC data
            timestamps = [datetime.fromtimestamp(int(k[0])/1000) for k in klines]
            opens = [float(k[1]) for k in klines]
            highs = [float(k[2]) for k in klines]
            lows = [float(k[3]) for k in klines]
            closes = [float(k[4]) for k in klines]
            
            # Create figure
            fig, ax = plt.subplots(figsize=(12, 6))
            fig.patch.set_facecolor('#1e1e1e')
            ax.set_facecolor('#1e1e1e')
            
            # Plot candlesticks
            for i, (timestamp, open_price, high, low, close) in enumerate(zip(timestamps, opens, highs, lows, closes)):
                color = '#00ff00' if close >= open_price else '#ff0000'
                
                # Draw the wick
                ax.plot([timestamp, timestamp], [low, high], color='white', linewidth=0.5)
                
                # Draw the body
                body_height = abs(close - open_price)
                body_bottom = min(open_price, close)
                
                rect = plt.Rectangle((mdates.date2num(timestamp) - 0.0003, body_bottom), 
                                   0.0006, body_height, 
                                   facecolor=color, edgecolor=color)
                ax.add_patch(rect)
            
            # Formatting
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
            plt.xticks(rotation=45)
            
            ax.set_title(f'{symbol} - 1 Minute Chart', color='white', fontsize=14)
            ax.set_xlabel('Time', color='white')
            ax.set_ylabel('Price', color='white')
            ax.tick_params(colors='white')
            
            # Style
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            
            plt.tight_layout()
            
            # Save to BytesIO
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', facecolor='#1e1e1e', dpi=100)
            img_buffer.seek(0)
            plt.close()
            
            return img_buffer
            
        except Exception as e:
            logger.error(f"Error creating chart: {e}")
            return None

    def generate_signal(self, data: Dict) -> str:
        """Generate trading signal based on price data"""
        try:
            klines = data["klines"]
            closes = [float(k[4]) for k in klines[-20:]]  # Last 20 closes
            
            # Simple moving average strategy
            sma_short = sum(closes[-5:]) / 5
            sma_long = sum(closes[-10:]) / 10
            current_price = closes[-1]
            prev_price = closes[-2]
            
            # Generate signal
            if sma_short > sma_long and current_price > prev_price:
                return "🟢 UP"
            elif sma_short < sma_long and current_price < prev_price:
                return "🔴 DOWN"
            else:
                return "⚪ WAIT"
                
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            return "⚪ WAIT"

# Bot handlers
bot_instance = OTCTradingBot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    keyboard = [
        [InlineKeyboardButton("📊 OTC Markets", callback_data="otc_markets")],
        [InlineKeyboardButton("💹 Real Markets", callback_data="real_markets")],
        [InlineKeyboardButton("📈 Active Signals", callback_data="active_signals")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = """
🤖 **OTC Trading Bot**

📊 Real-time market data
📈 1-minute candlestick charts  
🎯 UP/DOWN trading signals
⏰ Time-based predictions

Choose a market to start trading:
    """
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard buttons"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "otc_markets":
        await show_otc_markets(query)
    elif query.data == "real_markets":
        await show_real_markets(query)
    elif query.data == "active_signals":
        await show_active_signals(query)
    elif query.data.startswith("trade_"):
        symbol = query.data.replace("trade_", "")
        await show_trading_interface(query, symbol)
    elif query.data.startswith("signal_"):
        symbol = query.data.replace("signal_", "")
        await generate_trading_signal(query, symbol)

async def show_otc_markets(query):
    """Show OTC market pairs"""
    keyboard = []
    for pair in bot_instance.otc_pairs:
        keyboard.append([InlineKeyboardButton(pair, callback_data=f"trade_{pair}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("📊 **OTC Markets**\n\nSelect a trading pair:", 
                                reply_markup=reply_markup, parse_mode='Markdown')

async def show_real_markets(query):
    """Show real market pairs"""
    keyboard = []
    for i in range(0, len(bot_instance.real_pairs), 2):
        row = []
        row.append(InlineKeyboardButton(bot_instance.real_pairs[i], 
                                      callback_data=f"trade_{bot_instance.real_pairs[i]}"))
        if i + 1 < len(bot_instance.real_pairs):
            row.append(InlineKeyboardButton(bot_instance.real_pairs[i + 1], 
                                          callback_data=f"trade_{bot_instance.real_pairs[i + 1]}"))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("💹 **Real Markets**\n\nSelect a trading pair:", 
                                reply_markup=reply_markup, parse_mode='Markdown')

async def show_trading_interface(query, symbol):
    """Show trading interface for selected symbol"""
    try:
        # Get market data
        if "OTC" in symbol:
            data = bot_instance.generate_otc_data(symbol)
        else:
            data = await bot_instance.get_real_market_data(symbol)
        
        if not data:
            await query.edit_message_text("❌ Error fetching market data. Please try again.")
            return
        
        # Create chart
        chart = bot_instance.create_chart(data, symbol)
        
        if chart:
            # Generate signal
            signal = bot_instance.generate_signal(data)
            current_time = datetime.now().strftime("%H:%M:%S")
            
            keyboard = [
                [InlineKeyboardButton("📊 Get Signal", callback_data=f"signal_{symbol}")],
                [InlineKeyboardButton("🔄 Refresh", callback_data=f"trade_{symbol}")],
                [InlineKeyboardButton("🔙 Back", callback_data="otc_markets" if "OTC" in symbol else "real_markets")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            caption = f"""
📈 **{symbol}**
💰 Price: ${data['price']:.6f}
🎯 Signal: {signal}
⏰ Time: {current_time}
📊 Timeframe: 1 Minute

*Click "Get Signal" for trading prediction*
            """
            
            await query.message.reply_photo(
                photo=chart,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            await query.delete_message()
        else:
            await query.edit_message_text("❌ Error creating chart. Please try again.")
            
    except Exception as e:
        logger.error(f"Error in trading interface: {e}")
        await query.edit_message_text("❌ Error loading trading interface. Please try again.")

async def generate_trading_signal(query, symbol):
    """Generate and show trading signal"""
    try:
        # Get fresh data
        if "OTC" in symbol:
            data = bot_instance.generate_otc_data(symbol)
        else:
            data = await bot_instance.get_real_market_data(symbol)
        
        if not data:
            await query.answer("❌ Error fetching data", show_alert=True)
            return
        
        signal = bot_instance.generate_signal(data)
        current_time = datetime.now()
        next_candle_time = current_time + timedelta(minutes=1)
        
        # Store signal with timestamp
        bot_instance.signals[f"{symbol}_{current_time.strftime('%H:%M')}"] = {
            "symbol": symbol,
            "signal": signal,
            "time": current_time,
            "next_candle": next_candle_time,
            "price": data["price"]
        }
        
        signal_text = f"""
🎯 **Trading Signal Generated**

📊 **{symbol}**
💰 Entry Price: ${data['price']:.6f}
🎯 **Signal: {signal}**
⏰ Signal Time: {current_time.strftime('%H:%M:%S')}
⏳ Next Candle: {next_candle_time.strftime('%H:%M:%S')}

*Signal valid for next 1-minute candle*
        """
        
        await query.answer()
        await query.message.reply_text(signal_text, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error generating signal: {e}")
        await query.answer("❌ Error generating signal", show_alert=True)

async def show_active_signals(query):
    """Show active trading signals"""
    try:
        if not bot_instance.signals:
            await query.edit_message_text("📊 No active signals found.\n\nStart trading to generate signals!")
            return
        
        signals_text = "📈 **Active Trading Signals**\n\n"
        
        # Show last 10 signals
        recent_signals = list(bot_instance.signals.items())[-10:]
        
        for signal_id, signal_data in recent_signals:
            time_str = signal_data["time"].strftime("%H:%M")
            signals_text += f"🎯 **{signal_data['symbol']}** - {time_str}\n"
            signals_text += f"   Signal: {signal_data['signal']}\n"
            signals_text += f"   Price: ${signal_data['price']:.6f}\n\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(signals_text, reply_markup=reply_markup, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error showing active signals: {e}")
        await query.edit_message_text("❌ Error loading signals.")

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Start the bot
    logger.info("Starting OTC Trading Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
