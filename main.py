import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from market_data import get_market_data
import config
import pytz
from datetime import datetime

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# বাংলাদেশের সময় অনুযায়ী সময় দেখাবে
dhaka_time = pytz.timezone(config.TIMEZONE)

def start(update: Update, context: CallbackContext) -> None:
    """স্টার্ট কমান্ড হ্যান্ডলার"""
    user = update.effective_user
    update.message.reply_text(f'আসসালামু আলাইকুম {user.first_name}!\n\n'
                             'আমি আপনার ট্রেডিং সহকারী বট\n\n'
                             'মার্কেট ডেটা পেতে /markets টাইপ করুন')

def list_markets(update: Update, context: CallbackContext) -> None:
    """মার্কেট লিস্ট দেখাবে"""
    keyboard = [
        [InlineKeyboardButton("ফরেক্স মার্কেট", callback_data='forex')],
        [InlineKeyboardButton("ক্রিপ্টো মার্কেট", callback_data='crypto')],
        [InlineKeyboardButton("OTC মার্কেট", callback_data='otc')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('কোন মার্কেট দেখতে চান?', reply_markup=reply_markup)

def handle_market_selection(update: Update, context: CallbackContext) -> None:
    """মার্কেট সিলেক্ট হ্যান্ডলার"""
    query = update.callback_query
    query.answer()
    
    market_type = query.data
    context.user_data['market_type'] = market_type
    
    # সময় ইনপুট চাইবে
    query.edit_message_text(text=f"আপনি {market_type} মার্কেট নির্বাচন করেছেন\n\n"
                           "কোন সময়ের ডেটা চান? (24 ঘন্টা ফরম্যাটে লিখুন, যেমন: 13)")

def handle_time_input(update: Update, context: CallbackContext) -> None:
    """সময় ইনপুট হ্যান্ডলার"""
    try:
        time = int(update.message.text)
        if 0 <= time <= 23:
            market_type = context.user_data.get('market_type', 'forex')
            
            # মার্কেট ডেটা ফেচ করবে
            update.message.reply_text(f"{time}:00 টার ডেটা লোড হচ্ছে...")
            
            market_data = get_market_data(market_type, time)
            
            # রেজাল্ট দেখাবে
            response = f"{market_type} মার্কেট ডেটা ({time}:00)\n\n"
            for item in market_data:
                response += f"{item['pair']}: {item['price']} ({item['change']}%)\n"
            
            update.message.reply_text(response)
        else:
            update.message.reply_text("দয়া করে 0 থেকে 23 এর মধ্যে একটি সংখ্যা দিন")
    except ValueError:
        update.message.reply_text("দয়া করে শুধুমাত্র সংখ্যা দিন (যেমন: 9, 13, 22)")

def error_handler(update: Update, context: CallbackContext) -> None:
    """এরর হ্যান্ডলার"""
    logger.error(msg="একটি সমস্যা হয়েছে:", exc_info=context.error)
    update.message.reply_text("দুঃখিত, একটি সমস্যা হয়েছে। পরে আবার চেষ্টা করুন")

def main() -> None:
    """মেইন ফাংশন"""
    updater = Updater(config.TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # কমান্ড হ্যান্ডলার
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("markets", list_markets))
    
    # কলব্যাক হ্যান্ডলার
    dispatcher.add_handler(CallbackQueryHandler(handle_market_selection))
    
    # মেসেজ হ্যান্ডলার
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_time_input))
    
    # এরর হ্যান্ডলার
    dispatcher.add_error_handler(error_handler)

    # বট স্টার্ট করবে
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
