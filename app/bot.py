# app/bot.py
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello from the bot!")

app.add_handler(CommandHandler("start", start))

def run_telegram_bot():
    app.run_polling()
