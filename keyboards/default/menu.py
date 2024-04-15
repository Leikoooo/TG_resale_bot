# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup
from main import lang
from data.config import admins
from utils.db_api.sqlite import get_userx


def check_user_out_func(user_id):
    user_info=get_userx(user_id=user_id)
    if str(user_info[1]) not in admins:
        menu_default = ReplyKeyboardMarkup(resize_keyboard=True)
        menu_default.row("🔉 Social media", "⚔️ Games")
        menu_default.row("Profile", "💵 Deposit", "FAQ")
    else:
        menu_default = ReplyKeyboardMarkup(resize_keyboard=True)
        menu_default.row("🔉 Social media", "⚔️ Games","💵 Deposit")
        menu_default.row("Profile","FAQ")
        menu_default.row("Info", "Settings")
        menu_default.row("Functions", "Product Management")
    return menu_default

def all_back_to_main_default(user_id):
    all_back_to_main_default = ReplyKeyboardMarkup(resize_keyboard=True)
    all_back_to_main_default.row("⬅ To the main page")

    return all_back_to_main_default