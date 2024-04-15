# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main import lang

# Проверка оплаты 
def open_item_func(position_id, remover, category_id, user_id):
    open_item = InlineKeyboardMarkup()
    open_item.add(InlineKeyboardButton(text="💵 Buy",
                                        callback_data=f"buy_this_item:{position_id}"))
    open_item.add(InlineKeyboardButton("🔘 Back",
                                        callback_data=f"back_buy_item_position:{remover}:{category_id}"))
    return open_item

def check_payment_crystal(user_id):
    check_payment_crystal_button1 = InlineKeyboardButton('Paid', callback_data=f"paid:{user_id}")
    check_payment_crystal_button2 = InlineKeyboardButton('Cancel payment', callback_data=f"otmena:{user_id}")
    return InlineKeyboardMarkup().add(check_payment_crystal_button1).add(check_payment_crystal_button2)

# Подтверждение покупки товара
def confirm_buy_items(amount_pay, user_id):
    confirm_buy_item_keyboard = InlineKeyboardMarkup()
    yes_buy_kb = InlineKeyboardButton(text="✅ Confirm",
                                    callback_data=f"xbuy_item:{amount_pay}")
    not_buy_kb = InlineKeyboardButton("❌ Cancel",
                                    callback_data=f"not_buy_items")
    confirm_buy_item_keyboard.add(yes_buy_kb, not_buy_kb)
    return confirm_buy_item_keyboard
