from telegram import Update, User, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from models import user_manager
CREATE_DEBT_BUTTON = "Создать запрос"
CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

async def start(update: Update, context: CONTEXT_DEFAULT_TYPE):
    user: User = update.effective_user
    app_user = user_manager.auth_user(user)
    markup = ReplyKeyboardMarkup(
        [[KeyboardButton(text=CREATE_DEBT_BUTTON), KeyboardButton(text="Мои долги")]], resize_keyboard=True, one_time_keyboard=True
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, выбери действие", reply_markup=markup)
