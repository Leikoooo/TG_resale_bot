# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from filters import IsAdmin
from keyboards.default import get_settings_func, payment_default, get_functions_func, items_default, admins
from keyboards.inline import choice_way_input_payment_func
from loader import dp, bot
from utils import get_dates
from utils.db_api.sqlite import *
from main import lang

# -----------------------------------------------------Переведен------------------------------------------------------------



# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]



# Обработка кнопки "Настройки бота"
@dp.message_handler(IsAdmin(), text=["Settings"], state="*")
async def settings_bot(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("⚙ Basic bot Settings.", reply_markup=get_settings_func(message.from_user.id))

# Обработка кнопки "Общие функции"
@dp.message_handler(IsAdmin(), text=["Functions"], state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Select the desired function.", reply_markup=get_functions_func(message.from_user.id))


# Обработка кнопки "Общие функции"
@dp.message_handler(IsAdmin(), text=["Info"], state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    about_bot = get_about_bot(message.from_user.id)
    await message.answer(about_bot)


# Обработка кнопки "Управление товарами"
@dp.message_handler(IsAdmin(), text=["Product Management","💰 Управление товарами"], state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("💰 Editing products, positions and categories 📜",
                            reply_markup=items_default(message.from_user.id))

# Получение БД
@dp.message_handler(IsAdmin(), text="/getbd", state="*")
async def general_functions(message: types.Message, state: FSMContext):
    await state.finish()
    for admin in admins:
        with open("data/botBD.sqlite", "rb") as doc:
            await bot.send_document(admin,
                                    doc,
                                    caption=f"<b>📦 BACKUP</b>\n"
                                            f"<code>🕜 {get_dates()}</code>")


def get_about_bot(user_id):
    show_profit_day = 0
    show_profit_all = 0
    get_settings = get_settingsx()
    all_purchases = get_all_purchasesx()
    show_users = get_all_usersx()
    for purchase in all_purchases:
        show_profit_all += round(float(purchase[6]),2)
        if float(get_settings[4]) - float (purchase[14]) < 86400:
            show_profit_day += round(float(purchase[6]), 2)
    message = "<b>📰 ВСЯ ИНФОРМАЦИЯ О БОТЕ</b>\n" \
            f"➖➖➖➖➖➖➖➖➖➖➖➖\n" \
            f"<b>🔶 Пользователи: 🔶</b>\n" \
            f"👤 Пользователей: <code>{len(show_users)}</code>\n" \
            f"➖➖➖➖➖➖➖➖➖➖➖➖\n" \
            f"<b>🔶 Средства 🔶</b>\n" \
            f"💰 Продано товаров за 24ч: <code>{round(show_profit_day,2)}$</code>\n"\
            f"💰 Продано товаров на: <code>{round(show_profit_all,2)}$</code>\n"
    return message


# Получение списка всех товаров
@dp.message_handler(IsAdmin(), text="/getitems", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = get_all_itemsx()
    len_items = len(get_items)
    if len_items >= 1:
        if lang(message.from_user.id)=='Eng':
            await message.answer("<b>💰 All items</b>\n"
                                "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                "<code>📍 ID item - item data</code>\n"
                                "➖➖➖➖➖➖➖➖➖➖➖➖\n")
        else:
            await message.answer("<b>💰 Все товары</b>\n"
                                "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                "<code>📍 айди товара - данные товара</code>\n"
                                "➖➖➖➖➖➖➖➖➖➖➖➖\n")
        for item in get_items:
            save_items.append(f"<code>📍 {item[1]} - {item[2]}</code>")
        if len_items >= 20:
            count_split = round(len_items / 20)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message)
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message)
    else:
        if lang(message.from_user.id)=='Eng':
            await message.answer("<b>💰 Items are missing</b>")
        else:
            await message.answer("<b>💰 Товары отсутствуют</b>")

# Получение списка всех позиций
@dp.message_handler(IsAdmin(), text="/getposition", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = get_all_positionsx()
    len_items = len(get_items)
    if len_items >= 1:
        if lang(message.from_user.id)=='Eng':
            await message.answer("<b>📁 All positions</b>\n➖➖➖➖➖➖➖➖➖➖➖➖\n")
        else:
            await message.answer("<b>📁 Все позиции</b>\n➖➖➖➖➖➖➖➖➖➖➖➖\n")
        for item in get_items:
            save_items.append(f"<code>{item[2]}</code>")
        if len_items >= 35:
            count_split = round(len_items / 35)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message)
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message)
    else:
        if lang(message.from_user.id)=='Eng':
            await message.answer("<b>📁 There are no positions</b>")
        else:
            await message.answer("<b>📁 Позиции отсутствуют</b>")    


# Получение подробного списка всех товаров
@dp.message_handler(IsAdmin(), text="/getinfoitems", state="*")
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.finish()
    save_items = []
    count_split = 0
    get_items = get_all_itemsx()
    len_items = len(get_items)
    if len_items >= 1:
        await message.answer("<b>💰 All items and their positions</b>\n"
                                "➖➖➖➖➖➖➖➖➖➖➖➖\n")
        for item in get_items:
            get_position = get_positionx("*", position_id=item[3])
            save_items.append(f"<code>{get_position[2]} - {item[2]}</code>")
        if len_items >= 20:
            count_split = round(len_items / 20)
            count_split = len_items // count_split
        if count_split > 1:
            get_message = split_messages(save_items, count_split)
            for msg in get_message:
                send_message = "\n".join(msg)
                await message.answer(send_message)
        else:
            send_message = "\n".join(save_items)
            await message.answer(send_message)
    else:
            await message.answer("<b>💰 Items are missing</b>")
