from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler, CallbackQueryHandler
from models import user_manager
from handlers import CREATE_DEBT_BUTTON, start
from datetime import date
from database import conn

CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE
month_names = ("Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октрябрь", "Ноябрь", "Декабрь")
months = {idx+1:month for idx, month in enumerate(month_names)}
days_quantity = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8:31, 9: 30, 10: 31, 11: 30, 12: 31}

async def get_borrower(update: Update, context: CONTEXT_DEFAULT_TYPE):
    user = update.message.from_user
    buttons = [[InlineKeyboardButton(text=f"{u.first_name} {u.last_name}", callback_data=f"{u.telegram_id}")] for u in user_manager.users if u.telegram_id != user.id]
    markup = InlineKeyboardMarkup(buttons)

    await context.bot.send_message(update.effective_chat.id, text="Укажите заёмщика", reply_markup=markup)
    return 0

async def get_ammount(update: Update, context: CONTEXT_DEFAULT_TYPE):
    print(f"borrower_id = {update.callback_query.data}")
    context.user_data["borrower_id"] = update.callback_query.data
    
    await context.bot.send_message(update.effective_chat.id, text="Введите сумму")
    return 1

async def get_month(update: Update, context: CONTEXT_DEFAULT_TYPE):
    context.user_data["amount"] = update.effective_message.text
    buttons = [[InlineKeyboardButton(text=month, callback_data=f"{idx}")] for idx, month in months.items()]
    markup = InlineKeyboardMarkup(buttons)

    await context.bot.send_message(update.effective_chat.id, text="Укажите срок. Выберите месяц", reply_markup=markup)
    return 2

async def get_day(update: Update, context: CONTEXT_DEFAULT_TYPE):
    month = update.callback_query.data
    context.user_data["month"] = month
    quantity = days_quantity[int(month)] + 1
    buttons = [[InlineKeyboardButton(text=f"{day}", callback_data=f"{day}")] for day in range(1, quantity)]
    markup = InlineKeyboardMarkup(buttons)

    await context.bot.send_message(update.effective_chat.id, text="Выберите день", reply_markup=markup)
    return 3

async def send_debt_request(update: Update, context: CONTEXT_DEFAULT_TYPE):
    user = user_manager.auth_user(update.effective_user)
    context.user_data["debtor_id"] = user.telegram_id
    context.user_data["day"] = update.callback_query.data
    borrower_id = int(context.user_data["borrower_id"])
    amount = context.user_data["amount"]
    month = context.user_data["month"]
    day = update.callback_query.data
    deadline = date(2024, int(month), int(day))
    text = f"Запрос на долг\nОт: {user.username}\nСумма: {amount}\nСрок: {deadline.isoformat()}"
    buttons = [[KeyboardButton(text="Принять ✅"), KeyboardButton(text="Отклонить ❌")]]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

    await context.bot.send_message(borrower_id, text, reply_markup=markup)
    return 4

async def process_response(update: Update, context: CONTEXT_DEFAULT_TYPE):
    response = update.effective_message.text
    borrower = user_manager.get_user_by_id(int(context.user_data["borrower_id"]))
    debtor = user_manager.get_user_by_id(context.user_data["debtor_id"])
    if response == "Принять ✅":
        amount = context.user_data["amount"]
        month = context.user_data["month"]
        day = context.user_data["day"]
        deadline = date(2024, int(month), int(day))
        with conn.cursor() as cur:
            query = "INSERT INTO debts (borrower_id, debtor_id, amount, deadline) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (borrower.telegram_id, debtor.telegram_id, amount, deadline))
            conn.commit()
        await context.bot.send_message(debtor.telegram_id, text="Пользователь одобрил запрос")
    if response == "Отклонить ❌":
        await context.bot.send_message(debtor.telegram_id, text="Пользователь отклонил запрос")
    await start(update, context)
    return -1

debt_create_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(f"^{CREATE_DEBT_BUTTON}$"), get_borrower)],
    states={
        0: [CallbackQueryHandler(get_ammount)],
        1: [MessageHandler(filters.TEXT, get_month)],
        2: [CallbackQueryHandler(get_day)],
        3: [CallbackQueryHandler(send_debt_request)],
        4: [MessageHandler(filters.TEXT, process_response)]
    },
    fallbacks=[CommandHandler("start", start)]
)