import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8579048820:AAEFOX2J_2Xcdb3-ioZaKAIgsjPiMLljrH8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalam-o-Alaikum! Main Muhammad Parwez ka personal secure bot hoon. Boliye, main aapki kya madad kar sakta hoon?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response_message = f"🔒 (Secure Chat)\nAapne kaha: {user_text}\n\nYeh baat bilkul secure hai."
    await update.message.reply_text(response_message)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Muhammad Parwez Bot started...")
    application.run_polling()
