# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.default import check_user_out_func, all_back_to_main_default
from keyboards.inline import *
from keyboards.inline.inline_page import *
from loader import dp, bot
from states.state_users import *
from states.state_settings import *
from utils.other_func import clear_firstname, get_dates, send_all_admin
from main import lang
# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ

def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]

@dp.message_handler(text=["💵 Deposit"], state="*")
async def show_search(message: types.Message, state: FSMContext):
    trz = InlineKeyboardMarkup()
    btc = InlineKeyboardButton(text="BTC", callback_data="user_input_BTC")
    ltc = InlineKeyboardButton(text="LTC", callback_data="user_input_LTC")
    eth = InlineKeyboardButton(text="ETH", callback_data="user_input_ETH")
    usdt1 = InlineKeyboardButton(text="USDT", callback_data="user_input_USDT")
    bnb = InlineKeyboardButton(text="BNB", callback_data="user_input_BNB1")
    trz.add(usdt1, btc,eth)
    trz.add(ltc, bnb)
    await message.answer("<b>💵 Choose a payment system 💵</b>",
        reply_markup=trz)

@dp.message_handler(text=["🔉 Social media"], state="*")
async def show_search(message: types.Message, state: FSMContext):
    await state.finish()
    category_id = get_category_id('🔉 Social media')
    get_kb = buy_item_open_podcategory_ap(0, '🔉 Social media')
    if len(category_id) >= 1:
        await message.answer("<b>Select platform:</b>",
                                    reply_markup=get_kb)
    else:
        await message.answer(f"❗️Items in the tab missing.")

@dp.message_handler(text=["⚔️ Games"], state="*")
async def show_search(message: types.Message, state: FSMContext):
    await state.finish()
    category_id = get_category_id('⚔️ Games')
    get_kb = buy_item_open_podcategory_ap(0, '⚔️ Games')
    if len(category_id) >= 1:
        await message.answer("<b>Select platform:</b>",
                                    reply_markup=get_kb)
    else:
        await message.answer(f"❗️Items in the tab missing.")

@dp.callback_query_handler(text_startswith="buy_open_podcategory", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    await state.finish()
    category_id = int(call.data.split(":")[1])
    get_category = get_categoryx("*", podcategory_id=category_id)
    get_kb = buy_item_item_category_ap(0, category_id)
    if len(get_category) >= 1:
        await call.message.edit_text("<b>Сhoose receiving method:</b>",
                                    reply_markup=get_kb)
    else:
        await call.answer(f"❗️Items in the tab missing.")

@dp.callback_query_handler(text="pokupki", state="*")
async def show_referral(call: CallbackQuery, state: FSMContext):
    await state.finish()
    get_categories = get_all_podcategoriesx()
    if len(get_categories) >= 1:
        get_kb = buy_item_open_podcategory_ap(0)
        await call.message.answer("<b>Выберите нужный вам товар:</b>", reply_markup=get_kb)
    else:
        await call.message.answer("<b>Товары в данное время отсутствуют.</b>")

# Обработка кнопки "Профиль"
@dp.message_handler(text=["Профиль","Profile"], state="*")
async def show_profile(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(get_user_profile(message.from_user.id))

# Обработка кнопки "FAQ"
@dp.message_handler(text="FAQ", state="*")
async def show_my_deals(message: types.Message, state: FSMContext):
    await state.finish()
    get_settings = get_settingsx()
    send_msg = get_settings[1]
    if "{username}" in str(send_msg):
        send_msg = send_msg.replace("{username}", f"<b>{message.from_user.username}</b>")
    if "{user_id}" in str(send_msg):
        send_msg = send_msg.replace("{user_id}", f"<b>{message.from_user.id}</b>")
    if "{firstname}" in str(send_msg):
        send_msg = send_msg.replace("{firstname}", f"<b>{clear_firstname(message.from_user.first_name)}</b>")
    await message.answer(send_msg, disable_web_page_preview=True)

################################################################################################
######################################### ПОКУПКА ТОВАРА #######################################
# Открытие категории для покупки
@dp.callback_query_handler(text_startswith="buy_open_podcategory", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    podcategory_id = int(call.data.split(":")[1])
    get_podcategory=get_podcategoryx("*", category_id=podcategory_id)
    get_category = get_categoryx("*", podcategory_id=podcategory_id)
    get_kb = buy_item_item_category_ap(0, podcategory_id)
    if lang(call.from_user.id)=='Eng':
        if len(get_category) >= 1:
            await call.message.edit_text("<b>Select an item:</b>",
                                        reply_markup=get_kb)
        else:
            await call.answer(f"❕ Products in the category {get_podcategory[2]} missing.")
    else:
        if len(get_category) >= 1:
            await call.message.edit_text("<b>Выберите нужный вам товар:</b>",
                                        reply_markup=get_kb)
        else:
            await call.answer(f"❕ Товары в категории {get_podcategory[2]} отсутствуют.")

@dp.callback_query_handler(text_startswith="buy_open_category", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    await state.finish()
    category_id = int(call.data.split(":")[1])
    get_category = get_categoryx("*", category_id=category_id)
    get_positions = get_positionsx("*", category_id=category_id)

    get_kb = buy_item_item_position_ap(0, category_id)
    if lang(call.from_user.id)=='Eng':
        if len(get_positions) >= 1:
            await call.message.edit_text("<b>Select an item:</b>",
                                        reply_markup=get_kb)
        else:
            await call.answer(f"❕ Items in the tab {get_category[0][2]} missing.")
    else:
        if len(get_positions) >= 1:
            await call.message.edit_text("<b>Выберите нужный вам товар:</b>",
                                        reply_markup=get_kb)
        else:
            await call.answer(f"❕ Товары во вкладке {get_category[0][2]} отсутствуют.")

# Вернутсья к предыдущей категории при покупке
@dp.callback_query_handler(text_startswith="back_buy:", state="*")
async def back_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    category_id=int(call.data.split(":")[1])
    get_category = get_categoryx("*", category_id=category_id)
    get_podcatygory = get_podcategoryx("*", category_id=get_category[0][3])
    if get_podcatygory[3]=='🔉 Social media':
        await call.message.edit_text("<b>Select an item:</b>",
                                    reply_markup=buy_item_open_podcategory_ap(0,'🔉 Social media'))
    else:
        await call.message.edit_text("<b>Select an item:</b>",
                                    reply_markup=buy_item_open_podcategory_ap(0, '⚔️ Games'))


# Следующая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_category_nextp", state="*")
async def buy_item_next_page_category(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    if lang(call.from_user.id)=='Eng':
        await call.message.edit_text("<b>Select an item:</b>",
                                    reply_markup=buy_item_next_page_category_ap(remover))
    else:
        await call.message.edit_text("<b>Выберите нужный вам товар:</b>",
                                    reply_markup=buy_item_next_page_category_ap(remover))

# Предыдущая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_category_prevp", state="*")
async def buy_item_prev_page_category(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    if lang(call.from_user.id)=='Eng':
        await call.message.edit_text("<b>Select an item:</b>",
                                    reply_markup=buy_item_previous_page_category_ap(remover))
    else:
        await call.message.edit_text("<b>Выберите нужный вам товар:</b>",
                                    reply_markup=buy_item_previous_page_category_ap(remover))
# Следующая страница позиций при покупке
@dp.callback_query_handler(text_startswith="buy_position_nextp", state="*")
async def buy_item_next_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    if lang(call.from_user.id)=='Eng':
        await call.message.edit_text("<b>Select the product you need:</b>",
                                    reply_markup=item_buy_next_page_position_ap(remover, category_id))
    else:
        await call.message.edit_text("<b>Выберите нужный вам товар:</b>",
                                    reply_markup=item_buy_next_page_position_ap(remover, category_id))
    
# Предыдущая страница позиций при покупке
@dp.callback_query_handler(text_startswith="buy_position_prevp", state="*")
async def buy_item_prev_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    if lang(call.from_user.id)=='Eng':
        await call.message.edit_text("<b>Select an item:</b>",
                                    reply_markup=item_buy_previous_page_position_ap(remover, category_id))
    else:
        await call.message.edit_text("<b>Выберите нужный вам товар:</b>",
                                    reply_markup=item_buy_previous_page_position_ap(remover, category_id))

# Возвращение к страницам позиций при покупке товара
@dp.callback_query_handler(text_startswith="back_buy_item_position", state="*")
async def buy_item_next_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.delete()
    if lang(call.from_user.id)=='Eng':
        await call.message.answer("<b>Select an item:</b>",
                        reply_markup=buy_item_item_position_ap(remover, category_id))
    else:
        await call.message.answer("<b>Выберите нужный вам товар:</b>",
                              reply_markup=buy_item_item_position_ap(remover, category_id))


# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="buy_open_position", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])
    get_position = get_positionx("*", position_id=position_id)
    get_category = get_categoryx("*", category_id=category_id)[0]
    get_items = get_itemsx("*", position_id=position_id)
    get_podcategory= get_podcategoriesx("*", category_id=get_category[3])[0]
    send_msg = f"<b>Purchase of item:</b>\n" \
                "➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                f"<b>📜 Platform:</b> <code>{get_podcategory[2]}</code>\n" \
                f"<b>📜 Receiving:</b> <code>{get_category[2]}</code>\n" \
                f"<b>📜 Item:</b> <code>{get_position[2]}</code>\n" \
                f"<b>💵 Price:</b> <code>{get_position[3]}$</code>\n\n" \
                f"<b>Description:</b>\n" \
                f"{get_position[4]}\n"

    if len(get_position[5]) >= 5:
        await call.message.delete()
        await call.message.answer_photo(get_position[5],
                                        send_msg,
                                        reply_markup=open_item_func(position_id, remover, category_id, call.from_user.id))
    else:
        await call.message.edit_text(send_msg,
                                     reply_markup=open_item_func(position_id, remover, category_id, call.from_user.id))

# Выбор кол-ва товаров для покупки
@dp.callback_query_handler(text_startswith="buy_this_item", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    get_items = get_itemsx("*", position_id=position_id)
    get_position = get_positionx("*", position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    async with state.proxy() as data:
        data["here_cache_position_id"] = position_id
    await call.message.delete()
    # Проверка на ввод данных от аккаунта 
    category = get_categoryx("*", category_id=get_position[7])[0]
    if category[4] == "Да":
        await StorageUsers.here_input_data.set()
        await call.message.answer(f"Введите данные от аккаунта, на который хотите купить подписку")
    else:
        add_data(call.from_user.id, position_id, "Данных нет")
        get_position = get_positionx("*", position_id=position_id)
        await call. message.answer(f"Are you sure you want to buy this item?", reply_markup=confirm_buy_items(get_position[3], call.from_user.id))


@dp.message_handler(state=StorageUsers.here_input_data)
async def input_buy_count_item(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data["here_cache_position_id"]
    add_data(message.from_user.id, position_id, message.text)
    get_position = get_positionx("*", position_id=position_id)
    await message.answer(f"Данные от аккаунта успешно добавлены, Are you sure you want to buy this item?", reply_markup=confirm_buy_items(get_position[3], message.from_user.id))

# Отмена покупки товара
@dp.callback_query_handler(text_startswith="not_buy_items", state="*")
async def not_buy_this_item(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("<b>You have canceled the purchase of an item</b>",
                                reply_markup=check_user_out_func(call.from_user.id))

@dp.callback_query_handler(text_startswith="get_item:", state="*")
async def yes_buy_this_item(call: CallbackQuery, state: FSMContext):
    user_id= call.data.split(':')[1]
    await StorageUsers.here_input_message.set()
    await state.update_data(message=user_id)
    await bot.send_message(call.from_user.id, "Введите сообщение, которое хотите отправить")

@dp.message_handler(state=StorageUsers.here_input_message)
async def input_buy_count_item(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data["message"]
    await bot.send_message(user_id, message.text)
    await message.answer("Сообщение успешно отправлено")
# Согласие на покупку товара
@dp.callback_query_handler(text_startswith="xbuy_item:", state="*")
async def yes_buy_this_item(call: CallbackQuery, state: FSMContext):
    amount_pay = int(call.data.split(":")[1])
    await call.message.delete()
    get_user = get_userx(user_id=call.from_user.id)
    position_id = get_data(call.from_user.id)[1]
    position = get_positionx("*", position_id=position_id)
    podcategory_id = get_categoryx("*", category_id=position[7])[0]
    podcategory = get_podcategoryx("*", category_id=podcategory_id[3])
    if float(get_user[4]) >= amount_pay:
        buy_time = get_dates()
        text=get_data(call.from_user.id)[2]
        update_userx(call.from_user.id, balance=float(get_user[4]) - amount_pay)
        add_purchasex(call.from_user.id, call.from_user.username, call.from_user.first_name,
                'receipt', 1, amount_pay, position[3], position[1], position[2],
                'save_items', get_user[4], float(str(get_user[4])) - amount_pay, buy_time, int(time.time()))
        clear_data(call.from_user.id)
        await call.message.answer(f"<b>Вы успешно заказали подписку ✅</b>\n"
                    f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
                    f"💵 Сумма покупки: <code>{amount_pay}$</code>\n"
                    f"🏷 Категория: <code>{podcategory[2]}</code>\n"
                    f"👤 Покупатель: <a href='tg://user?id={get_user[1]}'>{get_user[3]}</a> <code>({get_user[1]})</code>\n"
                    f"🕜 Дата покупки: <code>{buy_time}</code>\n\nОжитайте ответа от администратора",
                    reply_markup=check_user_out_func(call.from_user.id))
        await send_all_admin(f"<b>Новый заказ</b>\n💵 Сумма покупки: <code>{amount_pay}$</code>\n@{call.from_user.username}|<a href='tg://user?id={call.from_user.id}'>{call.from_user.first_name}</a> | <code>{call.from_user.id}</code>\n"
        f"🏷 Категория: <code>{podcategory[2]}</code>\n🏷 Подкатегория: <code>{podcategory_id[2]}</code>\n🏷 Позиция: <code>{position[2]}</code>\nДанные заказа:\n{text}\n", markup=answer_body(call.from_user.id))
    else:
        await call.message.answer("<b>❗ There are not enough funds on your account</b>\n"
                    f"<b>❗️ Make a deposit</b>\n")