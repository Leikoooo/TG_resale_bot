# - *- coding: utf- 8 - *-
import datetime
import logging
import random
import sqlite3
import time
from data.config import bot_description
import datetime
# Путь к БД

path_to_db = "botBD.sqlite"

def logger(statement):
    logging.basicConfig(
        level=logging.INFO,
        filename="logs.log",
        format=f"[Executing] [%(asctime)s] | [%(filename)s LINE:%(lineno)d] | {statement}",
        datefmt="%d-%b-%y %H:%M:%S"
    )
    logging.info(statement)

def handle_silently(function):
    def wrapped(*args, **kwargs):
        result = None
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            logger("{}({}, {}) failed with exception {}".format(
                function.__name__, repr(args[1]), repr(kwargs), repr(e)))
        return result

    return wrapped


####################################################################################################
###################################### ФОРМАТИРОВАНИЕ ЗАПРОСА ######################################
# Форматирование запроса с аргументами
def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())


# Форматирование запроса без аргументов
def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())


####################################################################################################
########################################### ЗАПРОСЫ К БД ###########################################
# Добавление пользователя


def add_userx(user_id, user_login, user_name, balance, role, reg_date, all_refill):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_users "
                   "(user_id, user_login, user_name, balance,role,  reg_date, all_refill) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?)",
                   [user_id, user_login, user_name, balance, role, reg_date, all_refill])
        db.commit()
        db.execute("INSERT INTO Language "
            "(user_id, lang) "
            "VALUES (?, ?)",
            [user_id, 'Eng'])
        db.commit()

def add_packet(user_id,category_id, price, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO packet "
                   "(user_id, category_id, price)"
                   "VALUES (?, ?, ?)",
                   [user_id, category_id, price])
        db.commit()
def get_packet(user_id, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        packet=db.execute(f"SELECT * FROM packet where user_id = {user_id}").fetchall()
    return packet

# Изменение пользователя
def update_userx(user_id, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_users SET XXX WHERE user_id = {user_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


def update_seller(user_id, role):
    with sqlite3.connect(path_to_db) as db:
        db.execute(f"UPDATE storage_users SET role = {role}  WHERE increment = {user_id}")
        db.commit()

# Удаление пользователя
def delete_userx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "DELETE FROM storage_users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()
        db.execute('VACUUM')
        db.commit()

def add_data(user_id, position_id, data):
    with sqlite3.connect(path_to_db) as db:
        datas= db.execute('select data from storage_data where user_id = ? and position_id = ?', (user_id, position_id)).fetchone()
        if datas is None:
            db.execute("INSERT or ignore INTO storage_data "
                    "(user_id, position_id, data)"
                    "VALUES (?, ?, ?)",
                    [user_id, position_id, data])
            db.commit()
        else:
            db.execute("UPDATE storage_data SET data = ? WHERE user_id = ? and position_id = ?", (data, user_id, position_id))
            db.commit()

def add_check(user_id, suma_btc, suma, curr, date):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT or ignore INTO storage_check "
                   "(user_id, suma_btc, suma, curr, date) "
                   "VALUES (?, ?, ?, ?, ?)",
                   [user_id, str(suma_btc),str(suma), str(curr), str(date)])
        db.commit()

def remove_check(user_id):
    with sqlite3.connect(path_to_db) as db:
        db.execute(f"DELETE FROM storage_check WHERE user_id={user_id}")
        db.commit()

def get_check(user_id=None):
    with sqlite3.connect(path_to_db) as db:
        if user_id is None:
            get_response = db.execute(f"SELECT * FROM storage_check").fetchall()
        else:
            get_response = db.execute(f"SELECT * FROM storage_check WHERE user_id={user_id}").fetchone()
        return get_response

def clear_data(user_id):
    with sqlite3.connect(path_to_db) as db:
        db.execute(f"DELETE FROM storage_data WHERE user_id = {user_id}")
        db.commit()
        db.execute('VACUUM')
        db.commit()

def get_data(user_id):
    with sqlite3.connect(path_to_db) as db:
        data = db.execute(f"SELECT * FROM storage_data WHERE user_id = {user_id}").fetchone()
    return data

# Получение пользователя
def get_userx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response


def get_id(inc):
    with sqlite3.connect(path_to_db) as db:
        get_response = db.execute(f"SELECT * FROM storage_users WHERE increment={inc}")
        get_response = get_response.fetchone()
    return get_response

# Получение пользователей
def get_usersx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response


# Получение всех пользователей
def get_all_usersx():
    with sqlite3.connect(path_to_db) as db:
        get_response = db.execute("SELECT * FROM storage_users")
        get_response = get_response.fetchall()
    return get_response


# Получение платежных систем
def get_paymentx():
    with sqlite3.connect(path_to_db) as db:
        get_response = db.execute("SELECT * FROM storage_payment")
        get_response = get_response.fetchone()
    return get_response


# Изменение платежных систем
def update_paymentx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_payment SET XXX "
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


# Получение настроек
def get_settingsx():
    with sqlite3.connect(path_to_db) as db:
        get_response = db.execute("SELECT * FROM storage_settings")
        get_response = get_response.fetchone()
    return get_response


# Обновление настроек
def update_settingsx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_settings SET XXX "
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


# Добавление пополнения в БД
def add_refillx(user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_refill "
                   "(user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   [user_id, user_login, user_name, comment, amount, receipt, way_pay, dates, dates_unix])
        db.commit()


# Получение пополнения
def get_refillx(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_refill WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response


# Получение пополнений
def get_refillsx(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_refill WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response


# Получение всех пополнений
def get_all_refillx():
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_refill"
        get_response = db.execute(sql)
        get_response = get_response.fetchall()
    return get_response


# Добавление категории в БД
def add_categoryx(category_id, category_name, podcategory_id, need_data):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_category "
                   "(category_id, category_name, podcategory_id, need_data) "
                   "VALUES (?, ?, ?, ?)",
                   [category_id, category_name, podcategory_id, need_data])
        db.commit()

def add_podcategoryx(category_id, category_name, types):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_podcategory "
                   "(category_id, category_name, category_type) "
                   "VALUES (?, ?, ?)",
                   [category_id, category_name, types])
        db.commit()

# Изменение категории
def update_categoryx(category_id, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_category SET XXX WHERE category_id = {category_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


# Получение категории
def get_categoryx(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_category WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response

def get_podcategoryx(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_podcategory WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response


# Получение категорий
def get_categoriesx(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_category WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response


# Получение всех категорий
def get_all_categoriesx():
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_category"
        get_response = db.execute(sql)
        get_response = get_response.fetchall()
    return get_response

def get_all_podcategoriesx():
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_podcategory"
        get_response = db.execute(sql)
        get_response = get_response.fetchall()
    return get_response

def get_all_podcategoriesxs(types):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT * FROM storage_podcategory where category_type = '{types}'"
        get_response = db.execute(sql)
        get_response = get_response.fetchall()
    return get_response

def get_podcategoriesx(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_podcategory WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response

# Очистка подкатегорий
def clear_podcategoryx():
    with sqlite3.connect(path_to_db) as db:
        sql = "DELETE FROM storage_podcategory"
        db.execute(sql)
        db.commit()
        db.execute('VACUUM')
        db.commit()

def clear_packet(user_id):
    with sqlite3.connect(path_to_db) as db:
        sql = f"DELETE FROM packet where user_id={user_id}"
        db.execute(sql)
        db.commit()
        db.execute('VACUUM')
        db.commit()

# Удаление подтоваров
def remove_categoryx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "DELETE FROM storage_podcategory WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()
        db.execute('VACUUM')
        db.commit()

# Очистка категорий
def clear_categoryx():
    with sqlite3.connect(path_to_db) as db:
        sql = "DELETE FROM storage_category"
        db.execute(sql)
        db.commit()
        db.execute('VACUUM')
        db.commit()


# Удаление товаров
def remove_categoryx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "DELETE FROM storage_category WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()
        db.execute('VACUUM')
        db.commit()


# Добавление категории в БД
def add_positionx(position_id, position_name, position_price, position_discription, position_image, position_date,
                  category_id):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_position "
                   "(position_id, position_name, position_price, position_discription, position_image, position_date, category_id) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?)",
                   [position_id, position_name, position_price, position_discription, position_image,
                    position_date, category_id])
        db.commit()


# Изменение позиции
def update_positionx(position_id, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_position SET XXX WHERE position_id = {position_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


# Получение категории
def get_positionx(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_position WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response


# Получение категорий
def get_positionsx(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_position WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response


# Получение всех категорий
def get_all_positionsx():
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_position"
        get_response = db.execute(sql)
        get_response = get_response.fetchall()
    return get_response

# Очистка категорий
def clear_positionx():
    with sqlite3.connect(path_to_db) as db:
        sql = "DELETE FROM storage_position"
        db.execute(sql)
        db.commit()
        db.execute('VACUUM')
        db.commit()

def get_adress(user_id):
    with sqlite3.connect(path_to_db) as db:
        adrs=db.execute(f"SELECT * FROM adress WHERE user_id={user_id}").fetchone()
    return adrs

def re_sroki(user_id, srok, **kwargs):
    print(user_id,srok)
    try:
        with sqlite3.connect(path_to_db) as db:
            adrs=db.execute(f"SELECT * FROM adress WHERE user_id={user_id}").fetchone()
            if adrs==None:
                db.execute("INSERT INTO adress "
                        "(user_id, srok) "
                        "VALUES (?, ?)",
                        [user_id, srok])
                db.commit()
            else:
                db.execute(f"UPDATE adress SET srok='{srok}' WHERE user_id = {user_id}")
                db.commit()
    except Exception as e:
        print(e)

def sum_price(user_id):
    with sqlite3.connect(path_to_db) as db:
        get_response = db.execute(f"SELECT sum(item_price) FROM storage_purchases WHERE user_id=?",(user_id,))
        get_response = get_response.fetchone()
    if get_response[0]==None:
        return 0
    return get_response[0]

def re_adress(user_id, adress, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        adrs=db.execute(f"SELECT * FROM adress WHERE user_id={user_id}").fetchone()
        if adrs==None:
            db.execute("INSERT INTO adress "
                    "(user_id, adress) "
                    "VALUES (?, ?)",
                    [user_id, adress])
            db.commit()
        else:
            db.execute(f"UPDATE adress SET adress= '{adress}' WHERE user_id = {user_id}")
            db.commit()

def mapes():
    with sqlite3.connect(path_to_db) as db:
        adrs=db.execute(f"SELECT * FROM map").fetchall()
    return adrs

def get_map(map_id):
    with sqlite3.connect(path_to_db) as db:
        adrs=db.execute(f"SELECT * FROM map where increment={map_id}").fetchone()
    return adrs

def add_mapes(address, pic, link1, link2):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO map "
                "(address, pic, link1, link2)"
                "VALUES (?, ?, ?, ?)",
                [address, pic, link1, link2])
        db.commit()

# Удаление позиций
def remove_positionx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "DELETE FROM storage_position WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()
        db.execute('VACUUM')
        db.commit()


# Добавление категории в БД
def add_itemx(category_id, position_id, get_all_items, user_id, user_name):
    with sqlite3.connect(path_to_db) as db:
        try:
            for item_data in get_all_items:
                if not item_data.isspace() and item_data != "":
                    item_id = [random.randint(100000, 999999)]
                    year=None
                    zipka=None
                    if '|' in item_data:
                        zipka=[i for i in item_data.split('|') if i.strip().isdigit() and len(str(i.strip()))==5]
                        
                        if zipka !=[]:
                            zipka=zipka[0].strip()
                        else:
                            zipka=None
                        
                        year=[i for i in item_data.split('|') if '/' in i]
                        if year!=[]:
                            for j in year:
                                for i in j.split('/'):
                                    if (i.strip()[:2]=='19' or i.strip()[:2]=='20') and len(str(i).strip())==4:
                                        year=i.strip()
                                        break
                                    elif i.strip().isdigit() and int(i)>31 and len(i.strip())==2:
                                        year='19'+i.strip()
                                        break
                        else:
                            year=None
                        if year is not None and year.strip().isdigit():
                            pass
                        else: 
                            year=None
                        
                    db.execute("INSERT INTO storage_item "
                            "(item_id, item_data, position_id, category_id, creator_id, creator_name, add_date, zip, year) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            [item_id[0], item_data, position_id, category_id, user_id, user_name,
                                datetime.datetime.today().replace(microsecond=0), zipka, year])
            db.commit()
        except Exception as e:
            print(item_data)
            print(year)
            print(zipka)
            print(e)

# Изменение категории
def update_itemx(item_id, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_item SET XXX WHERE item_id = {item_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


# Получение категории
def get_itemx(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_item WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response


# Получение категорий
def get_itemsx(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_item WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response

def count_zip(zipka, year):
    with sqlite3.connect(path_to_db) as db:
        count = db.execute("SELECT COUNT() FROM storage_item where zip=? and year=?",[zipka,year]).fetchone()[0]
    return count

# Получение всех категорий
def get_all_itemsx():
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_item"
        get_response = db.execute(sql)
        get_response = get_response.fetchall()
    return get_response


# Очистка категорий
def clear_itemx():
    with sqlite3.connect(path_to_db) as db:
        sql = "DELETE FROM storage_item"
        db.execute(sql)
        db.commit()
        db.execute('VACUUM')
        db.commit()


# Удаление товаров
def remove_itemx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "DELETE FROM storage_item WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()
        db.execute('VACUUM')
        db.commit()

# Покупка товаров
def buy_itemx(get_items, get_count):
    with sqlite3.connect(path_to_db) as db:
        send_count = 0
        save_items = []
        for select_send_item in get_items:
            if send_count != get_count:
                send_count += 1
                save_items.append(f"{send_count}. <code>{select_send_item[2]}</code>")
                sql, parameters = get_format_args("DELETE FROM storage_item WHERE ", {"item_id": select_send_item[1]})
                db.execute(sql, parameters)
                split_len = len(f"{send_count}. <code>{select_send_item[2]}</code>")
                db.commit()
                db.execute('VACUUM')
                db.commit()
            else:
                break
        db.commit()
    return save_items, send_count, split_len


# Получение покупки
def get_purchasex(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_purchases WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response


# Получение покупок
def get_purchasesx(what_select, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"SELECT {what_select} FROM storage_purchases WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response


# Получение всех покупок
def get_all_purchasesx():
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_purchases"
        get_response = db.execute(sql)
        get_response = get_response.fetchall()
    return get_response

def add_purchasex(user_id, user_login, user_name, receipt, item_count, item_price, item_price_one_item,
                  item_position_id,
                  item_position_name, item_buy, balance_before, balance_after, buy_date, buy_date_unix):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_purchases "
                   "(user_id, user_login, user_name, receipt, item_count, item_price, item_price_one_item, item_position_id, "
                   "item_position_name, item_buy, balance_before, balance_after, buy_date, buy_date_unix) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   [user_id, user_login, user_name, receipt, item_count, item_price, item_price_one_item,
                    item_position_id, item_position_name, item_buy, balance_before, balance_after, buy_date,
                    buy_date_unix])
        db.commit()


def get_category_id(category):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_podcategory WHERE category_type = ?"
        get_response = db.execute(sql, [category])
        get_response = get_response.fetchall()
    return get_response


# Последние 10 покупок
def last_purchasesx(user_id):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_purchases WHERE user_id = ? ORDER BY increment DESC LIMIT 10"
        get_response = db.execute(sql, [user_id])
        get_response = get_response.fetchall()
    return get_response


# Создание всех таблиц для БД
def create_bdx():
    with sqlite3.connect(path_to_db) as db:
        # Создание БД с хранением данных пользователей
        check_sql = db.execute("PRAGMA table_info(storage_users)")
        check_sql = check_sql.fetchall()
        check_create_users = [c for c in check_sql]
        if len(check_create_users) == 8:
            print("DB was found(1/13)")
        else:
            db.execute("CREATE TABLE storage_users("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "user_id INTEGER, user_login TEXT, user_name TEXT, "
                       "balance TEXT, role INTEGER, reg_date TIMESTAMP, all_refill INTEGER)")
            print("DB was not found(1/13) | Creating...")

        # Создание БД с хранением данных платежных систем
        check_sql = db.execute("PRAGMA table_info(storage_payment)")
        check_sql = check_sql.fetchall()
        check_create_payment = [c for c in check_sql]
        if len(check_create_payment) == 6:
            print("DB was found(2/13)")
        else:
            db.execute("CREATE TABLE storage_payment("
                       "qiwi_login TEXT, qiwi_token TEXT, "
                       "qiwi_private_key TEXT, qiwi_nickname TEXT, "
                       "way_payment TEXT, status TEXT)")
            db.execute("INSERT INTO storage_payment("
                       "qiwi_login, qiwi_token, "
                       "qiwi_private_key, qiwi_nickname, "
                       "way_payment, status) "
                       "VALUES (?, ?, ?, ?, ?, ?)",
                       ["None", "None", "None", "None", "form", "False"])
            print("DB was not found(2/13) | Creating...")

        # Создание БД с хранением настроек
        check_sql = db.execute("PRAGMA table_info(storage_settings)")
        check_sql = check_sql.fetchall()
        check_create_settings = [c for c in check_sql]
        if len(check_create_settings) == 6:
            print("DB was found(3/13)")
        else:
            db.execute("CREATE TABLE storage_settings("
                       "contact INTEGER, faq TEXT, "
                       "status TEXT, status_buy TEXT,"
                       "profit_buy TEXT, profit_refill TEXT)")
            sql = "INSERT INTO storage_settings(" \
                  "contact, faq, status, status_buy, profit_buy, profit_refill) " \
                  "VALUES (?, ?, ?, ?, ?, ?)"
            now_unix = int(time.time())
            parameters = ("ℹ Контакты. Измените их в настройках бота.\n"
                          "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                          f"{bot_description}",
                          "ℹ Информация. Измените её в настройках бота.\n"
                          "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                          f"{bot_description}",
                          "True", "True", now_unix, now_unix)
            db.execute(sql, parameters)
            print("DB was not found(3/13) | Creating...")

        # Создание БД с хранением пополнений пользователей
        check_sql = db.execute("PRAGMA table_info(storage_refill)")
        check_sql = check_sql.fetchall()
        check_create_refill = [c for c in check_sql]
        if len(check_create_refill) == 10:
            print("DB was found(4/13)")
        else:
            db.execute("CREATE TABLE storage_refill("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "user_id INTEGER, user_login TEXT, "
                       "user_name TEXT, comment TEXT, "
                       "amount TEXT, receipt TEXT, "
                       "way_pay TEXT, dates TIMESTAMP, "
                       "dates_unix TEXT)")
            print("DB was not found(4/13) | Creating...")


        # Создание БД с хранением категорий
        check_sql = db.execute("PRAGMA table_info(storage_category)")
        check_sql = check_sql.fetchall()
        check_create_category = [c for c in check_sql]
        if len(check_create_category) == 5:
            print("DB was found(5/13)")
        else:
            db.execute("CREATE TABLE storage_category("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "category_id INTEGER, category_name TEXT, podcategory_id INTEGER, need_data TEXT)")
            print("DB was not found(5/13) | Creating...")


        check_sql = db.execute("PRAGMA table_info(storage_podcategory)")
        check_sql = check_sql.fetchall()
        check_create_category = [c for c in check_sql]
        if len(check_create_category) == 4:
            print("DB was found(6/13)")
        else:
            db.execute("CREATE TABLE storage_podcategory("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "category_id INTEGER, category_name TEXT, category_type TEXT)")
            print("DB was not found(6/13) | Creating...")

        # Создание БД с хранением позиций
        check_sql = db.execute("PRAGMA table_info(storage_position)")
        check_sql = check_sql.fetchall()
        check_create_position = [c for c in check_sql]
        if len(check_create_position) == 8:
            print("DB was found(7/13)")
        else:
            db.execute("CREATE TABLE storage_position("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "position_id INTEGER, position_name TEXT, "
                       "position_price INTEGER, position_discription TEXT,"
                       "position_image TEXT, position_date TIMESTAMP, "
                       "category_id INTEGER)")
            print("DB was not found(7/13) | Creating...")

        # Создание БД с хранением товаров
        check_sql = db.execute("PRAGMA table_info(storage_item)")
        check_sql = check_sql.fetchall()
        check_create_item = [c for c in check_sql]
        if len(check_create_item) == 10:
            print("DB was found(8/13)")
        else:
            db.execute("CREATE TABLE storage_item("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "item_id INTEGER, item_data TEXT, "
                       "position_id INTEGER, category_id INTEGER, "
                       "creator_id INTEGER, creator_name TEXT, "
                       "add_date TIMESTAMP,"
                       "zip INTEGER, year TEXT)")
            print("DB was not found(8/13) | Creating...")

        # Создание БД с хранением покупок
        check_sql = db.execute("PRAGMA table_info(storage_purchases)")
        check_sql = check_sql.fetchall()
        check_create_purchases = [c for c in check_sql]
        if len(check_create_purchases) == 15:
            print("DB was found(9/13)")
        else:
            db.execute("CREATE TABLE storage_purchases("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "user_id INTEGER, user_login TEXT, "
                       "user_name TEXT, receipt TEXT, "
                       "item_count INTEGER, item_price TEXT, "
                       "item_price_one_item TEXT, item_position_id INTEGER, "
                       "item_position_name TEXT, item_buy TEXT, "
                       "balance_before TEXT, balance_after TEXT, "
                       "buy_date TIMESTAMP, buy_date_unix TEXT)")
            print("DB was not found(9/13) | Creating...")
        db.commit()

        check_sql = db.execute("PRAGMA table_info(Language)")
        check_sql = check_sql.fetchall()
        check_create_purchases = [c for c in check_sql]
        if len(check_create_purchases) == 2:
            print("DB was found(10/13)")
        else:
            db.execute("CREATE TABLE Language("
                       "user_id INTEGER UNIQUE, lang TEXT)")
            print("DB was not found(10/13) | Creating...")
        db.commit()

        check_sql = db.execute("PRAGMA table_info(storage_data)")
        check_sql = check_sql.fetchall()
        check_create_purchases = [c for c in check_sql]
        if len(check_create_purchases) == 3:
            print("DB was found(10/13)")
        else:
            db.execute("CREATE TABLE storage_data("
                       "user_id INTEGER UNIQUE, position_id INT, data text)")
            print("DB was not found(10/13) | Creating...")
        db.commit()

        check_sql = db.execute("PRAGMA table_info(storage_check)")
        check_sql = check_sql.fetchall()
        check_create_purchases = [c for c in check_sql]
        if len(check_create_purchases) == 5: 
            print("DB was found(10/10)")
        else:
            db.execute("CREATE TABLE storage_check("
                       "user_id INTEGER UNIQUE, suma_btc TEXT, suma TEXT, curr TEXT, date TEXT)")
            print("DB was not found(11/11) | Creating...")
        db.commit()