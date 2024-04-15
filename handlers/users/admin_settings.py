# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import CantParseEntities

from filters import IsAdmin
from keyboards.default import get_settings_func
from loader import dp
from states import StorageSettings
from utils.db_api.sqlite import *
from utils.other_func import send_all_admin, clear_firstname
from main import lang

# Обработка кнопки "Изменить Faq"
@dp.message_handler(IsAdmin(), text=["ℹ Edit the FAQ 🖍","ℹ Изменить FAQ 🖍"], state="*")
async def change_faq(message: types.Message, state: FSMContext):
    await state.finish()
    get_faq = get_settingsx()
    await message.answer(f"<b>ℹ Current FAQ:</b>\n{get_faq[1]}")
    await message.answer("<b>🖍 Enter a new text for the FAQ</b>\n"
                         "❕ You can use prepared syntax and HTML markup:\n"
                         "▶ <code>{username}</code>  - user login\n"
                         "▶ <code>{user_id}</code>   - user id\n"
                         "▶ <code>{firstname}</code> - user name")
    await StorageSettings.here_faq.set()


# Обработка кнопки "Изменить контакты"
@dp.message_handler(IsAdmin(), text=["📕 Изменить контакты 🖍","📕 Change contacts 🖍"], state="*")
async def change_contact(message: types.Message, state: FSMContext):
    await state.finish()
    get_contact = get_settingsx()
    await message.answer(f"<b>📕 Current contacts:</b>\n{get_contact[0]}")
    await message.answer("🖍 Send the user login.\n")
    await StorageSettings.here_contact.set()


# Выключение покупок
@dp.message_handler(IsAdmin(), text=["🔴 Disable purchases","🔴 Выключить покупки"], state="*")
async def turn_off_buy(message: types.Message, state: FSMContext):
    await state.finish()
    update_settingsx(status_buy="False")
    await message.answer("<b>🔴 Purchases in the bot were turned off.</b>",
                         reply_markup=get_settings_func(message.from_user.id))
    await send_all_admin(
        f"👤 Administrator <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a>\n"
        "🔴 Turned off purchases in the bot.", not_me=message.from_user.id)


# Включение покупок
@dp.message_handler(IsAdmin(), text=["🟢 Enable purchases","🟢 Включить покупки"], state="*")
async def turn_on_buy(message: types.Message, state: FSMContext):
    await state.finish()
    update_settingsx(status_buy="True")
    await message.answer("<b>🟢 Purchases in the bot were included.</b>",
                         reply_markup=get_settings_func(message.from_user.id))
    await send_all_admin(
        f"👤 Administrator <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a>\n"
        "🟢 Enabled purchases in the bot.", not_me=message.from_user.id)


# Обработка кнопки "Отправить бота на тех. работы"
@dp.message_handler(IsAdmin(), text=["🔴 Send to tech. works","🔴 Отправить на тех. работы"], state="*")
async def send_bot_to_work(message: types.Message, state: FSMContext):
    await state.finish()
    update_settingsx(status="False")
    await message.answer("<b>🔴 The bot was sent for technical work.</b>",
                         reply_markup=get_settings_func(message.from_user.id))
    await send_all_admin(
        f"👤 Administrator <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a>\n"
        "🔴 Sent the bot for technical work.", not_me=message.from_user.id)


# Обработка кнопки "Вывести бота из тех. работ"
@dp.message_handler(IsAdmin(), text=["🟢 Withdraw from tech. works","🟢 Вывести из тех. работ"], state="*")
async def return_bot_from_work(message: types.Message, state: FSMContext):
    await state.finish()
    update_settingsx(status="True")
    await message.answer("<b>🟢 The bot was taken out of technical work.</b>",
                         reply_markup=get_settings_func(message.from_user.id))
    await send_all_admin(
        f"👤 Administrator <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a>\n"
        "🟢 Took the bot out of technical work.", not_me=message.from_user.id)


# Принятие нового текста для faq
@dp.message_handler(IsAdmin(), state=StorageSettings.here_faq)
async def get_text_for_change_faq(message: types.Message, state: FSMContext):
    send_msg = message.text
    msg = message.text
    if "{username}" in msg:
        msg = msg.replace("{username}", f"<b>{message.from_user.username}</b>")
    if "{user_id}" in msg:
        msg = msg.replace("{user_id}", f"<b>{message.from_user.id}</b>")
    if "{firstname}" in msg:
        msg = msg.replace("{firstname}", f"<b>{clear_firstname(message.from_user.first_name)}</b>")
    try:
        await state.finish()
        await message.answer(f"ℹ The FAQ has been updated ✅ Example:\n{msg}",
                             reply_markup=get_settings_func(message.from_user.id))
        update_settingsx(faq=send_msg)
    except CantParseEntities:
        await StorageSettings.here_faq.set()
        await message.answer("<b>❌ HTML syntax error.</b>\n"
                             "🖍 Enter a new text for the FAQ")


# Принятие нового айди для контактов
@dp.message_handler(IsAdmin(), state=StorageSettings.here_contact)
async def get_id_for_change_contact(message: types.Message, state: FSMContext):
    msg = message.text
    await state.finish()
    msg = f"📕 <b>Write here ➡ <a href='https://t.me/{msg}'>Administrator</a></b>"
    update_settingsx(contact=msg)
    await message.answer(f"📕 Contacts have been successfully updated ✅",
                            reply_markup=get_settings_func(message.from_user.id))

