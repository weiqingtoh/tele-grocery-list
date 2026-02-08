#!/usr/bin/env python3
"""
Telegram Grocery List Bot
A simple bot to manage a shared grocery list.
"""

import os
import json
import logging
from typing import Optional
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# File to store the grocery list
GROCERY_FILE = "grocery_list.json"

# Keyboard markup for easy interaction
def get_keyboard():
    keyboard = [
        [KeyboardButton("➕ Add Item"), KeyboardButton("➖ Remove Item")],
        [KeyboardButton("📋 Show List"), KeyboardButton("🗑️ Clear List")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def load_grocery_list() -> list:
    """Load the grocery list from file."""
    if os.path.exists(GROCERY_FILE):
        try:
            with open(GROCERY_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_grocery_list(items: list) -> None:
    """Save the grocery list to file."""
    with open(GROCERY_FILE, 'w') as f:
        json.dump(items, f, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler."""
    await update.message.reply_text(
        "🛒 Welcome to Grocery List Bot!\n\n"
        "Use the buttons below to manage your grocery list:",
        reply_markup=get_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler."""
    help_text = (
        "📖 *Available Commands:*\n\n"
        "➕ *Add Item* - Add an item to the list\n"
        "➖ *Remove Item* - Remove an item from the list\n"
        "📋 *Show List* - Display all items\n"
        "🗑️ *Clear List* - Remove all items\n"
        "/start - Start the bot\n"
        "/help - Show this message"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def show_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the current grocery list."""
    items = load_grocery_list()
    
    if not items:
        await update.message.reply_text(
            "📋 Your grocery list is empty!",
            reply_markup=get_keyboard()
        )
    else:
        list_text = "📋 *Your Grocery List:*\n\n"
        for i, item in enumerate(items, 1):
            list_text += f"{i}. {item}\n"
        await update.message.reply_text(list_text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_keyboard())

async def add_item_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start adding an item."""
    context.user_data['action'] = 'add_item'
    await update.message.reply_text(
        "✏️ What item would you like to add?",
        reply_markup=ReplyKeyboardMarkup([["Cancel"]], resize_keyboard=True)
    )

async def remove_item_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start removing an item."""
    items = load_grocery_list()
    
    if not items:
        await update.message.reply_text(
            "📋 Your grocery list is empty!",
            reply_markup=get_keyboard()
        )
    else:
        list_text = "🗑️ *Select item to remove:*\n\n"
        for i, item in enumerate(items, 1):
            list_text += f"{i}. {item}\n"
        context.user_data['action'] = 'remove_item'
        keyboard = [[KeyboardButton(str(i))] for i in range(1, len(items) + 1)]
        keyboard.append([KeyboardButton("Cancel")])
        await update.message.reply_text(
            list_text + "\nEnter the number of the item to remove:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

async def clear_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear the entire grocery list."""
    save_grocery_list([])
    await update.message.reply_text(
        "🗑️ Grocery list cleared!",
        reply_markup=get_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages and button presses."""
    text = update.message.text.strip()
    action = context.user_data.get('action')
    
    # Handle button presses
    if text == "➕ Add Item":
        await add_item_start(update, context)
    elif text == "➖ Remove Item":
        await remove_item_start(update, context)
    elif text == "📋 Show List":
        await show_list(update, context)
    elif text == "🗑️ Clear List":
        await clear_list(update, context)
    elif text == "Cancel":
        context.user_data.pop('action', None)
        await update.message.reply_text(
            "Operation cancelled.",
            reply_markup=get_keyboard()
        )
    # Handle adding item
    elif action == 'add_item':
        items = load_grocery_list()
        if text not in items:
            items.append(text)
            save_grocery_list(items)
            await update.message.reply_text(
                f"✅ Added: {text}",
                reply_markup=get_keyboard()
            )
        else:
            await update.message.reply_text(
                f"⚠️ '{text}' is already in the list!",
                reply_markup=get_keyboard()
            )
        context.user_data.pop('action', None)
    # Handle removing item
    elif action == 'remove_item':
        try:
            index = int(text) - 1
            items = load_grocery_list()
            if 0 <= index < len(items):
                removed = items.pop(index)
                save_grocery_list(items)
                await update.message.reply_text(
                    f"✅ Removed: {removed}",
                    reply_markup=get_keyboard()
                )
            else:
                await update.message.reply_text(
                    "❌ Invalid item number!",
                    reply_markup=get_keyboard()
                )
        except ValueError:
            await update.message.reply_text(
                "❌ Please enter a valid number!",
                reply_markup=get_keyboard()
            )
        context.user_data.pop('action', None)

def main() -> None:
    """Start the bot."""
    # Get bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
