from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Reminder storage
reminders = {}

# Function to send reminder
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(chat_id=job.chat_id, text=f"⏰ Reminder: {job.data}")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Use /remind <minutes> <message> to set a reminder.")

# /remind command
async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        minutes = int(context.args[0])
        reminder_msg = ' '.join(context.args[1:])
        chat_id = update.effective_chat.id
        reminder_time = datetime.now() + timedelta(minutes=minutes)

        context.job_queue.run_once(send_reminder, when=minutes * 60, chat_id=chat_id, data=reminder_msg)

        await update.message.reply_text(f"Reminder set for {minutes} minute(s) from now.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /remind <minutes> <message>")

# Run bot
if __name__ == '__main__':
    TOKEN = "YOUR_BOT_TOKEN_HERE"

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("remind", remind))

    app.run_polling()
