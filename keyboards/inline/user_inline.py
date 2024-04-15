# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main import lang
# Кнопки при поиске профиля через админ-меню
def open_profile_inl(user_id):
    if lang(user_id)=='Eng':
        open_profile_inl = InlineKeyboardMarkup()
        # input_kb = InlineKeyboardButton(text="💵 Пополнить", callback_data="user_input")
        input_kb = InlineKeyboardButton(text="💵 Deposit", callback_data="choice_lz")
        # mybuy_kb = InlineKeyboardButton(text="Apply promocode", callback_data="my_buy")
        open_profile_inl.add(input_kb)
    else:
        open_profile_inl = InlineKeyboardMarkup()
        # input_kb = InlineKeyboardButton(text="💵 Пополнить", callback_data="user_input")
        input_kb = InlineKeyboardButton(text="💵 Пополнить", callback_data="choice_lz")
        # mybuy_kb = InlineKeyboardButton(text="Применить промокод", callback_data="my_buy")
        open_profile_inl.add(input_kb)
    return open_profile_inl
# Кнопка с возвратом к профилю\

def answer_body(user_id):
    answer_body = InlineKeyboardMarkup()
    answer_body.add(InlineKeyboardButton(text="Выдать товар", callback_data=f"get_item:{user_id}"))
    return answer_body

def to_profile_inl(user_id):
    if lang(user_id)=='Eng':
        to_profile_inl = InlineKeyboardMarkup()
        to_profile_inl.add(InlineKeyboardButton(text="Profile", callback_data="user_profile"))
    else:
        to_profile_inl = InlineKeyboardMarkup()
        to_profile_inl.add(InlineKeyboardButton(text="Профиль", callback_data="user_profile"))
    return to_profile_inl

lang_inl = InlineKeyboardMarkup()
input_kb = InlineKeyboardButton(text="Russian", callback_data="Rus")
mybuy_kb = InlineKeyboardButton(text="English", callback_data="Eng")
lang_inl.add(input_kb, mybuy_kb)
