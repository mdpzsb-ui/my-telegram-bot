import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8579048820:AAEdZzcN_5C2mYpZjsiBJHJyI0MQnvtxdBc"

# Flask server taaki Railway ka port requirement poora rahe
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running securely!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Telegram Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalam-o-Alaikum! Main Muhammad Parwez ka personal secure bot hoon. Boliye, main aapki kya madad kar sakta hoon?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response_message = f"🔒 (Secure Chat)\nAapne kaha: {user_text}\n\nYeh baat bilkul secure hai."
    await update.message.reply_text(response_message)

def main():
    # Flask ko alag thread mein chalate hain
    t = Thread(target=run_flask)
    t.start()

    # Telegram bot start karte hain
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Telegram Bot & Web Server started...")
    application.run_polling()

if __name__ == '__main__':
    main()
