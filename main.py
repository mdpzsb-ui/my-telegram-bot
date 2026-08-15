import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8579048820:AAEdZzcN_5C2mYpZjsiBJHJyI0MQnvtxdBc"
PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

# Global application variable
application = None

async def setup_application():
    app_builder = Application.builder().token(TOKEN).build()
    
    async def start(update: Update, context):
        await update.message.reply_text("Assalam-o-Alaikum! Main Muhammad Parwez ka personal secure bot hoon.")

    async def handle_message(update: Update, context):
        user_text = update.message.text
        await update.message.reply_text(f"🔒 (Secure Chat)\nAapne kaha: {user_text}\n\nYeh baat bilkul secure hai.")

    app_builder.add_handler(CommandHandler('start', start))
    app_builder.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    await app_builder.initialize()
    return app_builder

@app.route('/')
def home():
    return "Webhook Bot is active!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    import asyncio
    try:
        json_data = request.get_json(force=True)
        update = Update.de_json(json_data, application.bot)
        
        async def process():
            await application.process_update(update)
            
        asyncio.run(process())
    except Exception as e:
        logger.error(f"Error processing update: {e}")
    return 'OK', 200

if __name__ == '__main__':
    import asyncio
    # Initialize application and set webhook automatically using Render/Railway URL if available
    loop = asyncio.get_event_loop()
    application = loop.run_until_complete(setup_application())
    
    # Get public URL automatically
    external_url = os.environ.get("RENDER_EXTERNAL_URL") or os.environ.get("RAILWAY_STATIC_URL")
    if external_url:
        webhook_url = f"https://{external_url.replace('https://', '')}/{TOKEN}"
        loop.run_until_complete(application.bot.set_webhook(webhook_url))
        logger.info(f"Webhook automatically set to: {webhook_url}")

    app.run(host='0.0.0.0', port=PORT)
