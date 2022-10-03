# -*- coding: utf-8 -*-
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from aiogram.utils import executor
import aiogram.utils.markdown as md
from aiogram.dispatcher.filters import Text
from aiogram_calendar_rus import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar
import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import requests
from fuzzywuzzy import process
global selected_date
import pandas as pd
import numpy as np
from functools import reduce
from config import API_TOKEN
from aiogram.types import ParseMode
import re
from datetime import datetime
from logistic import model_compile
import pickle
import tensorflow as tf
import math
from math import sin
from dictionary import *
from datetime import timedelta
import asyncio

proxies = {
   'http': 'http://kerio.skno.by:3210',
   'https': 'https://kerio.skno.by:3210',
}

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN,proxy='http://kerio.skno.by:3210')
#bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()


#url = "https://raw.githubusercontent.com/avpakh/wta_prognoz/master/dataset.csv"
#response = requests.get(url,proxies=proxies)

dest = 'dataset.csv' # локальный
#with open(dest, 'wb') as file:
#    file.write(response.content)


df = pd.read_csv(dest,sep='^')
player_list1 = list(df['winner'].unique())
player_list2 = list(df['loser'].unique())
player_list = player_list1 + player_list2
player_list = set(player_list) # Список игроков

# cоздать словарь  Имя игрока - id
dict_winner = df.groupby(['winner','winner_id']).size().reset_index().to_dict('records')
dict_loser = df.groupby(['loser','loser_id']).size().reset_index().to_dict('records')
dict_player = {}
for el in dict_winner:
    dict_player.update({el.get('winner'):int(el.get('winner_id'))})
for el in dict_loser:
    dict_player.update({el.get('loser'):int(el.get('loser_id'))})

# Получить актуальный rank по игроку и количество набранных очков
#url = "https://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_rankings_current.csv"
#response = requests.get(url,proxies=proxies)

player_id = 'id_player.csv' # локальный
df_playerid = pd.read_csv(player_id,sep=',')
df_playerid['dob'] = pd.to_datetime(df_playerid['dob'].str.strip(), format='%Y-%m-%d')

data_player = df_playerid.to_dict('records')

dict_id_player = {}
for el in data_player:
    dict_id_player.update({el.get('player_id'):el.get('id')})  #

dict_player_id = {}
for el in data_player:
    dict_player_id.update({el.get('id'):el.get('player_id')})

dict_player_info = {}
for el in data_player:
    dict_player_info.update({el.get('player_id'):( el.get('hand'),el.get('dob'),el.get('height'))})

rank_csv = 'wta_rankings_current.csv' # локальный
#with open(dest, 'wb') as file:
#    file.write(response.content)
# Формирование актуального рейтинга
df_rank = pd.read_csv(rank_csv,sep=',')
df_rank['ranking_date'] = pd.to_datetime(df_rank['ranking_date'].astype(str), format='%Y%m%d')
max_date = df_rank['ranking_date'].max()
df_rank1 = df_rank.loc[(df_rank.ranking_date == max_date)]
array_rank = df_rank1.to_dict('records')

rank_dict = {}
for el in array_rank:
    id = el.get('player')
    print (id)
    rank_dict.update({dict_id_player.get(id):(int(el.get('rank')),int(el.get('points')))})

#history = model_compile()

my_tf_saved_model = tf.keras.models.load_model(
    'D:\\Projects\\Bots\\models\\my_tf_model')
my_tf_saved_model.summary()

'''
ynew = my_tf_saved_model.predict(t1)
# show the inputs and predicted outputs
for i in range(len(t1)):
    print("X=%s, Predicted=%s" % (t1[i], ynew[i]))
'''

# создаём форму и указываем поля
class Form(StatesGroup):
    date = State
    name1 = State()
    name2 = State()
    name3 = State()
    court = State()
    surface = State()
    round = State()
    calc = State()
    stop = State()

start_kb = ReplyKeyboardMarkup(resize_keyboard=True,)
start_kb.row('Выбор даты')

start_player = ReplyKeyboardMarkup(resize_keyboard=True,)
start_player.row('Игроки')

start_precourt = ReplyKeyboardMarkup(resize_keyboard=True,)
start_precourt.row('Выбор расположения корта')

start_court = ReplyKeyboardMarkup(resize_keyboard=True,)
start_court.row('Outdoor','Indoor')

start_presurface = ReplyKeyboardMarkup(resize_keyboard=True,)
start_presurface.row('Выбор покрытия корта')

start_surface = ReplyKeyboardMarkup(resize_keyboard=True,)
start_surface.row('Hard','Carpet','Clay','Grass','Greenset')

start_preround = ReplyKeyboardMarkup(resize_keyboard=True,)
start_preround.row('Выбор очередности встречи')

start_round = ReplyKeyboardMarkup(resize_keyboard=False,row_width=5)
start_round.row('1st Round','2nd Round','3rd Round','4th Round','Quarterfinals','Semifinals','The Final','Round Robin','Third Place')

start_gocalc = ReplyKeyboardMarkup(resize_keyboard=True,)
start_gocalc.row('Выполнить прогноз')

def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1

async def getbiorhythms(_dob, _match_day):
    pi = math.pi
    match_day = datetime.strptime(_match_day, '%d/%m/%Y')
    print (match_day)

    elapsed_days = match_day - _dob  # time delta
    print(elapsed_days)

    elapsed_days_float = elapsed_days.total_seconds()  # total seconds from query date
    elapsed_days_float /= 60  # seconds to minutes conversion
    elapsed_days_float /= 60  # minutes to hours conversion
    elapsed_days_float /= 24  # hours to days conversion

    try:

        physical = sin(2 * pi * (elapsed_days_float) / 23)
        emotional = sin(2 * pi * (elapsed_days_float) / 28)
        intellectual = sin(2 * pi * (elapsed_days_float) / 33)

        list_of_cycles = [(100 * physical) + 100, (100 * emotional) + 100, (100 * intellectual) + 100]

        return list_of_cycles

    except Exception as er3:
        print('Error in Biorhythms Formulas', str(er3))

async def get_dob(pla):
    id_player = dict_player.get(pla)
    print (id_player)
    player_id = dict_player_id.get(id_player)
    print (player_id)
    values = dict_player_info.get(player_id)
    print (values)
    dob = values[1]  # dob
    return dob

async def get_hand(pla):
    id_player = dict_player.get(pla)
    player_id = dict_player_id.get(id_player)
    values = dict_player_info.get(player_id)
    hand = values[0]  # hand
    return hand

async def get_dob(pla):
    id_player = dict_player.get(pla)
    print(id_player)
    player_id = dict_player_id.get(id_player)
    print(player_id)
    values = dict_player_info.get(player_id)
    print(values)
    dob = values[1]  # dob
    return dob

async def make_predictions(pla1, pla2, date_info, rank1, rank2):
    return 1

async def get_rank(_player):
    print (_player)
    id_player = dict_player.get(_player)
    print (id_player)
    datas = rank_dict.get(int(id_player))
    if datas == None:
        print (df_rank.info())
        player_id = dict_player_id.get(id_player)
        df_rank2 = df_rank.loc[(df_rank.player == player_id)]
        print (df_rank2)
        max_date = df_rank2['ranking_date'].max()
        df_rank3 = df_rank2.loc[(df_rank.ranking_date == max_date)]
        array_rank = df_rank3.to_dict('records')
        for el in array_rank:
            datas = (el.get('rank')),int(el.get('points'))
            return  datas
    return datas

# starting bot when user sends `/start` command, answering with inline calendar
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await message.reply('Ввод даты теннисного поединка: ', reply_markup=start_kb)


@dp.message_handler(Text(equals=['Oтмена'], ignore_case=True))
async def simple_cal_handler(message: Message):
    await message.answer('Действие отменено. Введите /start, чтобы начать заново.', reply_markup=await DialogCalendar().start_calendar())


@dp.message_handler(Text(equals=['Выбор даты'], ignore_case=True))
async def nav_cal_handler(message: Message):
    await message.answer('Ввод даты теннисного поединка:', reply_markup=await SimpleCalendar().start_calendar())

@dp.message_handler(Text(equals=['Игроки'], ignore_case=True))
async def first_player_input_handler(message: types.Message):
    await message.reply("Ввод фамилии первой теннисистки")
    await Form.name1.set()

# Сюда приходит ответ с именем
@dp.message_handler(state=Form.court)
async def process_court(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['court'] = message.text
    court = message.text
    await message.reply("Ввод места игры (на улице/ в помещении)", reply_markup=start_court)
    if court in ('Outdoor','Indoor'):
        await bot.send_message(message.from_user.id, text=f'Спасибо за ответ\n '
                                                          f' Выбран : {court}', reply_markup= start_presurface
                            )
        await state.set_state(Form.surface.state)
        print(data)



@dp.message_handler(state=Form.stop)
async def process_stop(message: types.Message, state: FSMContext):
    await message.reply('Продолжим ?. Ввод даты теннисного поединка: ', reply_markup=start_kb)
    await Form.stop.set()
    await Form.next()


# Сюда приходит ответ с именем
@dp.message_handler(state=Form.surface)
async def process_surface(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surface'] = message.text
    surface = message.text
    await message.reply("Ввод вида покрытия ", reply_markup=start_surface)
    if surface in ('Hard','Carpet','Clay','Grass','Greenset'):
        await bot.send_message(message.from_user.id, text=f'Спасибо за ответ\n '
                                                          f' Выбрано покрытие : {surface}', reply_markup= start_preround
                            )
        await state.set_state(Form.round.state)
        print(data)

# Сюда приходит ответ с именем
@dp.message_handler(state=Form.round)
async def process_round(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['round'] = message.text
    surface = message.text
    await message.reply("Ввод очередности матча на турнире ", reply_markup=start_round)
    if surface in ('1st Round','2nd Round','3rd Round','4th Round','Quarterfinals','Semifinals','The Final','Round Robin','Third Place'):
        await bot.send_message(message.from_user.id, text=f'Спасибо за ответ\n '
                                                          f' Выбран  : {surface}', reply_markup= start_gocalc
                            )
        await state.set_state(Form.calc.state)


# Сюда приходит ответ с именем
@dp.message_handler(state=Form.name1)
async def process_name1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name1'] = message.text
    name = message.text
    print(name)
    if name in player_list:
        await bot.send_message(message.from_user.id, text=f'Спасибо за ответ\n '
                                                      f' Фамилия первой теннисистки : {name}',reply_markup=start_player)

        await state.set_state(Form.name2.state)
    else:
        proposed_data = process.extract(name, list(player_list), limit=3)
        tt = str([el[0] for el in proposed_data if el[1] >= 75])
        if len(tt) !=0:
            await bot.send_message(message.from_user.id, text=f'Неполное соответствие ввода\n  {name}\n'
                                                          f'Возможные игроки: {tt}')
        else:
            await bot.send_message(message.from_user.id, text=f'В БД нет игроков по маске ввода \n  {name}\n')


@dp.message_handler(state=Form.calc)
async def process_calc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        reg_model = pickle.load(open("pickle_model.pkl", 'rb'))

        markup = types.ReplyKeyboardRemove()

        pla1 = data['name1']
        pla2 = data['name2']
        date_info = data['date']
        _court = data['court']
        _sufrace = data['surface']
        _round = data['round']

        rank1 = await get_rank(pla1)
        rank2 = await get_rank(pla2)

        dob1 = await get_dob(pla1)  # hand,date,height
        dob2 = await get_dob(pla2)

        hand1 = await get_hand(pla1)
        hand2 = await get_hand(pla2)

        bio1 = await getbiorhythms(dob1,date_info)
        bio2 = await getbiorhythms(dob2, date_info)

        diff_phi1 = bio1[0] - bio2[0]
        diff_emo1 = bio1[1] - bio2[1]
        diff_int1 = bio1[2] - bio2[2]

        diff_phi2 = bio2[0] - bio1[0]
        diff_emo2 = bio2[1] - bio1[1]
        diff_int2 = bio2[2] - bio1[2]

        court_value  = court.get(_court)
        surface_value = surface.get(_sufrace)
        round_value = round.get(_round)

        match_day = datetime.strptime(date_info, '%d/%m/%Y')
        age1 = (match_day - dob1)
        age2 = (match_day - dob2)

        age1 = age1/timedelta(days=1)
        age2 = age2/timedelta(days=1)

        diff_age1 = age1 - age2
        diff_age2 = age2 - age1

        comb1 = bio1[0]  + bio1[1] + bio1[2]
        comb2 = bio2[0]  + bio2[1] + bio2[2]

        diff1 = comb1 - comb2
        diff2 = comb2 - comb1

        diff_rank1 = rank1[0]- rank2[0]
        diff_rank2 = rank2[0]- rank1[0]

        tens_player1 = [rank1[0],rank1[1],bio1[0],bio1[1],bio1[2],diff_phi1,diff_emo1,diff_int1,diff_age1,comb1,age1,diff1,diff_rank1]
        tens_player2 = [rank2[0], rank2[1], bio2[0], bio2[1], bio2[2],
                        diff_phi2, diff_emo2, diff_int2, diff_age2, comb2, age2, diff2, diff_rank2]

        print(tens_player1)
        print(tens_player2)

        tens1 = tf.constant(tens_player1)
        tens2 = tf.constant(tens_player2)


        input_tensor1 = tf.reshape(tens1, shape=(1,13))
        input_tensor2 = tf.reshape(tens2, shape=(1,13))

        print(tens1)
        print(tens2)

        print(input_tensor1)
        print(input_tensor2)

        y1 = my_tf_saved_model.predict(input_tensor1)
        y2 = my_tf_saved_model.predict(input_tensor2)

        y1_log= reg_model.predict(input_tensor1)
        y2_log = reg_model.predict(input_tensor2)

        print (y1,y2)

        print (tens_player1)
        print (tens_player2)

        str_rank1 = 'рейтинг: ' + str(rank1[0]) + ' очки: ' + str(rank1[1])
        str_rank2 = 'рейтинг: ' + str(rank2[0]) + ' очки: ' + str(rank2[1])
        pla1 = str(pla1) + ' ('+ str_rank1 + ' )'
        pla2 = str(pla2) +' ('+ str_rank2 + ' )'

        await bot.send_message(
            message.chat.id,
            text=f'Исходные данные к прогнозу: \n'
                 f'Дата встречи:  {date_info} \n'
                 f'Рейтинги игроков на :  {max_date} \n'
                 f'Игрок 1: {pla1 } \n'
                 f'Игрок 2: {pla2} \n'
                 f'---------------------------\n'
                 f' Прогноз (нейронная сеть)\n'
                 f'Игрок 1: {y1[0]} \n'
                 f'Игрок 2: {y2[0]} \n'
                 f'---------------------------\n'
                 f' Прогноз (логистическая регрессия) \n'
                 f'Игрок 1: {y1_log} \n'
                 f'Игрок 2: {y2_log} \n'
            ,
            #reply_markup=markup
        )

        await state.set_state(Form.stop)

@dp.message_handler(state=Form.name2)
async def process_name2(message: types.Message, state: FSMContext):
    await message.reply("Ввод фамилии второй теннисистки")
    await Form.name2.set()
    await Form.next()


@dp.message_handler(state=Form.name3)
async def process_name1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name2'] = message.text
    name = message.text
    print(name)
    if name in player_list:
        await bot.send_message(message.from_user.id, text=f'Спасибо за ответ\n '
                                                      f' Фамилия второй теннисистки : {name}\n'
                                                      f' Cледующий шаг  - Выбор места игры:',reply_markup=start_precourt)
        print (data)
        await Form.next()
        await state.set_state(Form.court.state)
    else:
        proposed_data = process.extract(name, list(player_list), limit=3)
        tt = [el[0] for el in proposed_data if el[1] >= 75]
        if len(tt) != 0:

            await bot.send_message(message.from_user.id, text=f'Неполное соответствие ввода\n  {name}\n'
                                                      f'Возможные игроки: {tt}')
        else:
            await bot.send_message(message.from_user.id, text=f'В БД нет игроков по маске ввода \n  {name}\n')

@dp.message_handler(state=Form.court)
async def process_court(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['court'] = message.text
    name = message.text
    print(name)

# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict,state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        selected_date = date.strftime("%d/%m/%Y")
        await callback_query.message.answer(
            f'Ваш выбор:  {date.strftime("%d/%m/%Y") }\n'
            f'Следующий шаг - Выбор игроков',
            reply_markup=start_player,                  #
        )
        async with state.proxy() as data:
            data['date'] = selected_date


@dp.message_handler(Text(equals=['Режим диалога'], ignore_case=True))
async def simple_cal_handler(message: Message):
    await message.answer('Ввод даты теннисного поединка:', reply_markup=await DialogCalendar().start_calendar())

# dialog calendar usage
@dp.callback_query_handler(dialog_cal_callback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict,message: types.Message):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        selected_date = date.strftime("%d/%m/%Y")
        await callback_query.message.answer(
            f'Вы выбрали дату: {date.strftime("%d/%m/%Y")}',
            reply_markup=start_kb
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

