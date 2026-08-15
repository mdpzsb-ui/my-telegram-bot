import os
import logging
from flask import Flask, request
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8579048820:AAEdZzcN_5C2mYpZjsiBJHJyI0MQnvtxdBc"
PORT = int(os.environ.get("PORT", 8080))

app = Flask(__name__)
bot = telegram.Bot(TOKEN)
application = None

async def setup_bot():
    global application
    application = Application.builder().token(TOKEN).build()
    
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Assalam-o-Alaikum! Main Muhammad Parwez ka personal secure bot hoon.")

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text
        await update.message.reply_text(f"🔒 (Secure Chat)\nAapne kaha: {user_text}\n\nYeh baat bilkul secure hai.")

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    await application.initialize()

@app.route('/')
def home():
    return "Webhook Bot is running smoothly!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    import asyncio
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, bot)
    
    async def process():
        await application.process_update(update)
    
    asyncio.run(process())
    return 'OK'

if __name__ == '__main__':
    import asyncio
    asyncio.run(setup_bot())
    app.run(host='0.0.0.0', port=PORT)
