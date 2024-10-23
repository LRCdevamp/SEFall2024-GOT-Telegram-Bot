# SEFall2024-GOT-Telegram-Bot
This is a Telegram bot that was created as an example for the Software Engineering course project at Semnan University in the fall of 2024.
A Telegram bot that provides detailed information about Game of Thrones battles, characters, and deaths using data from Kaggle datasets. Get instant access to battle details, character information, and mortality data through an easy-to-use button interface.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Telegram-blue.svg)
![Panda](https://img.shields.io/badge/Pandas-2.2.3-150458.svg)


## Features

- 🗡️ Battle information lookup
- 👥 Character details and predictions
- 💀 Character death information
- 🔘 User-friendly button interface
- 📊 Data from curated Game of Thrones datasets

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/SEFall2024-GOT-Telegram-Bot.git
   cd SEFall2024-GOT-Telegram-Bot
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the bot**
   - Create a Telegram bot via [@BotFather](https://t.me/botfather)
   - Replace `YOUR_BOT_TOKEN` in `MainScript.py` with your token

5. **Run the bot**
   ```bash
   python MainScript.py
   ```

6. **Start using the bot**
   - Open Telegram
   - Find your bot
   - Send `/start` command
   - Use the button interface to explore data

## Data Sources

The bot uses modified CSV files from [Kaggle's Game of Thrones Dataset](https://www.kaggle.com/datasets/mylesoneill/game-of-thrones). Empty cells have been filled with 'none' for consistency.

## Documentation

For detailed information about:
- Complete installation instructions
- Configuration details
- Data structure
- Function reference
- Available commands

Please visit our [Wiki](https://github.com/LRCdevamp/SEFall2024-GOT-Telegram-Bot/wiki)

## Prerequisites

- Python 3.x
- Telegram account
