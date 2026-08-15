import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8763508564:AAHJmqio1tBvksc-Qhc9x1dZVFA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalam-o-Alaikum! Mujhe video ka link bhejein.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url or "http" not in url:
        return

    await update.message.reply_text("⏳ Downloading...")

    ydl_opts = {
        'format': 'best/bestvideo+bestaudio',
        'outtmpl': 'video.mp4',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists('video.mp4'):
            with open('video.mp4', 'rb') as f:
                await update.message.reply_video(f)
            os.remove('video.mp4')
        else:
            await update.message.reply_text("Download nahi ho saka.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()
