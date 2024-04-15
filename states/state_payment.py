# - *- coding: utf- 8 - *-
from aiogram.dispatcher.filters.state import State, StatesGroup



class StoragePay(StatesGroup):
    here_input_suma=State()
    here_input_curr=State()
