import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("دکمه شماره 1", callback_data='1')],
        [InlineKeyboardButton("دکمه شماره 2", callback_data='2')],
        [InlineKeyboardButton("دکمه شماره 3", callback_data='3')],
        [InlineKeyboardButton("دکمه شماره 4", callback_data='4')]
                ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose:', reply_markup=reply_markup)
    

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='نه نه نه، اینجوری نمیشه دیگه. لطفا دوباره /start رو بزن و از دکمه‌های شیشه‌ای استفاده کن.')

if __name__ == '__main__':
    application = ApplicationBuilder().token('PUT BOT TOKEN API HERE').build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    application.run_polling()