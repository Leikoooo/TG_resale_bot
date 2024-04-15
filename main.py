# - *- coding: utf- 8 - *-
import asyncio

from aiogram import executor
import filters
import middlewares
from handlers import dp
from utils.db_api.sqlite import create_bdx
from utils.other_func import *
from utils.set_bot_commands import set_default_commands
import sqlite3
from handlers.users.seleium import pushup
path_to_db = "botBD.sqlite"
async def on_startup(dp):
    filters.setup(dp)
    middlewares.setup(dp)
    await set_default_commands(dp)
    await on_startup_notify(dp)
    asyncio.create_task(pushup())
    asyncio.create_task(update_last_profit())
    print("---------------The bot is running---------------")

def re_lang(user_id, language):
    with sqlite3.connect(path_to_db) as db:
        db.execute(f"UPDATE Language SET lang='{language}' WHERE user_id = ?", [user_id])
        db.commit()

def lang(user_id):
    with sqlite3.connect(path_to_db) as db:
        get_response = db.execute(f"SELECT lang FROM Language WHERE user_id = ?", [user_id])
        get_response = get_response.fetchone()
    return get_response[0]

if __name__ == "__main__":
    create_bdx()
    update_profit()
    executor.start_polling(dp, on_startup=on_startup)
