# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup
from main import lang

def items_default(user_id):
    if lang(user_id)=='Eng':
        items_default = ReplyKeyboardMarkup(resize_keyboard=True)
        items_default.row("📁 Add positions", "📁 Change positions", "📁 Delete positions")
        items_default.row("📜 Add subcategory", "📜 Change subcategory", "📜 Delete subcategory")
        items_default.row("📜 Add category", "📜 Delete category")
        items_default.row("⬅ To the main page")
    else:
        items_default = ReplyKeyboardMarkup(resize_keyboard=True)
        items_default.row("📁 Создать позицию", "📁 Изменить позицию", "📁 Удалить позиции")
        items_default.row("📜 Создать подкатегорию", "📜 Изменить подкатегорию", "📜 Удалить подкатегории")
        items_default.row("📜 Создать категорию", "📜 Удалить категории")
        items_default.row("⬅ На главную")
    return items_default
def skip_send_image_default(user_id):
    if lang(user_id)=='Eng':
        skip_send_image_default = ReplyKeyboardMarkup(resize_keyboard=True)
        skip_send_image_default.row("📸 Skip")
    else:
        skip_send_image_default = ReplyKeyboardMarkup(resize_keyboard=True)
        skip_send_image_default.row("📸 Пропустить")
    return skip_send_image_default
def cancel_send_image_default(user_id):
    if lang(user_id)=='Eng':
        cancel_send_image_default = ReplyKeyboardMarkup(resize_keyboard=True)
        cancel_send_image_default.row("📸 Cancel")
    else:
        cancel_send_image_default = ReplyKeyboardMarkup(resize_keyboard=True)
        cancel_send_image_default.row("📸 Отменить")
    return cancel_send_image_default
def finish_load_items_default(user_id):
    if lang(user_id)=='Eng':
        finish_load_items_default = ReplyKeyboardMarkup(resize_keyboard=True)
        finish_load_items_default.row("📥 Finish loading the items")
    else:
        finish_load_items_default = ReplyKeyboardMarkup(resize_keyboard=True)
        finish_load_items_default.row("📥 Закончить загрузку товаров")
    return finish_load_items_default