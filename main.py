import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8579048820:AAEdZzcN_5C2mYpZjsiBJHJyI0MQnvtxdBc"

# 1. Flask App banate hain taaki Render ka port open rahe
app = Flask('')

@app.route('/')
def home():
    return "Bot is running live on Render!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Telegram Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalam-o-Alaikum! Main Muhammad Parwez ka personal secure bot hoon.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(f"🔒 (Secure Chat)\nAapne kaha: {user_text}\n\nYeh baat bilkul secure hai.")

def main():
    # Flask ko background thread mein chalu karte hain
    t = Thread(target=run_flask)
    t.start()

    # Telegram bot polling start karte hain
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot polling & Web Server started successfully...")
    application.run_polling()

if __name__ == '__main__':
    main()
