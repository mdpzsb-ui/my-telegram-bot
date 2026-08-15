import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8763508564:AAHJmqio1tBvksc-Qhc9x1dZVFA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalam-o-Alaikum! Main All Video Downloader bot hoon. Mujhe kisi bhi video ka link bhejein, main download karke bhej dunga.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        await update.message.reply_text("Bhai, kripya koi valid video link bhejein.")
        return

    await update.message.reply_text("⏳ Video download ho raha hai, thoda intezaar karein...")

    output_file = "video.mp4"
    
    if os.path.exists(output_file):
        os.remove(output_file)

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_file,
        'max_filesize': 50 * 1024 * 1024,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(output_file):
            with open(output_file, 'rb') as video:
                await update.message.reply_video(video)
            os.remove(output_file)
        else:
            await update.message.reply_text("Maafi chahta hoon, video download nahi ho saka.")
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text(f"Error aa gaya hai: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot started and polling...")
    application.run_polling()
