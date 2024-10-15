import logging
import re
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
        keyboard = [[InlineKeyboardButton(word, callback_data=f'{word},0')] for word in string.ascii_uppercase]
        keyboard.append([InlineKeyboardButton('بازگشت به منو اصلی',callback_data='BackToMainMenu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("از اونجایی که دو هزار تا کارکتر داریم، حرف اول کارکترت رو انتخاب کن", reply_markup=reply_markup)

    elif re.match(r'^[A-Z],[0-9]$', query.data):
        letter, number = query.data.split(',')
        keyboard = [[InlineKeyboardButton(name,callback_data=name)] for name in get_characters_name(CharactersPredictions,letter)[int(number)]]
        keyboard.append([InlineKeyboardButton("صفحه بعدی", callback_data=(f'{letter},{int(number)+1}')if int(number)!=(len(get_characters_name(CharactersPredictions,letter))-1) else (f'{letter},{0}'))])
        keyboard.append([InlineKeyboardButton("صفحه قبلی", callback_data=(f'{letter},{int(number)-1}')if int(number)!= 0 else (f'{letter},{len(get_characters_name(CharactersPredictions,letter))-1}'))])
        keyboard.append([InlineKeyboardButton("بازگشت به لیست حروف", callback_data='Characters')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"مجموعا {get_characters_names_length(CharactersPredictions,letter)} تا اسم داریم که با این حرف شروع میشن.\n این صفحه {int(number)+1} از {len(get_characters_name(CharactersPredictions,letter))}صفحه‌ست!",reply_markup=reply_markup)

    elif query.data in get_names_from_characters(CharactersPredictions):
        keyboard = [[InlineKeyboardButton('بازگشت به منو اصلی',callback_data='BackToMainMenu')],
                    [InlineKeyboardButton(f"بازگشت به لیست کارکترهای حرف {query.data[0]}", callback_data=(f'{query.data[0]},0'))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        character_Index = get_names_from_characters(CharactersPredictions).index(query.data)
        entry = get_entry(CharactersPredictions,character_Index)

        await query.edit_message_text(
            "نام شخصیت: {name}\n"
            "لقب شخصیت: {title}\n"
            "جنسیت شخصیت: {male}\n"
            "خواستگاه فرهنگی شخصیت: {culture}\n"
            "سال تولد: {dateOfBirth}\n"
            "سال مرگ: {dateOfDeath}\n"
            "نام پدر: {father}\n"
            "نام مادر: {mother}\n"
            "جانشین: {heir}\n"
            "خاندان : {house}\n"
            "نام همسر: {spouse}\n"
            "آیا فرد از خانواده اشرافی است؟ {isNoble}\n"
            "آیا فرد ازدواج کرده است؟ {isMarried}\n"
            "سن: {age}\n"
            "آیا شخصیت تا انتهای آخرین کتاب، زنده است؟ {isAlive}\n".format(
                name = query.data,
                title=entry.title if entry.title != 'none' else 'ندارد',
                male = "مرد" if entry.male == 1 else 'زن',
                culture = entry.culture if entry.culture != 'none' else 'نامشخص',
                dateOfBirth = entry.dateOfBirth if entry.dateOfBirth != 'none' else 'نامشخص',
                dateOfDeath = entry.DateoFdeath if entry.DateoFdeath != 'none' else 'نامشخص',
                father = entry.father if entry.father != 'none' else 'نامشخص',
                mother = entry.mother if entry.mother != 'none' else 'نامشخص',
                heir = entry.heir if entry.heir!= 'none' else 'ندارد',
                house = entry.house if entry.house != 'none' else 'نامشخص',
                spouse = entry.spouse if entry.spouse != 'none' else 'ندارد',
                isNoble = 'بله' if entry.isNoble == 1 else 'خیر',
                isMarried = 'بله' if entry.isMarried == 1 else 'خیر',
                age = entry.age if entry.age != 'none' else 'نامشخص',
                isAlive = 'بله' if entry.isAlive == 1 else 'خیر')
            ,reply_markup=reply_markup)

    elif query.data in get_battles_names(BattlesDatabase):
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

    elif query.data == 'Deaths':
        keyboard = [[InlineKeyboardButton(word, callback_data=f'death,{word},0')] for word in string.ascii_uppercase]
        keyboard.append([InlineKeyboardButton('بازگشت به منو اصلی',callback_data='BackToMainMenu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("دقیقا 917 تا مرگ تو کتاب‌ها ثبت شده. برای اینکه راحت‌تر بتونی شخصیت مورد نظرت رو پیدا کنی، حرف اول اسمش رو انتخاب کن.", reply_markup=reply_markup)

    elif re.match(r'^death,[A-Z],[0-9]$',query.data):
        death, letter, number = query.data.split(',')
        keyboard = [[InlineKeyboardButton(name,callback_data=f'{name},death')] for name in get_names_from_deaths(CharactersDeathesDatabase,letter)[int(number)]]
        keyboard.append([InlineKeyboardButton("صفحه بعدی", callback_data=(f'death,{letter},{int(number)+1}')if int(number)!=(len(get_names_from_deaths(CharactersDeathesDatabase,letter))-1) else (f'death,{letter},{0}'))])
        keyboard.append([InlineKeyboardButton("صفحه قبلی", callback_data=(f'death,{letter},{int(number)-1}')if int(number)!= 0 else (f'death,{letter},{len(get_names_from_deaths(CharactersDeathesDatabase,letter))-1}'))])
        keyboard.append([InlineKeyboardButton("بازگشت به لیست حروف", callback_data='Deaths')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"مجموعا {get_characters_deaths_length(CharactersDeathesDatabase,letter)} تا اسم داریم که با این حرف شروع میشن.\n این صفحه {int(number)+1} از {len(get_names_from_deaths(CharactersDeathesDatabase,letter))}صفحه‌ست!",reply_markup=reply_markup)

    elif query.data.endswith(',death'):
        name,death = query.data.split(',')
        keyboard = [[InlineKeyboardButton('بازگشت به منو اصلی',callback_data='BackToMainMenu')],
                    [InlineKeyboardButton(f"بازگشت به لیست کارکترهای حرف {name[0]}", callback_data=(f'death,{name[0]},0'))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
    
        character_Index = get_all_names_from_deaths(CharactersDeathesDatabase).index(name)
        entry = get_entry(CharactersDeathesDatabase,character_Index)

        await query.edit_message_text(
            "نام شخصیت: {name}\n"
            "این شخصیت به چه خاندانی وفادار بود؟ {Alligiances}\n"
            "جنسیت شخصیت: {gender}\n"
            "سال مرگ: {deathYear}\n"
            "این شخصیت در کتاب چندم مرد؟ {BookOfDeath}\n"
            "این شخصیت در کدام قسمت کتاب بالا مرد؟ {DeathChapter}\n"
            "این شخصیت در کدام قسمت برای اولین بار حضور پیدا کرد؟ {BookIntroChapter}\n"
            "آیا این شخصیت در کتاب Game Of Thrones بود؟: {GoT}\n"
            "آیا این شخصیت در کتاب Clash of Kinds بود؟: {CoK}\n"
            "آیا این شخصیت در کتاب Storm of Swords بود؟: {SoS}\n"
            "آیا این شخصیت در کتاب Feast for Crows بود؟: {FfC}\n"
            "آیا این شخصیت در کتاب Dance with Dragons بود؟: {DwD}\n"
            .format(
                name = name,
                Alligiances = entry.Allegiances if entry.Allegiances != "none" else 'این شخصیت به هیچ خاندانی وفادار نبود.',
                gender = "مرد" if entry.Gender == 1 else 'زن',
                deathYear = entry.DeathYear if entry.DeathYear != 'none' else 'نامشخص',
                BookOfDeath = entry.BookofDeath if entry.BookofDeath != 'none' else 'نامشخص',
                DeathChapter = entry.DeathChapter if entry.DeathChapter != 'none' else 'نامشخص',
                BookIntroChapter = entry.BookIntroChapter if entry.BookIntroChapter!= 'none' else 'نامشخص',
                GoT = 'بله' if entry.GoT == 1 else 'خیر',
                CoK = 'بله' if entry.CoK == 1 else 'خیر',
                SoS = 'بله' if entry.SoS == 1 else 'خیر',
                FfC = 'بله' if entry.FfC == 1 else 'خیر',
                DwD = 'بله' if entry.DwD == 1 else 'خیر')
            ,reply_markup=reply_markup)



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
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()