# 🚀 Quick Start - Just Copy & Paste!

## For Windows Users:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate

# 3. Install dependencies
pip install -r telegram_requirements.txt

# 4. Run the bot
python telegram_bot.py
```

## For Mac/Linux Users:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r telegram_requirements.txt

# 4. Run the bot
python telegram_bot.py
```

## ⚠️ BEFORE RUNNING:

**Create a `.env` file in the same folder with:**

```
BOT_TOKEN=your_bot_token_here
```

**Get your token from @BotFather on Telegram!**

---

## How to Get Bot Token (5 Steps):

1. Open Telegram
2. Search for **@BotFather**
3. Type `/newbot`
4. Give it a name (e.g., "Instagram Reset Bot")
5. Give it a username ending with `_bot` (e.g., "insta_reset_bot")
6. Copy the token BotFather gives you
7. Paste it in `.env` file

---

## Test Your Bot:

1. Run: `python telegram_bot.py`
2. See message: "✅ Bot is running! Send /start to begin."
3. Open Telegram
4. Search for your bot
5. Type `/start`
6. Bot should respond!

---

## Deploy to Replit (Easy):

1. Go to replit.com
2. Click "Create Repl" → Python
3. Upload your files:
   - telegram_bot.py
   - telegram_requirements.txt
   - .env
4. Click "Run"
5. Bot runs 24/7 automatically!

---

## Commands in Telegram:

- `/start` - Start password reset
- `/help` - Show help
- `/cancel` - Cancel operation

---

**That's it! Your bot is ready! 🎉**
