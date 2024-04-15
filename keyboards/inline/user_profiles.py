# - *- coding: utf- 8 - *-
from utils.db_api.sqlite import get_userx, get_purchasesx, sum_price
from main import lang
def get_user_profile(user_id):
    get_user = get_userx(user_id=user_id)
    get_purchases = get_purchasesx("*", user_id=user_id)
    count_items = 0
    if len(get_purchases) >= 1:
        for items in get_purchases:
            count_items += int(items[5])
    msg = f"<b> Your profile:</b>\n" \
        f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
        f"🔑 My ID: <code>{get_user[1]}</code>\n" \
        f"👤 Login: <b>@{get_user[2]}</b>\n" \
        f"🕜 Registration: <code>{get_user[6]}</code>\n" \
        f"💳 Balance: <code>{get_user[4]}$</code>\n" 
    return msg


def search_user_profile(user_id):
    get_status_user = get_userx(user_id=user_id)
    get_purchases = get_purchasesx("*", user_id=user_id)
    count_items = 0
    if len(get_purchases) >= 1:
        for items in get_purchases:
            count_items += int(items[5])
    msg = f"<b> User Profile:</b> <a href='tg://user?id={get_status_user[1]}'>{get_status_user[3]}</a>\n" \
        f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
        f"🔑 ID: <code>{get_status_user[1]}</code>\n" \
        f"👤 Login: <b>@{get_status_user[2]}</b>\n" \
        f"Ⓜ Name: <a href='tg://user?id={get_status_user[1]}'>{get_status_user[3]}</a>\n" \
        f"🕜 Registration: <code>{get_status_user[6]}</code>\n" \
        f"💳 Balance: <code>{get_status_user[4]}$</code>\n" 
    return msg
