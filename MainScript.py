import logging
import string
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


    elif query.data == 'Characters':
        keyboard = [[InlineKeyboardButton(word, callback_data=word)] for word in string.ascii_uppercase]
        keyboard.append([InlineKeyboardButton('بازگشت به منو اصلی',callback_data='BackToMainMenu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("از اونجایی که دو هزار تا کارکتر داریم، حرف اول کارکترت رو انتخاب کن", reply_markup=reply_markup)


    elif query.data in get_battles_names(BattlesDatabase):
        get_battles_names(BattlesDatabase)
        keyboard = [[InlineKeyboardButton('بازگشت به منو اصلی',callback_data='BackToMainMenu')],
                    [InlineKeyboardButton("جنگ بعدی", callback_data='NextBattle')],
                    [InlineKeyboardButton("بازگشت به لیست جنگ‌ها", callback_data='Battles')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        battle_Index = battle_names.index(query.data)
        entry = get_entry(BattlesDatabase,battle_Index)
        await query.edit_message_text(
                    "نام جنگ: {name}\n"
                    "سال وقوع جنگ: {year}\n"
                    "پادشاه حمله‌کننده: {attacker_king}\n"
                    "پادشاه مدافع: {defender_king}\n"
                    "حمله‌کننده اول: {attacker_1}\n"
                    "{attacker_2}"
                    "{attacker_3}"
                    "{attacker_4}"
                    "مدافع اول: {defender_1}\n"
                    "{defender_2}"
                    "{defender_3}"
                    "{defender_4}"
                    "نتیجه برای حمله‌کننده: {attacker_outcome}\n"
                    "نوع جنگ: {battle_type}\n"
                    "آیا این جنگ منجر به مرگ فرد مهمی شد؟ {major_death}\n"
                    "آیا این جنگ منجر به تصرف استراتژیک منطقه‌ای شد؟ {major_capture}\n"
                    "تعداد نفرات سپاه حمله‌کننده: {attacker_size}\n"
                    "تعداد نفرات سپاه مدافع: {defender_size}\n"
                    "فرمانده سپاه حمله‌کننده: {attacker_commander}\n"
                    "فرمانده سپاه مدافع: {defender_commander}\n"
                    "آیا این جنگ در تابستان بوقوع پیوست؟ {summer}\n"
                    "محل وقوع جنگ: {location}\n"
                    "منطقه وقوع جنگ: {region}".format(
                        name=query.data,
                        year=entry.year,
                        attacker_king=entry.attacker_king,
                        defender_king=entry.defender_king,
                        attacker_1=entry.attacker_1,
                        attacker_2=f"حمله‌کننده دوم: {entry.attacker_2}\n" if entry.attacker_2 != 'none' else "",
                        attacker_3=f"حمله‌کننده سوم: {entry.attacker_3}\n" if entry.attacker_3 != 'none' else "",
                        attacker_4=f"حمله‌کننده چهارم: {entry.attacker_4}\n" if entry.attacker_4 != 'none' else "",
                        defender_1=entry.defender_1,
                        defender_2=f"مدافع دوم: {entry.defender_2}\n" if entry.defender_2 != 'none' else "",
                        defender_3=f"مدافع سوم: {entry.defender_3}\n" if entry.defender_3 != 'none' else "",
                        defender_4=f"مدافع چهارم: {entry.defender_4}\n" if entry.defender_4 != 'none' else "",
                        attacker_outcome='پیروزی' if entry.attacker_outcome == 'win' else 'شکست' ,
                        battle_type=entry.battle_type,
                        major_death='بله' if entry.major_death == 1 else 'خیر',
                        major_capture='بله' if entry.major_capture == 1 else 'خیر',
                        attacker_size=int(entry.attacker_size) if entry.attacker_size != 'none' else 'نامشخص',
                        defender_size=int(entry.defender_size)if entry.defender_size != 'none' else 'نامشخص',
                        attacker_commander=entry.attacker_commander,
                        defender_commander=entry.defender_commander,
                        summer='ّبله' if entry.attacker_outcome == 1 else 'خیر',
                        location=entry.location,
                        region=entry.region),reply_markup=reply_markup)





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
    application = ApplicationBuilder().token('7890270186:AAFzK49GuzNLKcGyiYunxkS1InhGCELeJds').build()
    application = ApplicationBuilder().token('**********************').build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()