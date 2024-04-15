# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from filters import IsWork, IsUser
from filters.all_filters import IsBuy
from keyboards.default import check_user_out_func
from keyboards.inline.user_inline import lang_inl
from loader import dp, bot
from states import StorageUsers
from utils.db_api.sqlite import *
from utils.other_func import clear_firstname, get_dates
from aiogram.types import CallbackQuery
from keyboards.inline.user_func import *
from keyboards.inline.admin_func import *
prohibit_buy = ["xbuy_item", "not_buy_items", "buy_this_item", "buy_open_position", "back_buy_item_position",
                "buy_position_prevp", "buy_position_nextp", "buy_category_prevp", "buy_category_nextp",
                "back_buy_item_to_category", "buy_open_category"]


# Проверка на нахождение бота на технических работах
@dp.message_handler(IsWork(), state="*")
@dp.callback_query_handler(IsWork(), state="*")
async def send_work_message(message: types.Message, state: FSMContext):
    await message.answer("<b>🔴 Bot on technical work.</b>")


# Обработка кнопки "На главную" и команды "/start"
@dp.message_handler(text=["⬅ To the main page",'⬅ На главную'], state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Главная',reply_markup=check_user_out_func(message.from_user.id))


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    first_name = clear_firstname(message.from_user.first_name)
    get_user_id = get_userx(user_id=message.from_user.id)
    if get_user_id is None:
        if message.from_user.username is not None:
            get_user_login = get_userx(user_login=message.from_user.username)
            if get_user_login is None:
                add_userx(message.from_user.id, message.from_user.username.lower(), first_name, 0, 0, get_dates(), 0)
            else:
                delete_userx(user_login=message.from_user.username)
                add_userx(message.from_user.id, message.from_user.username.lower(), first_name, 0, 0, get_dates(), 0)
        else:
            add_userx(message.from_user.id, message.from_user.username, first_name, 0, 0, get_dates(), 0)
    else:
        if first_name != get_user_id[3]:
            update_userx(get_user_id[1], user_name=first_name)
        if message.from_user.username is not None:
            if message.from_user.username.lower() != get_user_id[2]:
                update_userx(get_user_id[1], user_login=message.from_user.username.lower())
    await message.answer("<b>🔸 The bot is ready to use.</b>\n"
                         "🔸 If auxiliary buttons do not appear\n"
                         "▶ Enter /start",
                         reply_markup=check_user_out_func(message.from_user.id))


@dp.callback_query_handler(text=["⬅ To the main page",'⬅ На главную'], state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Главная',reply_markup=check_user_out_func(call.from_user.id))
    await call.message.delete()

@dp.message_handler(IsUser(), state="*")
@dp.callback_query_handler(IsUser(), state="*")
async def send_user_message(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id,
                           "<b>❗ Профиль не был найден.</b>\n"
                           "▶ Нажмите /start")


# Проверка на доступность покупок
@dp.message_handler(IsBuy(), text=['💰 Купить',"💰 Buy"], state="*")
@dp.message_handler(IsBuy(), state=StorageUsers.here_input_count_buy_item)
@dp.callback_query_handler(IsBuy(), text_startswith=prohibit_buy, state="*")
async def send_user_message(message, state: FSMContext):
    if "id" in message:
        await message.answer("🔴 Purchases in the bot are temporarily disabled", True)
    else:
        await message.answer("<b>🔴 Purchases in the bot are temporarily disabled</b>")
