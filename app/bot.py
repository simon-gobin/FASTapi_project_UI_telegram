# app/bot.py
from dotenv import load_dotenv
import os

from roleplay_assistant import JSON_manager, RoleplayAssistant
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import roleplay_assistant

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def get_user_json_path(update: Update) -> str:
    user_id = str(update.effective_user.id)
    return f"user_data/{user_id}_story.json"

def get_json_manager(update: Update) -> JSON_manager:
    json_path = get_user_json_path(update)
    manager = JSON_manager(json_path)
    return manager


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    user = update.effective_user
    manager = get_json_manager(update)
    manager.create_json()

    keyboard = [
        [
            InlineKeyboardButton("🇬🇧", callback_data="en"),
            InlineKeyboardButton("🇫🇷", callback_data="fr"),
        ],
        [InlineKeyboardButton("🇪🇸", callback_data="es")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(rf"Hi {user.first_name}! It's your first time here. We'll create a story together. "
    rf"Please choose your language : " , reply_markup=reply_markup)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    manager = get_json_manager(update)
    manager.reset_json()
    manager.create_json()
    await update.message.reply_text(rf"Hi {user.first_name}! Let restart again please typing /start for choose you language ")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    manager = get_json_manager(update)
    manager.update_state("Language", query.data)
    await query.edit_message_text(text=f"Selected option: {query.data}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def set_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set up the JSON if first interaction"""
    await update.message.reply_text(roleplay_assistant.set_up())




async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_response = update.message.text.strip()
    user_id = str(user.id)
    json_path = f"user_data/{user_id}_story.json"

    assistant = RoleplayAssistant(json_path)
    manager = assistant.manager

    # Step 1: Store user reply into JSON
    if not manager.story_state["User Character"]:
        manager.update_state("User Character", user_response)
        assistant.add_user_message(user_response)
    elif not manager.story_state["System Character"]:
        manager.update_state("System Character", user_response)
        assistant.add_user_message(user_response)
    elif not manager.story_state["Situation"]:
        manager.update_state("Situation", user_response)
        assistant.add_user_message(user_response)
    else:
        # Setup complete
        assistant.add_user_message(user_response)
        await update.message.reply_text("🎬 Story setup complete. Let’s begin!")
        return

    # Step 2: Ask next question (from Qwen3)
    assistant_reply = assistant.get_next_prompt()
    if assistant_reply:
        assistant.add_assistant_message(assistant_reply)
        await update.message.reply_text(assistant_reply)




def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reset", reset))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()