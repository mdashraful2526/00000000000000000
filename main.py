# main.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from market_data import fetch_market_data
import config
import datetime

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Send message on /start"""
    user = update.effective_user
    update.message.reply_text(f"Hi {user.first_name}! Welcome to the Trading Bot\n\n"
                             "Use /markets to see available markets")

def list_markets(update: Update, context: CallbackContext) -> None:
    """Show available markets"""
    keyboard = [
        [
            InlineKeyboardButton("OTC Markets", callback_data='OTC'),
            InlineKeyboardButton("Real Markets", callback_data='REAL')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose market type:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    """Handle button presses"""
    query = update.callback_query
    query.answer()

    if query.data in ['OTC', 'REAL']:
        # Store market type in user context
        context.user_data['market_type'] = query.data
        
        # Ask for time input
        query.edit_message_text(text=f"You selected {query.data} market\n\n"
                               "Please enter the time in 24h format (e.g., 15 for 3PM):")
        return
    
    if 'time_input' not in context.user_data:
        try:
            time = int(query.data)
            if 0 <= time <= 23:
                context.user_data['time_input'] = time
                query.edit_message_text(text=f"Time set to {time}:00\n\nGathering data...")
                
                # Fetch market data
                market_type = context.user_data['market_type']
                data = fetch_market_data(market_type, time)
                
                # Display results
                message = "\n".join([f"{pair} {market_type}" for pair in data])
                query.edit_message_text(text=message)
            else:
                query.edit_message_text(text="Please enter a valid hour (0-23)")
        except ValueError:
            query.edit_message_text(text="Please enter a valid number (0-23)")

def handle_time_input(update: Update, context: CallbackContext) -> None:
    """Handle manual time input"""
    try:
        time = int(update.message.text)
        if 0 <= time <= 23:
            context.user_data['time_input'] = time
            update.message.reply_text(f"Time set to {time}:00\n\nGathering data...")
            
            # Fetch market data
            market_type = context.user_data.get('market_type', 'OTC')
            data = fetch_market_data(market_type, time)
            
            # Display results
            message = "\n".join([f"{pair} {market_type}" for pair in data])
            update.message.reply_text(message)
        else:
            update.message.reply_text("Please enter a valid hour (0-23)")
    except ValueError:
        update.message.reply_text("Please enter a valid number (0-23)")

def error_handler(update: Update, context: CallbackContext) -> None:
    """Log errors"""
    logger.error(msg="Exception while handling update:", exc_info=context.error)

def main() -> None:
    """Start the bot"""
    updater = Updater(config.TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("markets", list_markets))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_time_input))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
