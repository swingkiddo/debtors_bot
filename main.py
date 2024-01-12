import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, StringRegexHandler, ConversationHandler


from handlers import start, debt_create_conv
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "6877971933:AAFsZ6PGioV90UDojsgQaUCWLnsT4w9hlqA"


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)

    application.add_handler(start_handler)
    application.add_handler(debt_create_conv)
    
    application.run_polling()