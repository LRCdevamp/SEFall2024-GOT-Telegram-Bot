import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import pandas as pd
from PandaDatabaseFunctions import *

BattlesDatabase = 'battles.csv'
CharactersDeathesDatabase = 'character-deaths.csv'
CharactersPredictions = 'character-predictions.csv'
global battle_names
battle_names =  get_battles_names(BattlesDatabase)
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
    await update.message.reply_text('درمورد چی برات بگم؟', reply_markup=reply_markup)
    

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'BackToMainMenu':
        keyboard = [[InlineKeyboardButton("جستجوی تاریخچه جنگ‌ها", callback_data='Battles')],
                    [InlineKeyboardButton("جستجوی تاریخچه شخصیت‌ها", callback_data='Characters')],
                    [InlineKeyboardButton("جستجوی تاریخچه مرگ شخصیت‌ها", callback_data='Deaths')]]   
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("خب برگشتم! حالا درمورد چی برات بگم؟", reply_markup=reply_markup)

    elif query.data == 'Battles':
        keyboard = [[InlineKeyboardButton(col, callback_data=col)] for col in get_battles_names(BattlesDatabase)]
        keyboard.append([InlineKeyboardButton('بازگشت به منو اصلی',callback_data='BackToMainMenu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("در مورد کدوم جنگ میخوای بیشتر بدونی؟", reply_markup=reply_markup)

    elif query.data in get_battles_names(BattlesDatabase):
        battle_Index = battle_names.index(query.data)
        keyboard = [[InlineKeyboardButton('بازگشت به منو اصلی',callback_data='BackToMainMenu')],
                    [InlineKeyboardButton("جنگ بعدی",callback_data='{battleName}'.format(battleName=battle_names[battle_Index+1] if battle_Index != 37 else battle_names[0]))],                    [InlineKeyboardButton("بازگشت به لیست جنگ‌ها", callback_data='Battles')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        entry = get_entry(BattlesDatabase,battle_Index)
        await query.edit_message_text("نام جنگ: {name}\nسال وقوع جنگ: {year}\nپادشاه حمله‌کننده: {attacker_king}\nپادشاه مدافع: {defender_king}".format(name=query.data,year=entry.year,attacker_king = entry.attacker_king,defender_king = entry.defender_king),reply_markup=reply_markup)

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
    application = ApplicationBuilder().token('*********************').build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()