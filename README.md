# Telegram Grocery List Bot

A simple Telegram bot that helps you manage a shared grocery list. Users can add, remove, view, and clear items from the list.

## Features

- ➕ **Add Items** - Add items to your grocery list
- ➖ **Remove Items** - Remove specific items by number
- 📋 **View List** - Display all current items
- 🗑️ **Clear List** - Remove all items at once
- Persistent storage - List persists between bot restarts
- Easy button interface - No need to type commands

## Prerequisites

- Python 3.11+
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))
- Railway Account (for deployment)

## Local Setup

1. Clone or download the repository

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Set your bot token:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

4. Run the bot:
```bash
python main.py
```

## Railway Deployment

1. Create a [Railway](https://railway.app) account

2. Connect your GitHub repository or deploy directly:
   - Option A: Push your code to GitHub and connect the repo to Railway
   - Option B: Use Railway CLI for direct deployment

3. Create a new Railway project:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub" or "CLI"

4. Set environment variables:
   - In Railway dashboard, go to Variables
   - Add: `TELEGRAM_BOT_TOKEN="your_bot_token_here"`

5. Railway will automatically deploy when you push to GitHub

6. View logs:
   - In Railway dashboard under "Logs" tab
   - Or use Railway CLI: `railway logs`

### Deploy with Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize and deploy
railway init
railway up
```

## Using the Bot

1. Find your bot on Telegram (search by the name you gave it)

2. Send `/start` to begin

3. Use the button interface to:
   - **Add Item**: Click the button and type the item name
   - **Remove Item**: Click the button and select the item number
   - **Show List**: View all items
   - **Clear List**: Remove all items
Railway, this file will be stored in the app's ephemeral filesystem, meaning it will be reset when the app restarts. For persistent storage across restarts, consider upgrading to use a database like PostgreSQL.

## Notes

- The grocery list is shared among all users of the bot
- Items are stored locally in `grocery_list.json`
- Railway provides free tier with generous limits
- For production use, consider migrating to a persistent database

The grocery list is stored in a JSON file (`grocery_list.json`). When deployed to Heroku, this file will be stored in the app's ephemeral filesystem, meaning it will be reset when the app restarts. For persistent storage across dyno restarts, consider upgrading to use a database like PostgreSQL.

## Notes

- The grocery list is shared among all users of the bot
- Items are stored locally in `grocery_list.json`
- Heroku's free tier has limitations - the app may sleep if inactive for 30 minutes
