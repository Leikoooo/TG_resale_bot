# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup
from main import lang

def get_functions_func(user_id):
    functions_default = ReplyKeyboardMarkup(resize_keyboard=True)
    functions_default.row("📱 Profile Search 🔍", "📢 Mailing")
    functions_default.row("⬅ To the main page")
    return functions_default
