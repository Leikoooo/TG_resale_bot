# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main import lang
# Рассылка
def sure_send_ad_inl(user_id):
    if lang(user_id)=='Eng':
        sure_send_ad_inl = InlineKeyboardMarkup()
        yes_send_kb = InlineKeyboardButton(text="✅ Send", callback_data="yes_send_ad")
        button = InlineKeyboardButton(text="⭕ Add Buttons", callback_data="button_send_ad")
        not_send_kb = InlineKeyboardButton(text="❌ Back", callback_data="not_send_kb")
        sure_send_ad_inl.add(yes_send_kb, not_send_kb)
        sure_send_ad_inl.add(button)
    else:
        sure_send_ad_inl = InlineKeyboardMarkup()
        yes_send_kb = InlineKeyboardButton(text="✅ Отправить", callback_data="yes_send_ad")
        button = InlineKeyboardButton(text="⭕ Добавить кнопки", callback_data="button_send_ad")
        not_send_kb = InlineKeyboardButton(text="❌ Отменить", callback_data="not_send_kb")
        sure_send_ad_inl.add(yes_send_kb, not_send_kb)
        sure_send_ad_inl.add(button)
    return sure_send_ad_inl

# Удаление подкатегорий
def confirm_clear_podcategory_inl(user_id):
    if lang(user_id)=='Eng':
        confirm_clear_podcategory_inl = InlineKeyboardMarkup()
        yes_clear_cat_kb = InlineKeyboardButton(text="❌ Yes, delete all", callback_data="confirm_clear_podcategory")
        not_clear_cat_kb = InlineKeyboardButton(text="✅ No, back", callback_data="cancel_clear_podcategory")
        confirm_clear_podcategory_inl.add(yes_clear_cat_kb, not_clear_cat_kb)
    else:
        confirm_clear_podcategory_inl = InlineKeyboardMarkup()
        yes_clear_cat_kb = InlineKeyboardButton(text="❌ Да, удалить все", callback_data="confirm_clear_podcategory")
        not_clear_cat_kb = InlineKeyboardButton(text="✅ Нет, отменить", callback_data="cancel_clear_podcategory")
        confirm_clear_podcategory_inl.add(yes_clear_cat_kb, not_clear_cat_kb)
    return confirm_clear_podcategory_inl

def confirm_clear_category_inl(user_id):
    if lang(user_id)=='Eng':
        confirm_clear_category_inl = InlineKeyboardMarkup()
        yes_clear_cat_kb = InlineKeyboardButton(text="❌ Yes, delete all", callback_data="confirm_clear_category")
        not_clear_cat_kb = InlineKeyboardButton(text="✅ No, back", callback_data="cancel_clear_category")
        confirm_clear_category_inl.add(yes_clear_cat_kb, not_clear_cat_kb)
    else:
        confirm_clear_category_inl = InlineKeyboardMarkup()
        yes_clear_cat_kb = InlineKeyboardButton(text="❌ Да, удалить все", callback_data="confirm_clear_category")
        not_clear_cat_kb = InlineKeyboardButton(text="✅ Нет, отменить", callback_data="cancel_clear_category")
        confirm_clear_category_inl.add(yes_clear_cat_kb, not_clear_cat_kb)
    return confirm_clear_category_inl
def confirm_clear_position_inl(user_id):
    if lang(user_id)=='Eng':
        confirm_clear_position_inl = InlineKeyboardMarkup()
        yes_clear_cat_kb = InlineKeyboardButton(text="❌ Yes, delete all", callback_data="confirm_clear_position")
        not_clear_cat_kb = InlineKeyboardButton(text="✅ No, back", callback_data="cancel_clear_position")
        confirm_clear_position_inl.add(yes_clear_cat_kb, not_clear_cat_kb)
    else:
        confirm_clear_position_inl = InlineKeyboardMarkup()
        yes_clear_cat_kb = InlineKeyboardButton(text="❌ Да, удалить все", callback_data="confirm_clear_position")
        not_clear_cat_kb = InlineKeyboardButton(text="✅ Нет, отменить", callback_data="cancel_clear_position")
        confirm_clear_position_inl.add(yes_clear_cat_kb, not_clear_cat_kb)
    return confirm_clear_position_inl

def confirm_clear_item_inl(user_id):
    if lang(user_id)=='Eng':
        confirm_clear_item_inl = InlineKeyboardMarkup()
        yes_clear_item_kb = InlineKeyboardButton(text="❌ Yes, delete all", callback_data="confirm_clear_item")
        not_clear_item_kb = InlineKeyboardButton(text="✅ No, back", callback_data="cancel_clear_item")
        confirm_clear_item_inl.add(yes_clear_item_kb, not_clear_item_kb)
    else:
        confirm_clear_item_inl = InlineKeyboardMarkup()
        yes_clear_item_kb = InlineKeyboardButton(text="❌ Да, удалить все", callback_data="confirm_clear_item")
        not_clear_item_kb = InlineKeyboardButton(text="✅ Нет, отменить", callback_data="cancel_clear_item")
        confirm_clear_item_inl.add(yes_clear_item_kb, not_clear_item_kb)
    return confirm_clear_item_inl
def delete_item_inl(user_id):
    if lang(user_id)=='Eng':
        confirm_clear_item_inl = InlineKeyboardMarkup()
        delete_item_inl.add(InlineKeyboardButton(text="💰 Delete an item", callback_data="delete_this_item"))
    else:
        delete_item_inl = InlineKeyboardMarkup()
        delete_item_inl.add(InlineKeyboardButton(text="💰 Удалить товар", callback_data="delete_this_item"))
    return delete_item_inl
