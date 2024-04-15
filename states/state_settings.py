# - *- coding: utf- 8 - *-
from aiogram.dispatcher.filters.state import State, StatesGroup


class StorageSettings(StatesGroup):
    here_contact = State()
    here_faq = State()


class Storage_map(StatesGroup):
    Storage_address = State()
    Storage_photo = State()
    Storage_link1 = State()
    Storage_link2 = State()
