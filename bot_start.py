# -*- coding: utf-8 -*-
import vk_api
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import math
import os.path
import json
import requests
from datetime import datetime
import time
import sqlite3
import threading
import random
from PIL import Image, ImageDraw, ImageFont
#pip install Pillow

from settings import *
from keyboards_list import *


vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)


# db_path = 'C://Users//kharo//Desktop//work//sakhproject_longpoll//db//'
# main_path = 'C://Users//kharo//Desktop//work//sakhproject_longpoll//'
# img_path = 'C://Users//kharo//Desktop//work//sakhproject_longpoll//images//'

settings_keyboard = dict(one_time=False, inline=False)

keyboard_ilde = VkKeyboard(**settings_keyboard)
keyboard_ilde.add_button(label='Ожидайте...', color=VkKeyboardColor.SECONDARY)


def create_keyboard(keys, sets=settings_keyboard):
	keyboard = VkKeyboard(**sets)
	if keys == {}:
		return keyboard.get_empty_keyboard()
		print('12')
	for key in keys:
		if isinstance(key, int) == False:
			keyboard.add_button(label=key, color=keys[key])
		elif isinstance(key, int) == True:
			keyboard.add_line()
	return keyboard.get_keyboard()

keyboards = {
	'empty' : create_keyboard(keyboard_empty),
	'idle' : create_keyboard(keyboard_idle),
	'main' : create_keyboard(keyboard_main),
	'sortie' : create_keyboard(keyboard_sortie)
}

keys_planet = {
	10 : keyboard_planets1,
	20 : keyboard_planets2
}

def send_message_to_user(user, msg, attachment=''):
	vk_session.method('messages.send',
		{
		'user_id': user,
		'message': msg,
		'random_id': 0,
		'attachment': attachment
		}
	)


def send_message_to_user_keyboard(user, msg, key_state, attachment=''):
	for place in keyboards:
		if key_state == place:
			key_state = keyboards[key_state]

	vk_session.method('messages.send',
		{
		'user_id': user,
		'message': msg,
		'keyboard': key_state,
		'random_id': 0,
		'attachment': attachment
		}
	)

def send_message_to_user_keys(user, msg, keys, attachment=''):
	vk_session.method('messages.send',
		{
		'user_id': user,
		'message': msg,
		'keyboard': keys,
		'random_id': 0,
		'attachment': attachment
		}
	)

def photo_messages(img):
	img = 'images/' + img + '.jpg'
	url = session_api.photos.getMessagesUploadServer(peer_id=0)['upload_url']
	res = requests.post(url, files={'photo': open(img, 'rb')}).json()
	result = session_api.photos.saveMessagesPhoto(**res)[0]
	photo_name = "photo{}_{}".format(result["owner_id"], result["id"])
	print('Фото ID: '+photo_name)
	return photo_name


def get_user_ship(user_id):
	fullname = get_user_name(user_id)
	fullname = fullname[0]+' '+fullname[1]
	img = Image.open('images/ship1.jpg')
	font = ImageFont.truetype('fonts/Pattaya-Regular.ttf', size=34)
	draw_text = ImageDraw.Draw(img)
	draw_text.text(
		(25, img.height - 60),
		fullname,
		font=font,
		fill='#ffffff'
	)
	img.save('images/user_ships/ship' + str(user_id) + '.jpg')
	# return photo_messages('user_ships/ship' + str(user_id))


def get_user_name(user_id):
	user = session_api.users.get(user_ids=user_id)
	fullname = [user[0]['first_name'], user[0]['last_name']]
	return fullname

def create_user(user_id, name, surname):
	user_info = (user_id, 1, 100, None, None, 1.0, datetime.now(), None)
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?);", user_info)
	conn.commit()
	get_user_ship(user_id)

def change_state(user_id, state, state_info, time):
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("UPDATE users SET state = ?, state_info = ?, end_time = ? WHERE user_id = ?", (state, state_info, time, user_id,))
	conn.commit()

def change_planet(user_id, planet):
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("UPDATE users SET planet = ? WHERE user_id = ?", (planet, user_id,))
	conn.commit()

def check_user(user_id):
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
	one_result = cur.fetchone()
	if one_result == None:
		return 0
	else:
		return 1

def check_status(user_id):
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("SELECT state, state_info, planet, end_time FROM users WHERE user_id = ?", (user_id,))
	one_result = cur.fetchone()
	return one_result

def create_travel(user_id, state_planet, where):
	state_on = 1
	state_off = None
	state_info = 'в полёте'
	timesl = abs(state_planet - where) * 15
	end_time = datetime.fromtimestamp(int(datetime.now().timestamp()) + timesl).strftime('%Y-%m-%d %H:%M:%S')


	change_state(event.user_id, state_on, state_info, end_time)

	time.sleep(timesl)

	change_state(event.user_id, None, None, None)
	change_planet(event.user_id, where)
	
	if where % 10 == 0:
		send_message_to_user_keyboard(event.user_id, 'Вы прилетели на местную станцию', 'main')
	else:
		send_message_to_user_keyboard(event.user_id, 'Вы прилетели к планете ' + planet[where][0], 'main')



# def create_db(): # Создание БД (одноразовая функция)
# 	conn = sqlite3.connect('db/main.db')
# 	cur = conn.cursor()
# 	cur.execute("""CREATE TABLE IF NOT EXISTS users(
# 	   user_id INT PRIMARY KEY,
# 	   level INT,
# 	   cash INT,
# 	   state INT,
# 	   state_info TEXT,
# 	   reg_time TEXT);
# 	""")
# 	conn.commit()

for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
		print('\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/')
		print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
		print('Текст сообщения: ' + str(event.text))
		print('ID пользователя: ' + str(event.user_id))
		print('===========================================')

		if event.from_user and not (event.from_me):
			response = event.text.lower()
			text = ''
			fullname = get_user_name(event.user_id)
			allow_to_bot = check_user(event.user_id)
			print('Кто: '+fullname[0]+' '+fullname[1])
			print('Доступ: '+str(allow_to_bot))

			if allow_to_bot == 1:
				status = check_status(event.user_id)
				state = status[0]
				state_info = status[1]
				state_planet = status[2]
				end_time = status[3]
				print('Занятость: '+str(state))

				if state == None:

					if state_info == 'выбор планеты': # СТАТУС ВЫБОРА ПЛАНЕТЫ
						planet = keys_planet[int(state_planet // 10 * 10)]
						for key in planet:
							if response == planet[key][0].lower():
								if state_planet != key:
									# Перелёт
									travel = threading.Thread(target=create_travel, args=(event.user_id, state_planet, key,))
									if key % 10 == 0:
										send_message_to_user_keyboard(event.user_id, 'Вылетаем на станцию...', 'idle')
									else:
										send_message_to_user_keyboard(event.user_id, 'Вылетаем на планету ' + planet[key][0] + '...', 'idle')
									travel.start()

					elif state_info == None: # НЕТ СТАТУСА

						if response == 'привет' or response == 'hello':
							x = int(datetime.now().timestamp())
							y = x + 600
							time_y = datetime.fromtimestamp(y).strftime('%Y-%m-%d %H:%M:%S')
							z = abs(x-y)

							hello_img = photo_messages('hello')
							send_message_to_user_keyboard(event.user_id, 'Hello', 'main', hello_img)

						elif response == 'корабль' or response == 'ship' or response == 'статус корабля':
							ship_img = photo_messages('user_ships/ship' + str(event.user_id))
							send_message_to_user_keyboard(event.user_id, 'Ваш корабль', 'main', ship_img)

						# elif response == 'покинуть планетную систему':
							# ТАК ЖЕ КАК И ПЛАНЕТЫ СО СТАТУСОМ

						elif response == 'сменить планету':
							keyboard = VkKeyboard(**settings_keyboard)
							cur_planet = int(state_planet // 10 * 10)
							print(cur_planet)
							planet = keys_planet[cur_planet]
							x = 0
							for key in planet:
								if x != 0 and x % 3 == 0:
									keyboard.add_line()
								if key != state_planet:
									keyboard.add_button(label=planet[key][0], color=planet[key][1])
								x += 1
							keyboard.add_line()
							keyboard.add_button(label='Назад', color=VkKeyboardColor.SECONDARY)
							keys = keyboard.get_keyboard()
							change_state(event.user_id, None, 'выбор планеты', None) # СТАТУС ВО ВРЕМЯ СМЕНЫ ПЛАНЕТЫ
							send_message_to_user_keys(event.user_id, 'Выберите планету:', keys)


						elif response == 'вылазка':
							send_message_to_user_keyboard(event.user_id, 'Выберите вашу цель визита на планету:', 'sortie')

					if response == 'назад':
						change_state(event.user_id, None, None, None)
						send_message_to_user_keyboard(event.user_id, 'Вы вернулись в панель управления кораблём:', 'main')

				elif state == 1:

					if response == 'ожидайте...':

						x = int(datetime.now().timestamp())
						y = datetime.fromisoformat(end_time).timestamp()
						z = int(abs(x-y))
						send_message_to_user_keyboard(event.user_id, 'До окончания полёта осталось: ' + str(z) 	+ ' секунд.', 'idle')



				# 	if response == 'отмена':


			elif allow_to_bot == 0:
				if response == 'начать' or response == 'start':
					create_user(event.user_id, fullname[0], fullname[1])
					send_message_to_user_keyboard(event.user_id, 'Добро пожаловать на ваш космический корабль, '+ fullname[0] + ' ' + fullname[1] +'!', 'main')

		print('/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ \n \n \n')