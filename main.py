import logging
import json
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, StringRegexHandler, ConversationHandler
from handlers import start, debt_create_conv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

with open("config.json") as cfg:
    config = json.load(cfg)
TOKEN = config["token"]


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)

    application.add_handler(start_handler)
    application.add_handler(debt_create_conv)
    
    application.run_polling()