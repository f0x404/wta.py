import logging
import random
import time

from telegram import Bot
from telegram.ext import Application, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

# زانیاری بۆ بۆت و چەنال
BOT_TOKEN = "7910838916:AAFhyO_8E6uNxqrmtUvSeWxRRjZ3buLE7ps"
CHANNEL_USERNAME = "@FFF000XXX"  # ناوی جەنالەکەت لەگەڵ @

# دامەزراندنی بۆتەکە بە شێوەی async
async def main():
    bot = Bot(token=BOT_TOKEN)

    # دابینکردنی وتەکان
    def load_quotes():
        with open("quotes.txt", "r", encoding="utf-8") as file:
            quotes = file.read().splitlines()
            random.shuffle(quotes)
            return quotes

    # دەرکردنی وتەی داهاتوو
    quotes = load_quotes()
    sent_quotes = set()

    # فەرمودنەکەی ناردن
    async def send_quote():
        nonlocal quotes, sent_quotes

        for quote in quotes:
            if quote not in sent_quotes:
                try:
                    await bot.send_message(chat_id=CHANNEL_USERNAME, text=quote)
                    logging.info(f"Quote sent: {quote}")
                    sent_quotes.add(quote)
                    return
                except Exception as e:
                    logging.error(f"Failed to send quote: {e}")
                    return

        logging.warning("No more quotes to send!")

    # دامەزراندنی ڕاژەکە
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_quote, "interval", minutes=1)
    scheduler.start()

    # دەستپێکردنی بۆت
    logging.basicConfig(level=logging.INFO)
    logging.info("Bot started successfully...")

    # بۆت بژێنە تا داخراوە
    while True:
        await asyncio.sleep(10)

# ئەم شێوەیە ڕووکاری ڕاستە و بەشێوەی async بەرەوپێش
if __name__ == '__main__':
    asyncio.run(main())