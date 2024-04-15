# - *- coding: utf- 8 - *-
import asyncio
import json

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from main import lang
from filters import IsAdmin
from keyboards.default import payment_default
from keyboards.inline import choice_way_input_payment_func
from loader import dp, bot
from utils import send_all_admin, clear_firstname
from utils.db_api.sqlite import get_paymentx, update_paymentx


###################################################################################
########################### ВКЛЮЧЕНИЕ/ВЫКЛЮЧЕНИЕ ПОПОЛНЕНИЯ #######################
# Включение пополнения
@dp.message_handler(IsAdmin(), text=["🔴 Disable deposits","🔴 Выключить пополнения"], state="*")
async def turn_off_refill(message: types.Message, state: FSMContext):
    await state.finish()
    if lang(message.from_user.id)=='Eng':
        update_paymentx(status="False")
        await message.answer("<b>🔴 Deposits in the bot were turned off.</b>",
                            reply_markup=payment_default(message.from_user.id))
        await send_all_admin(
            f"👤 Administrator <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a>\n"
            "🔴 Turned off deposits in the bot.", not_me=message.from_user.id)
    else:
        update_paymentx(status="False")
        await message.answer("<b>🔴 Пополнения в боте были выключены.</b>",
                            reply_markup=payment_default(message.from_user.id))
        await send_all_admin(
            f"👤 Администратор <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a>\n"
            "🔴 Выключил пополнения в боте.", not_me=message.from_user.id)

# Выключение пополнения
@dp.message_handler(IsAdmin(), text=["🟢 Enable deposits","🟢 Включить пополнения"], state="*")
async def turn_on_refill(message: types.Message, state: FSMContext):
    await state.finish()
    if lang(message.from_user.id)=='Eng':
        update_paymentx(status="True")
        await message.answer("<b>🟢 Deposits in the bot have been enabled.</b>",
                            reply_markup=payment_default(message.from_user.id))
        await send_all_admin(
            f"👤 Administrator <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a>\n"
            "🟢 Enabled deposits in the bot.", not_me=message.from_user.id)
    else:
        update_paymentx(status="True")
        await message.answer("<b>🟢 Пополнения в боте были включены.</b>",
                            reply_markup=payment_default(message.from_user.id))
        await send_all_admin(
            f"👤 Администратор <a href='tg://user?id={message.from_user.id}'>{clear_firstname(message.from_user.first_name)}</a>\n"
            "🟢 Включил пополнения в боте.", not_me=message.from_user.id)

###################################################################################
############################# ВЫБОР СПОСОБА ПОПОЛНЕНИЯ ############################
# Выбор способа пополнения
@dp.callback_query_handler(IsAdmin(), text_startswith="change_payment:")
async def input_amount(call: CallbackQuery):
    way_pay = call.data[15:]
    change_pass = False
    get_payment = get_paymentx()
    if way_pay == "nickname":
        try:
            request = requests.Session()
            request.headers["authorization"] = "Bearer " + get_payment[1]
            get_nickname = request.get(f"https://edge.qiwi.com/qw-nicknames/v1/persons/{get_payment[0]}/nickname")
            check_nickname = json.loads(get_nickname.text).get("nickname")
            if check_nickname is None:
                await call.answer("❗ There is no QIWI Nickname on the account")
            else:
                update_paymentx(qiwi_nickname=check_nickname)
                change_pass = True
        except json.decoder.JSONDecodeError:
            await call.answer("❗ QIWI wallet is not working.\n❗ Install it as soon as possible", True)
    else:
        change_pass = True
    if change_pass:
        update_paymentx(way_payment=way_pay)
        if lang(call.from_user.id)=='Eng':
            await bot.edit_message_text("🥝 Choose a deposit method 💵\n"
                                        "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                        "🔸 <b>Form</b> - <code>Ready-made form of payment QIWI</code>\n"
                                        "🔸 <b>Number</b> - <code>Transfer of funds by phone number</code>\n"
                                        "🔸 <b>Nickname</b> - "
                                        "<code>Transfer of funds by nickname (users will have to manually enter a comment)</code>",
                                        call.from_user.id,
                                        call.message.message_id,
                                        reply_markup=choice_way_input_payment_func(call.from_user.id))
        else:
            await bot.edit_message_text("🥝 Выберите способ пополнения 💵\n"
            "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            "🔸 <b>По форме</b> - <code>Готовая форма оплаты QIWI</code>\n"
            "🔸 <b>По номеру</b> - <code>Перевод средств по номеру телефона</code>\n"
            "🔸 <b>По никнейму</b> - "
            "<code>Перевод средств по никнейму (пользователям придётся вручную вводить комментарий)</code>",
            call.from_user.id,
            call.message.message_id,
            reply_markup=choice_way_input_payment_func(call.from_user.id))

