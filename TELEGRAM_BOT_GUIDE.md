# 🤖 Telegram Bot Setup & Deployment Guide

## 📋 What This Bot Does

✅ User sends `/start` command  
✅ Bot asks for Instagram reset link  
✅ User sends reset link  
✅ Bot changes password and sends **only the new password**  
✅ Simple, clean, minimal responses  

---

## 🔧 Part 1: Create Telegram Bot

### Step 1: Open Telegram and Create a Bot

1. Open Telegram app
2. Search for **@BotFather**
3. Click Start or type `/start`
4. Type `/newbot`
5. BotFather asks for bot name:
   - **Name:** Instagram Password Reset Bot (or any name)
6. BotFather asks for username:
   - **Username:** instagram_reset_bot (or any unique name ending with `_bot`)
7. **Copy the BOT TOKEN** (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

**Save this token! You need it!**

---

## 🚀 Part 2: Setup & Run Locally

### Step 1: Install Python
- Download from python.org
- During installation, check "Add Python to PATH"

### Step 2: Create Project Folder
```bash
mkdir telegram-bot
cd telegram-bot
```

### Step 3: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r telegram_requirements.txt
```

### Step 5: Setup .env File
Create a file named `.env` in your project folder:

```
BOT_TOKEN=your_bot_token_here
```

**Replace `your_bot_token_here` with your actual bot token from BotFather!**

### Step 6: Run the Bot
```bash
python telegram_bot.py
```

You should see:
```
==================================================
🤖 Instagram Password Reset Telegram Bot
==================================================
✅ Bot is running! Send /start to begin.
==================================================
```

### Step 7: Test the Bot
1. Open Telegram
2. Search for your bot name (e.g., @instagram_reset_bot)
3. Click Start
4. Type `/start`
5. Bot should ask for reset link
6. Paste your Instagram reset link
7. Bot returns the new password!

---

## 🌐 Part 3: Deploy to Cloud

### Option 1: **Replit (Easiest - Recommended)**

1. Go to **replit.com**
2. Sign up or login
3. Click "Create Repl"
4. Select "Python" as language
5. Upload your files:
   - `telegram_bot.py`
   - `telegram_requirements.txt`
   - `.env` (with your bot token)
6. Click the "Run" button
7. Bot will start running 24/7!

**Advantages:**
- ✅ Free
- ✅ 24/7 uptime
- ✅ No setup needed
- ✅ Can keep terminal open in background

---

### Option 2: **Railway.app (Professional)**

1. Go to **railway.app**
2. Sign up with GitHub
3. Create new project → Deploy from GitHub
4. Select your repository
5. In Railway dashboard:
   - Go to Variables
   - Add `BOT_TOKEN` and paste your token
6. Railway auto-deploys when you push to GitHub
7. Bot runs 24/7!

**Setup: Create `Procfile`**
```
worker: python telegram_bot.py
```

**Advantages:**
- ✅ Professional hosting
- ✅ Auto-deploy on GitHub push
- ✅ 24/7 uptime
- ✅ Better than Replit for production

---

### Option 3: **PythonAnywhere (Simple)**

1. Go to **pythonanywhere.com**
2. Create account
3. Upload files via their web interface
4. Create new "Web app" → Python 3.10
5. Edit the WSGI file (leave as is)
6. Set up a scheduled task:
   - Go to "Tasks"
   - New scheduled task
   - Run at daily: `python /home/yourname/telegram_bot.py`
7. "Always-on" feature (paid) keeps bot running 24/7

**Advantages:**
- ✅ Python-specific
- ✅ Easy to use
- ✅ 24/7 uptime (with paid plan)

---

### Option 4: **Heroku (Classic)**

1. Install Heroku CLI
2. Create account at **heroku.com**
3. In your project folder:

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Set bot token
heroku config:set BOT_TOKEN=your_actual_token_here

# Create Procfile
echo "worker: python telegram_bot.py" > Procfile

# Deploy
git push heroku main
```

4. Bot runs on Heroku's free tier!

---

## 📱 How Users Use Your Bot

### User Experience:
```
User: /start

Bot: 🔐 Instagram Password Reset Bot

Send me your Instagram reset link and I'll change the password for you.

📝 How to get reset link:
1. Go to Instagram login page
2. Click 'Forgot password?'
3. Enter your email
4. Check your email for reset link
5. Copy the link and paste it here

⏳ Waiting for your reset link...

User: https://instagram.com/accounts/password/reset/uidb36=XYZ&token=ABC:DEF

Bot: ⏳ Processing... Please wait...
(after processing)
Bot: ✅ Password Changed Successfully

NewPassword123!

[What would you like to do?]
[🔄 Try Another Reset] [❌ Exit]
```

---

## 🔐 Security Tips

### ⚠️ Important:
- **NEVER** share your `BOT_TOKEN`
- Keep `.env` file **private** (don't upload to GitHub)
- Use `.gitignore` file:
```
.env
venv/
__pycache__/
*.pyc
```

### Best Practices:
1. Always use environment variables for secrets
2. Don't hardcode tokens in code
3. Use `.env` for local development
4. Use platform's secrets manager for production

---

## 🐛 Troubleshooting

### "Bot token not found"
- Check `.env` file exists in same folder as `telegram_bot.py`
- Make sure `BOT_TOKEN=` has your actual token
- Restart the bot

### "Bot doesn't respond"
- Make sure bot is running (check console for errors)
- Check internet connection
- Try `/start` again in Telegram

### "Timeout errors"
- Instagram API is slow
- Bot will retry automatically
- User should try with different reset link

### "ModuleNotFoundError"
```bash
# Install missing package
pip install python-telegram-bot
```

---

## 📞 Getting Your Bot Token (Step-by-Step)

1. **Open Telegram** (mobile app or web.telegram.org)
2. **Search:** @BotFather
3. **Send:** `/start`
4. **Send:** `/newbot`
5. **Give bot name:** "Instagram Reset Bot"
6. **Give bot username:** "instagram_reset_bot_123" (must end with `_bot`)
7. **Copy the token** that BotFather sends
8. **Paste in `.env` file**

---

## 🚀 Quick Deployment Checklist

- [ ] Create bot with @BotFather and copy token
- [ ] Create `.env` file with `BOT_TOKEN=your_token`
- [ ] Install dependencies: `pip install -r telegram_requirements.txt`
- [ ] Test locally: `python telegram_bot.py`
- [ ] Choose hosting platform (Replit recommended)
- [ ] Deploy and set bot token in platform's settings
- [ ] Test bot in Telegram with `/start`
- [ ] Keep running 24/7! ✅

---

## 📚 Next Steps

1. ✅ Get bot working locally
2. ✅ Deploy to cloud
3. ✅ Share bot with friends/users
4. ✅ Add more features (logging, stats, etc.)
5. ✅ Improve error handling
6. ✅ Scale up usage

---

## 🎓 What You Learned

✅ How to create a Telegram bot  
✅ How conversational bots work (ConversationHandler)  
✅ How to handle user input and state  
✅ How to make API calls from bot  
✅ **How to deploy a bot to the cloud 24/7** ⭐  

**Congratulations! You're building Telegram bots! 🎉**

---

## 🆘 Need More Help?

- **Telegram Bot API Docs:** core.telegram.org
- **python-telegram-bot Docs:** python-telegram-bot.readthedocs.io
- **Stack Overflow:** Search "telegram bot python"
- **YouTube:** Search "python telegram bot tutorial"

---

**Happy botting! 🤖**
