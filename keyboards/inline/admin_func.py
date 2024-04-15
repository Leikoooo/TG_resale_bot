# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.sqlite import get_paymentx, get_positionx, get_itemsx, get_positionsx, get_categoryx
from main import lang

# Поиск профиля
def search_profile_func(user_id):
    search_profile = InlineKeyboardMarkup()
    if lang(user_id)=='Eng':
        user_purchases_kb = InlineKeyboardButton(text="🛒 Purchases", callback_data=f"show_purchases:{user_id}")
        add_balance_kb = InlineKeyboardButton(text="💴 Give a balance", callback_data=f"add_balance:{user_id}")
        set_balance_kb = InlineKeyboardButton(text="💸 Change balance", callback_data=f"set_balance:{user_id}")
        send_msg_kb = InlineKeyboardButton(text="💌 Send SMS", callback_data=f"send_message:{user_id}")
    else:
        user_purchases_kb = InlineKeyboardButton(text="🛒 Покупки", callback_data=f"show_purchases:{user_id}")
        add_balance_kb = InlineKeyboardButton(text="💴 Выдать баланс", callback_data=f"add_balance:{user_id}")
        set_balance_kb = InlineKeyboardButton(text="💸 Изменить баланс", callback_data=f"set_balance:{user_id}")
        send_msg_kb = InlineKeyboardButton(text="💌 Отправить СМС", callback_data=f"send_message:{user_id}")
    search_profile.add(add_balance_kb,set_balance_kb,send_msg_kb)
    return search_profile

def channel_confirm(user_id, link):
    conf = InlineKeyboardMarkup()
    user_purchases_kb = InlineKeyboardButton(text="Проверить подписку", callback_data=f"channel:{user_id}")
    user_purchases_kb2 = InlineKeyboardButton(text="Подписаться", url=f"{link}")
    conf.add(user_purchases_kb2)
    conf.add(user_purchases_kb)
    return conf

# Способы пополнения
def choice_way_input_payment_func():
    get_payments = get_paymentx()
    payment_method = InlineKeyboardMarkup()

    if get_payments[4] == "form":
        change_qiwi_form = InlineKeyboardButton(text="✅ Form", callback_data="...")
    else:
        change_qiwi_form = InlineKeyboardButton(text="❌ Form", callback_data="change_payment:form")

    if get_payments[4] == "number":
        change_qiwi_number = InlineKeyboardButton(text="✅ Number", callback_data="...")
    else:
        change_qiwi_number = InlineKeyboardButton(text="❌ Number", callback_data="change_payment:number")

    if get_payments[4] == "nickname":
        change_qiwi_nickname = InlineKeyboardButton(text="✅ Nickname", callback_data="...")
    else:
        change_qiwi_nickname = InlineKeyboardButton(text="❌ Nickname", callback_data="change_payment:nickname")
    payment_method.add(change_qiwi_form, change_qiwi_number)
    payment_method.add(change_qiwi_nickname)
    return payment_method


# Изменение категории
def edit_category_func(category_id, remover):
    category_keyboard = InlineKeyboardMarkup()
    get_fat_count = len(get_positionsx("*", category_id=category_id))
    get_category = get_categoryx("*", category_id=category_id)

    messages = "<b>📜 Select an action with a category 🖍</b>\n" \
               "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"🏷 Title: <code>{get_category[0][2]}</code>\n" \
               f"📁 Number of positions: <code>{get_fat_count}</code>"

    change_name_kb = InlineKeyboardButton(text="🏷 Change the title",
                                          callback_data=f"category_edit_name:{category_id}:{remover}")
    remove_kb = InlineKeyboardButton(text="❌ Remove",
                                     callback_data=f"category_remove:{category_id}:{remover}")
    back_category_kb = InlineKeyboardButton("⬅ Back ↩",
                                            callback_data=f"back_category_edit:{remover}")
    category_keyboard.add(change_name_kb, remove_kb)
    category_keyboard.add(back_category_kb)
    return messages, category_keyboard


# Кнопки с удалением категории
def confirm_remove_func(category_id, remover):
    confirm_remove_keyboard = InlineKeyboardMarkup()
    change_name_kb = InlineKeyboardButton(text="❌ Yes, remove",
                                          callback_data=f"yes_remove_category:{category_id}:{remover}")
    move_kb = InlineKeyboardButton(text="✅ No, back",
                                   callback_data=f"not_remove_category:{category_id}:{remover}")
    confirm_remove_keyboard.add(change_name_kb, move_kb)
    return confirm_remove_keyboard


# Кнопки при открытии позиции для изменения
def open_edit_position_func(position_id, category_id, remover):
    open_item_keyboard = InlineKeyboardMarkup()
    get_position = get_positionx("*", position_id=position_id)
    get_items = get_itemsx("*", position_id=position_id)
    have_photo = False
    photo_text = "Absent ❌"
    if len(get_position[5]) >= 5:
        have_photo = True
        photo_text = "Have ✅"
    messages = "<b>📁 Editing a position:</b>\n" \
               "➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"<b>🏷 Title:</b> <code>{get_position[2]}</code>\n" \
               f"<b>💵 Amount:</b> <code>{get_position[3]}$</code>\n" \
               f"<b>📦 Count:</b> <code>{len(get_items)}</code>\n" \
               f"<b>📸 Image:</b> <code>{photo_text}</code>\n" \
               f"<b>📜 Description:</b> \n" \
               f"{get_position[4]}\n"
    edit_name_kb = InlineKeyboardButton(text="🏷 Change title",
                                        callback_data=f"position_change_name:{position_id}:{category_id}:{remover}")
    edit_price_kb = InlineKeyboardButton(text="💵 Change amount",
                                         callback_data=f"position_change_price:{position_id}:{category_id}:{remover}")
    edit_discr_kb = InlineKeyboardButton(text="📜 Change description",
                                         callback_data=f"position_change_discription:{position_id}:{category_id}:{remover}")
    edit_photo_kb = InlineKeyboardButton(text="📸 Change Photo",
                                         callback_data=f"position_change_photo:{position_id}:{category_id}:{remover}")
    remove_kb = InlineKeyboardButton(text="🗑 Remove",
                                     callback_data=f"position_remove_this:{position_id}:{category_id}:{remover}")
    clear_kb = InlineKeyboardButton(text="❌ Clear",
                                    callback_data=f"position_clear_this:{position_id}:{category_id}:{remover}")
    back_positions_kb = InlineKeyboardButton("⬅ Back ↩",
                                             callback_data=f"back_position_edit:{category_id}:{remover}")
    open_item_keyboard.add(edit_name_kb, edit_price_kb)
    open_item_keyboard.add(edit_discr_kb, edit_photo_kb)
    open_item_keyboard.add(remove_kb, clear_kb)
    open_item_keyboard.add(back_positions_kb)
    return messages, open_item_keyboard, have_photo


# Подтверждение удаления позиции
def confirm_remove_position_func(position_id, category_id, remover):
    confirm_remove_position_keyboard = InlineKeyboardMarkup()
    change_name_kb = InlineKeyboardButton(text="❌ Yes, remove",
                                          callback_data=f"yes_remove_position:{position_id}:{category_id}:{remover}")
    move_kb = InlineKeyboardButton(text="✅ No, back",
                                   callback_data=f"not_remove_position:{position_id}:{category_id}:{remover}")
    confirm_remove_position_keyboard.add(change_name_kb, move_kb)
    return confirm_remove_position_keyboard


# Подтверждение очистики позиции
def confirm_clear_position_func(position_id, category_id, remover):
    confirm_clear_position_keyboard = InlineKeyboardMarkup()
    change_name_kb = InlineKeyboardButton(text="❌ Yes, remove",
                                          callback_data=f"yes_clear_position:{position_id}:{category_id}:{remover}")
    move_kb = InlineKeyboardButton(text="✅ No, back",
                                   callback_data=f"not_clear_position:{position_id}:{category_id}:{remover}")
    confirm_clear_position_keyboard.add(change_name_kb, move_kb)
    return confirm_clear_position_keyboard
