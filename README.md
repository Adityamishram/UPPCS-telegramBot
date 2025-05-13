
# UPSC Quiz Telegram Bot

This is a Telegram quiz bot for UPSC-style MCQs using data from January 2025.

## 🚀 How to Deploy on Render

1. Create a bot using [@BotFather](https://t.me/BotFather) and get your token.

2. Fork or upload this repo to GitHub.

3. Go to [https://render.com](https://render.com), create a new Web Service:
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python quiz_bot.py`

4. Add this Environment Variable:
   - `TELEGRAM_BOT_TOKEN=7453734359:AAEeBffcPyw_mvi0qgrqNo8gEj5gfw7sNmw`

That's it! The bot will be live and respond to /start on Telegram.

## 🧪 Sample Questions

The bot currently supports 600 UPSC questions. Start the quiz with `/start`.
