# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup
from main import lang
from utils.db_api.sqlite import get_paymentx


def payment_default(user_id):
    if lang(user_id)=='Eng':
        payment = get_paymentx()
        payment_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        payment_kb.row("🥝 Change QIWI 🖍", "🥝 Check QIWI ♻", "🥝 Balance QIWI 👁")
        if payment!= None and payment[5] == "True":
            payment_kb.row("🔴 Disable deposits")
        else:
            payment_kb.row("🟢 Enable deposits")
        payment_kb.row("⬅ To the main page")
    else:
        payment = get_paymentx()
        payment_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        payment_kb.row("🥝 Изменить QIWI 🖍", "🥝 Проверить QIWI ♻", "🥝 Баланс QIWI 👁")
        if payment!= None and payment[5] == "True":
            payment_kb.row("🔴 Выключить пополнения")
        else:
            payment_kb.row("🟢 Включить пополнения")
        payment_kb.row("⬅ На главную")
    return payment_kb
