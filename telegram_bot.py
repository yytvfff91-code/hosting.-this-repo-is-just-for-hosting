import os
import random
import string
import uuid
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# States for conversation
WAITING_FOR_LINK = 1

# Get bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not set in .env file!")

class PasswordResetBot:
    """Telegram bot for Instagram password reset"""
    
    @staticmethod
    def generate_instagram_password():
        """Generate a random Instagram-like password"""
        words = ['hello', 'insta', 'random', 'python', 'secure', 'cloud', 'deploy', 'server', 'api', 'flask']
        formats = [
            lambda w, n: f"{w}{n}!",
            lambda w, n: f"{w}{n}@",
            lambda w, n: f"{w}{n}#",
            lambda w, n: f"{w}_{n}",
            lambda w, n: f"{w}{n}&",
        ]
        word = random.choice(words)
        numbers = ''.join([str(random.randint(0, 9)) for _ in range(3)])
        format_func = random.choice(formats)
        password = format_func(word, numbers)
        
        while len(password) < 6:
            password += str(random.randint(0, 9))
        
        return password

    @staticmethod
    def generate_device_info():
        """Generate device information for API calls"""
        ANDROID_ID = f"android-{''.join(random.choices(string.hexdigits.lower(), k=16))}"
        timestamp = int(datetime.now().timestamp())
        WATERFALL_ID = str(uuid.uuid4())
        PASSWORD = f'#PWD_INSTAGRAM:0:{timestamp}:{PasswordResetBot.generate_instagram_password()}'
        
        return ANDROID_ID, WATERFALL_ID, PASSWORD

    @staticmethod
    def make_headers(mid=""):
        """Create API headers"""
        return {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Bloks-Version-Id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
            "X-Mid": mid,
        }

    @staticmethod
    def reset_instagram_password(reset_link):
        """Process Instagram password reset"""
        try:
            ANDROID_ID, WATERFALL_ID, PASSWORD = PasswordResetBot.generate_device_info()
            
            # Extract parameters from reset link
            uidb36 = reset_link.split("uidb36=")[1].split("&token=")[0]
            token = reset_link.split("&token=")[1].split(":")[0]

            # First API call
            url = "https://i.instagram.com/api/v1/accounts/password_reset/"
            data = {
                "source": "one_click_login_email",
                "uidb36": uidb36,
                "device_id": ANDROID_ID,
                "token": token,
                "waterfall_id": WATERFALL_ID
            }
            
            r = requests.post(url, headers=PasswordResetBot.make_headers(), data=data, timeout=10)

            if "user_id" not in r.text:
                return {"success": False, "error": "Invalid reset link"}

            mid = r.headers.get("Ig-Set-X-Mid", "")
            resp_json = r.json()
            user_id = resp_json.get("user_id")
            cni = resp_json.get("cni")
            nonce_code = resp_json.get("nonce_code")
            challenge_context = resp_json.get("challenge_context")

            # Second API call
            url2 = "https://i.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/"
            data2 = {
                "user_id": str(user_id),
                "cni": str(cni),
                "nonce_code": str(nonce_code),
                "bk_client_context": '{"bloks_version":"e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd","styles_id":"instagram"}',
                "challenge_context": str(challenge_context),
                "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
                "get_challenge": "true"
            }
            
            r2 = requests.post(url2, headers=PasswordResetBot.make_headers(mid), data=data2, timeout=10).text

            # Extract challenge context
            challenge_context_final = r2.replace('\\', '').split(f'(bk.action.i64.Const, {cni}), "')[1].split('", (bk.action.bool.Const, false)))')[0]

            # Third API call - set new password
            data3 = {
                "is_caa": "False",
                "source": "",
                "uidb36": "",
                "error_state": {"type_name": "str", "index": 0, "state_id": 1048583541},
                "afv": "",
                "cni": str(cni),
                "token": "",
                "has_follow_up_screens": "0",
                "bk_client_context": {"bloks_version": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd", "styles_id": "instagram"},
                "challenge_context": challenge_context_final,
                "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
                "enc_new_password1": PASSWORD,
                "enc_new_password2": PASSWORD
            }

            requests.post(url2, headers=PasswordResetBot.make_headers(mid), data=data3, timeout=10)
            new_password = PASSWORD.split(":")[-1]

            return {
                "success": True,
                "password": new_password,
                "user_id": user_id
            }

        except IndexError:
            return {"success": False, "error": "❌ Invalid reset link format"}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "❌ Request timeout - try again"}
        except Exception as e:
            return {"success": False, "error": f"❌ Error: {str(e)[:50]}"}

# Bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - initiate password reset"""
    user = update.effective_user
    logger.info(f"User {user.id} started the bot")
    
    welcome_message = (
        "🔐 *Instagram Password Reset Bot*\n\n"
        "Send me your Instagram reset link and I'll change the password for you.\n\n"
        "📝 *How to get reset link:*\n"
        "1. Go to Instagram login page\n"
        "2. Click 'Forgot password?'\n"
        "3. Enter your email\n"
        "4. Check your email for reset link\n"
        "5. Copy the link and paste it here\n\n"
        "⏳ Waiting for your reset link..."
    )
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown')
    return WAITING_FOR_LINK

async def handle_reset_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle reset link submission"""
    user = update.effective_user
    reset_link = update.message.text.strip()
    
    logger.info(f"User {user.id} submitted a reset link")
    
    # Show processing message
    processing_msg = await update.message.reply_text("⏳ Processing... Please wait...")
    
    # Validate reset link format
    if "uidb36=" not in reset_link or "token=" not in reset_link:
        await processing_msg.edit_text("❌ Invalid reset link format. Please check and try again.")
        return WAITING_FOR_LINK
    
    # Process the reset
    result = PasswordResetBot.reset_instagram_password(reset_link)
    
    if result.get("success"):
        new_password = result.get("password")
        
        # Send only the password
        response = f"✅ *Password Changed Successfully*\n\n`{new_password}`"
        
        await processing_msg.edit_text(response, parse_mode='Markdown')
        logger.info(f"User {user.id} - Password reset successful")
        
        # Ask if they want to try again
        restart_keyboard = [['🔄 Try Another Reset', '❌ Exit']]
        reply_markup = ReplyKeyboardMarkup(restart_keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            "What would you like to do?",
            reply_markup=reply_markup
        )
        return WAITING_FOR_LINK
    
    else:
        error = result.get("error", "Unknown error")
        await processing_msg.edit_text(f"❌ {error}\n\nPlease try again.", parse_mode='Markdown')
        logger.error(f"User {user.id} - Reset failed: {error}")
        return WAITING_FOR_LINK

async def handle_button_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button responses"""
    text = update.message.text
    
    if text == "🔄 Try Another Reset":
        await update.message.reply_text(
            "📝 Send me another reset link:",
            reply_markup=ReplyKeyboardRemove()
        )
        return WAITING_FOR_LINK
    elif text == "❌ Exit":
        await update.message.reply_text(
            "👋 Thanks for using the bot! Type /start to begin again.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    
    return WAITING_FOR_LINK

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation"""
    await update.message.reply_text(
        "❌ Cancelled. Type /start to begin again.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    help_text = (
        "🤖 *Available Commands:*\n\n"
        "/start - Start password reset\n"
        "/help - Show this help message\n"
        "/cancel - Cancel current operation\n\n"
        "📌 *How it works:*\n"
        "1. Send /start\n"
        "2. Paste your Instagram reset link\n"
        "3. Get your new password immediately!\n"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Set up conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_FOR_LINK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reset_link),
            ]
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start),
        ],
    )

    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))

    # Start the bot
    logger.info("🤖 Bot is starting...")
    print("=" * 50)
    print("🤖 Instagram Password Reset Telegram Bot")
    print("=" * 50)
    print("✅ Bot is running! Send /start to begin.")
    print("=" * 50)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
