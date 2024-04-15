# - *- coding: utf- 8 - *-
import json
import random
import time

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from main import lang
from keyboards.default import all_back_to_main_default, check_user_out_func
from keyboards.inline import *
from loader import dp, bot
from states.state_payment import *
from states.state_users import StorageUsers
from utils import send_all_admin, clear_firstname, get_dates
from utils.db_api.sqlite import update_userx, get_refillx, add_refillx, remove_check, get_check, add_check
from data.config import *
from handlers.users.seleium import get_page
import datetime



###################################################################################
############################## ВВОД СУММЫ ПОПОЛНЕНИЯ ##############################
# Выбор способа пополнения
@dp.callback_query_handler(text="choice_lz", state="*")
async def choice_trz(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    trz = InlineKeyboardMarkup()
    btc = InlineKeyboardButton(text="BTC", callback_data="user_input_BTC")
    ltc = InlineKeyboardButton(text="LTC", callback_data="user_input_LTC")
    eth = InlineKeyboardButton(text="ETH", callback_data="user_input_ETH")
    usdt1 = InlineKeyboardButton(text="USDT", callback_data="user_input_USDT")
    bnb = InlineKeyboardButton(text="BNB", callback_data="user_input_BNB")
    trz.add(usdt1, btc,eth)
    trz.add(ltc, bnb)
    await call.message.answer("<b>💵 Choose a payment system 💵</b>",
        reply_markup=trz)

def currency(suma, cur):
    url = "https://alpha-vantage.p.rapidapi.com/query"
    querystring = {"from_currency":f"{cur}","function":"CURRENCY_EXCHANGE_RATE","to_currency":"USD"}
    headers = {
            'x-rapidapi-host': "alpha-vantage.p.rapidapi.com",
            'x-rapidapi-key': "fcf32db4a8mshe171c026c639873p1829d7jsn49fcac8013b5"
            }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_dict=response.json()
    Curs = response_dict['Realtime Currency Exchange Rate']['5. Exchange Rate']
    return float(suma)/float(Curs)


def trun_n_d(n,d):
    return int(n*10**d)/10**d

@dp.callback_query_handler(text_startswith="user_input", state="*")
async def choice_trz(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data[11:]=='USDT':
        trz = InlineKeyboardMarkup()
        usdt2 = InlineKeyboardButton(text="BnB Smart Chain (BEP20)", callback_data="user_input_USDT2")
        usdt3 = InlineKeyboardButton(text="Tron (TRC20)", callback_data="user_input_USDT3")
        back = InlineKeyboardButton(text="Back", callback_data="choice_lz")
        trz.add(usdt2, usdt3)
        trz.add(back)
        await call.message.answer("<b>💵 Choose network 💵</b>",
            reply_markup=trz)
        return
    if call.data[11:] == 'USDT1':
        await state.finish()
        await call.message.answer("This payment system is not available")
        return
    await StoragePay.here_input_suma.set()
    await state.update_data(here_input_curr=call.data[11:])
    await call.message.answer(f"<b>💵 Enter deposit amount 💵</b>\nMinimum Top Up Amount - <code>{min_cash}$</code>")

@dp.message_handler(state=StoragePay.here_input_suma)
async def input_buy_count_item(message: types.Message, state: FSMContext):
    curr = await state.get_data()
    curr=curr['here_input_curr']
    if message.text.replace('.', '',1).replace(',', '',1).isdigit():
        suma = message.text.replace(',', '.',1)
        if float(suma)<min_cash:
            await state.finish()
            await message.answer(f'Minimum Top Up Amount - {min_cash}$')
            return
    else:
        await state.finish()
        await message.answer('Wrong format')
        return
    if curr=='BTC':
        curs='BTC'
        wallet=wallet_btc
        suma_cur=trun_n_d(float(currency(suma, "BTC")) + (random.randint(-100, 100)/100000000),8)
    elif curr=='LTC':
        curs= 'LTC'
        wallet=wallet_ltc
        suma_cur=trun_n_d(float(currency(suma, "LTC")) + (random.randint(-100, 100)/100000000),8)
    elif curr=='USDT1':
        curs='USDT - Ethereum ERC20'
        wallet=wallet_usdt1
        suma_cur=trun_n_d(float(currency(suma, 'USDT')) + (random.randint(-100, 100)/100000000),8)
    elif curr=='USDT2':
        curs='USDT - Smart Chain BEP20'
        wallet=wallet_usdt2
        suma_cur=trun_n_d(float(currency(suma, 'USDT')) + (random.randint(-100, 100)/100000000),8)
    elif curr=='BNB1':
        curs='BNB - Smart Chain BEP20'
        wallet=wallet_BNB1
        suma_cur=trun_n_d(float(currency(suma, 'BNB')) + (random.randint(-100, 100)/100000000),8)
    elif curr=='USDT3':
        curs='USDT - Tron TRC20'
        wallet=wallet_usdt3
        suma_cur=trun_n_d(float(currency(suma, 'USDT')) + (random.randint(-100, 100)/1000000),6)
    else:
        curs='ETH'
        wallet=wallet_eth
        suma_cur=trun_n_d(float(currency(suma, 'ETH')) + (random.randint(-100, 100)/100000000),8)
    await state.finish()
    date = datetime.datetime.now().strftime('%d-%H-%M') # Дата
    if get_check(message.from_user.id)==None:
        add_check(message.from_user.id,suma_cur, suma, curr, date)
        await bot.send_photo(message.from_user.id, photo=open(f'QR/{curr}.png', 'rb'), caption=f"You have to send <code>{suma_cur}</code> <b>{curs}</b>\nWallet to send: <code>{wallet}</code>\nWhen payment is made, bot will send you a message",
                        reply_markup=check_payment_crystal(message.from_user.id))
    else:
        remove_check(message.from_user.id)
        add_check(message.from_user.id,suma_cur,suma, curr, date)
        await bot.send_photo(message.from_user.id, photo=open(f'QR/{curr}.png', 'rb'), caption=f"You have to send <code>{suma_cur}</code> <b>{curs}</b>\nWallet to send: <code>{wallet}</code>\nWhen payment is made, bot will send you a message",
                    reply_markup=check_payment_crystal(message.from_user.id))

@dp.callback_query_handler(text_startswith="paid")
async def payment_check_commands(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split(':')[1]
    await bot.delete_message(chat_id=callback_query.from_user.id,
                        message_id=callback_query.message.message_id)
    await callback_query.message.answer(text='Good, we will check your payment soon, wait for a message')

@dp.callback_query_handler(text_startswith="otmena:")
async def payment_check_commands(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split(':')[1]
    remove_check(user_id)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                        message_id=callback_query.message.message_id)

@dp.callback_query_handler(text_startswith="check:")
async def payment_check_commands(call: types.CallbackQuery):
    del_mes = await call.message.answer('Expect verification')
    user_id = call.data.split(':')[1]
    data=get_check(call.from_user.id)
    try:
        check, text= get_page(data[1],data[3])
    except Exception as e:
        print(e)
        await call.answer("The transaction is invalid, create a new one")
        return
    pay_amount= data[2]
    get_user_info = get_userx(user_id=call.from_user.id)
    if check:
        if text=='':
            await bot.delete_message(call.from_user.id, del_mes.message_id)
            await bot.delete_message(call.from_user.id, call.message.message_id)
            update_userx(call.from_user.id,
                balance=str(round(float(get_user_info[4]) + float(pay_amount),2)),
                all_refill=str(round(float(get_user_info[7]) + float(pay_amount),2)))
            remove_check(call.from_user.id)
            await bot.send_message(chat_id=call.from_user.id,text=f"<b>✅ You have successfully topped up your balance in the amount of {pay_amount}$. Good luck ❤</b>\n")
            await send_all_admin(f"<b>💰 User</b> "
                                    f"(@{call.from_user.username}|<a href='tg://user?id={call.from_user.id}'>{call.from_user.first_name}</a>"
                                    f"|<code>{call.from_user.id}</code>) "
                                    f"<b>replenished the balance by the amount of</b> <code>{pay_amount}$</code> 🥝\n")
        else:
            await bot.delete_message(call.from_user.id, del_mes.message_id)
            await call.answer(text)
    else:
        await bot.delete_message(call.from_user.id, del_mes.message_id)
        await call.answer("Payment has not been made")


