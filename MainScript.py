import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import pandas as pd
from PandaDatabaseFunctions import *

BattlesDatabase = 'battles.csv'
CharactersDeathesDatabase = 'character-deaths.csv'
CharactersPredictions = 'character-predictions.csv'

# Include the pandas functions from the previous artifact here

import os
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())
import sys
print("Python path:", sys.path)


try:
    from PandaDatabaseFunctions import get_column_names, search_csv, get_unique_values
    print("Successfully imported functions from PandaDatabaseFunctions")
except ImportError as e:
    print(f"Failed to import from PandaDatabaseFunctions: {e}")


    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("جستجوی تاریخچه جنگ‌ها", callback_data='Battles')],
        [InlineKeyboardButton("جستجوی تاریخچه شخصیت‌ها", callback_data='Characters')],
        [InlineKeyboardButton("جستجوی تاریخچه مرگ شخصیت‌ها", callback_data='Deaths')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose an action:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'Battles':
        print(get_value_from_row_index(BattlesDatabase,2,0))
        print(get_value_from_row_index(BattlesDatabase,3,0))
        print(get_value_from_row_index(BattlesDatabase,4,0))
        columns = get_column_names(BattlesDatabase)
        keyboard = [[InlineKeyboardButton(col, callback_data=col)] for col in get_value_from_row_index(BattlesDatabase)]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Select a column to search:", reply_markup=reply_markup)
    elif query.data == 'show_columns':
        columns = get_column_names(BattlesDatabase)
        await query.edit_message_text(f"Columns in the CSV file:\n{', '.join(columns)}")
    elif query.data == 'show_unique':
        columns = get_column_names(BattlesDatabase)
        keyboard = [[InlineKeyboardButton(col, callback_data=f'unique_{col}')] for col in columns]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Select a column to show unique values:", reply_markup=reply_markup)
    elif query.data.startswith('search_'):
        column = query.data.split('_')[1]
        context.user_data['search_column'] = column
        await query.edit_message_text(f"Enter a value to search in the {column} column:")
    elif query.data.startswith('unique_'):
        column = query.data.split('_')[1]
        unique_values = get_unique_values(BattlesDatabase, column)
        await query.edit_message_text(f"Unique values in {column}:\n{', '.join(map(str, unique_values))}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'search_column' in context.user_data:
        column = context.user_data['search_column']
        value = update.message.text
        results = search_csv(BattlesDatabase, column, value)
        if not results.empty:
            response = f"Found {len(results)} results:\n\n"
            response += results.to_string(index=False)
            if len(response) > 4096:  # Telegram message length limit
                response = response[:4093] + "..."
            await update.message.reply_text(response)
        else:
            await update.message.reply_text("No matching results found.")
        del context.user_data['search_column']
    else:
        await update.message.reply_text("Please use the /start command to interact with the bot.")

if __name__ == '__main__':
    application = ApplicationBuilder().token('**********').build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()