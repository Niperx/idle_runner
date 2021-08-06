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
	for key in keys:
		if isinstance(key, int) == False:
			keyboard.add_button(label=key, color=keys[key])
		elif isinstance(key, int) == True:
			keyboard.add_line()
	return keyboard.get_keyboard()

keyboards = {
	'empty' : create_keyboard(keyboard_empty),
	'back' : create_keyboard(keyboard_back),
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
	print('Фото ID: '+ photo_name)
	return photo_name

def get_user_ship(user_id):
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("SELECT item_id, count FROM users_inventory WHERE owner_id = ? and slot = ?", (user_id, 2))
	items = cur.fetchall()
	cur.execute("SELECT item_id, count FROM users_inventory WHERE owner_id = ? and slot = ?", (user_id, 3))
	cur_items = len(cur.fetchall())
	cur.execute("SELECT level, cash, planet, ship_id FROM users WHERE user_id = ?", (user_id,))
	user = cur.fetchone()
	# if user[2] % 10 != 0:
	cur.execute("SELECT name FROM planets WHERE id = ?", (user[2],))
	planet = cur.fetchone()[0]
	# elif user[2] % 10 == 0:
	# 	planet = 'Станция'
	cur.execute("SELECT size_inventory_ship FROM users WHERE user_id = ?", (user_id,))
	max_ship_slots = cur.fetchone()[0] # Сколько места на корабле
	cur.execute("SELECT size_inventory_player FROM users WHERE user_id = ?", (user_id,))
	max_user_slots = cur.fetchone()[0]
	print(items)

	fullname = get_user_name(user_id)
	info = fullname[0]+' '+fullname[1]
	info += '\n' + 'Уровень: ' + str(user[0])
	info += '\n' + 'Кредиты: ' + str(user[1])
	info += '\n' + 'Локация: ' + str(planet)
	info += '\n' + 'Инвентарь (Корабль): [' + str(len(items)) + '/' + str(max_ship_slots) + ']'
	info += '\n' + 'Инвентарь (Персонаж): [' + str(cur_items) + '/' + str(max_user_slots) + ']'


	# if len(items) > 0:
	# 	for item in items:
	# 		item_info = check_item(item[0])
	# 		fullname += '\n' + item_info[1] + ' - ' + str(item[1])
	TINT_COLOR = (0, 0, 0)  # Black
	TRANSPARENCY = .25  # Degree of transparency, 0-100%
	OPACITY = int(255 * TRANSPARENCY)

	img = Image.open('images/ship'+str(user[3])+'.jpg')
	font = ImageFont.truetype('fonts/Bellota-Regular.ttf', size=28)
	draw_text = ImageDraw.Draw(img, "RGBA")
	x, y = (25, img.height / 2 + 30)
	w, h = draw_text.textsize(info, font)
	draw_text.rectangle((x - 5, y - 5, x + w + 5, y + h + 10), fill=(0, 0, 0, 75))
	draw_text.rectangle((x - 5, y - 5, x + w + 5, y + h + 10), outline=(0, 0, 0, 127), width=2)
	draw_text.text(
		(x, y),
		info,
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
	user_info = (user_id, 1, 100, None, None, 10, datetime.now(), None, 10, 50, random.randint(1, 3))
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?,?,?);", user_info)
	conn.commit()
	# get_user_ship(user_id)

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

def check_status_planet(planet):
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM planets WHERE id = ?", (planet,))
	one_result = cur.fetchone()
	return one_result

def check_item(item_id):
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM items WHERE id = ?", (item_id,))
	one_result = cur.fetchone()
	return one_result

def add_item(item_id, user_id, value=1, slot=3, active=None):
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("SELECT size_inventory_player FROM users WHERE user_id = ?", (user_id,))
	max_slots = cur.fetchone()[0]
	cur.execute("SELECT * FROM users_inventory WHERE owner_id = ? AND slot = ?", (user_id, slot,))
	slots = cur.fetchall()
	# for i in range(0, len(slots) - 1):
	for item in slots:
		if item[0] == item_id:
			cur.execute("SELECT count FROM users_inventory WHERE owner_id = ? AND item_id = ? AND slot = ?", (user_id, item_id, slot,))
			value += cur.fetchone()[0]
			cur.execute("UPDATE users_inventory SET count = ?, reg_time = ? WHERE owner_id = ? AND item_id = ? AND slot = ?", (value, datetime.now(), user_id, item_id, slot,))
			conn.commit()
			return print('Предмет добавлен в инвентарь и стакнут') 
	if len(slots) >= max_slots:
		return print('Недостаточно места в инвентаре') 
	if len(slots) < max_slots:
		item_info = (item_id, user_id, value, slot, active, datetime.now())
		cur = conn.cursor()
		cur.execute("INSERT INTO users_inventory VALUES(?,?,?,?,?,?);", item_info)
		conn.commit()
		return print('Предмет добавлен в инвентарь') 

def get_items(user_id, slot_from, slot_to):
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	if slot_to == 2:
		cur.execute("SELECT size_inventory_ship FROM users WHERE user_id = ?", (user_id,))
		max_slots = cur.fetchone()[0] # Сколько места на корабле
		cur.execute("SELECT * FROM users_inventory WHERE owner_id = ? AND slot = ?", (user_id, slot_from,))
		user_slots = cur.fetchall()

		if len(user_slots) >= 1:

			for slot in user_slots:
				cur.execute("SELECT * FROM users_inventory WHERE owner_id = ? AND slot = ? AND item_id = ?", (user_id, slot_to, slot[0],))
				current_ship_slot = cur.fetchone()
				if current_ship_slot == None or len(current_ship_slot) == 0:
					cur.execute("SELECT * FROM users_inventory WHERE owner_id = ? AND slot = ?", (user_id, slot_to,))
					ship_slots = cur.fetchall() 
					now_ship_slots = len(ship_slots) # Кол-во вещей на корабле
					if now_ship_slots < max_slots:
						cur.execute("UPDATE users_inventory SET slot = ?, reg_time = ? WHERE owner_id = ? AND item_id = ?", (slot_to, datetime.now(), user_id, slot[0],))
						conn.commit()
				elif len(current_ship_slot) != 0:
					value = current_ship_slot[2] + slot[2]
					cur.execute("UPDATE users_inventory SET count = ?, reg_time = ? WHERE owner_id = ? AND item_id = ? AND slot = ?", (value, datetime.now(), user_id, slot[0], slot_to,))
					conn.commit()
					cur.execute("DELETE FROM users_inventory WHERE item_id = ? AND owner_id = ? AND slot = ?", (slot[0], slot[1], slot[3],))
					conn.commit()
				
			return send_message_to_user(user_id, 'Вы перенесли предметы на корабль')
		else:
			return send_message_to_user(user_id, 'Инвентарь персонажа пуст')





def add_money(user_id, value):
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("SELECT cash FROM users WHERE user_id = ?", (user_id,))
	value += cur.fetchone()[0]
	cur.execute("UPDATE users SET cash = ? WHERE user_id = ?", (value, user_id,))
	conn.commit()
	return print('Кредиты зачислены на счёт') 

def create_travel(user_id, state_planet, where):
	state_on = 1
	state_off = None
	state_info = 'в полёте'
	timesl = abs(state_planet - where) * 15
	end_time = datetime.fromtimestamp(int(datetime.now().timestamp()) + timesl).strftime('%Y-%m-%d %H:%M:%S')


	change_state(user_id, state_on, state_info, end_time)

	time.sleep(timesl)

	change_state(user_id, None, None, None)
	change_planet(user_id, where)
	
	if where % 10 == 0:
		send_message_to_user_keyboard(user_id, 'Вы прилетели на местную станцию', 'main')
	else:
		send_message_to_user_keyboard(user_id, 'Вы подлетели к планете ' + planet[where][0], 'main')


def create_sortie(user_id, state_planet):
	state_on = 2 # Чек на продолжение экспидиции
	state_off = 3 # Чек на отмену экспидиции (Не нужная переменная, ибо он её берёт сам из профиля(БД) пользователя в строке 321 и 322, при нажатии кнопки "Отмена экспедиции")
	state_info = 'на планете' # Просто метка статуса у пользователя в профиле
	status_planet = check_status_planet(state_planet) # Проверка где пользователь на текущий момент
	change_state(user_id, state_on, state_info, None) # Меняем состояние пользователя на "В экспедиции"


	while state_on == 2:
		time.sleep(status_planet[2] + random.randint(-10, 10)) # Задаём время выполнения экспедиции: Время с планеты +- 10 сек(рандомно)

		status = check_status(user_id) # Берём статус у пользователя 
		state_on = status[0] # Переназначаем статус переменной выше

		situation = random.randint(1, 100) # Рандом ситуации, что пользователю выпадет (Руда, Хлам, Золото)
		print('Рандом: ' + str(situation)) # Инфа в консоль о том что выпало

		if situation <= 20: # Руда
			ore = check_item(status_planet[3]) # Берём ID руды с планеты
			text = 'Вы нашли жилу руды и добыли её \n' # Инфа в чат
			count = status_planet[4] + random.randint(-5, 5) # Кол-во руды: Кол-во прописанное в планете + рандом шт.
			text += 'Получено: ' + ore[1] + ' - ' + str(count) + ' шт. \n' # Инфа в чат
			if state_on == 2: # Если пользователь нажал "Отмена экспидиции" переводим его статус в другое состояние, чтобы закончить цикл с экспидицией
				text+= '\nПродолжаем путь...' # Инфа в чат
			add_item(ore[0], user_id, count, 3) # Функция на добавление предмета в инвентарь
			send_message_to_user(user_id, text) # Функция на вывод текста в чат

		elif situation > 30 and situation < 50 and status_planet[8] != None: # Хлам
			trash = check_item(random.choice(status_planet[8].split(','))) # Берём ID хлама с планеты
			text = 'Вы нашли немного хлама \n' # Инфа в чат
			text += 'Получено: ' + trash[1] # Инфа в чат
			if state_on == 2: # Если пользователь нажал "Отмена экспидиции" переводим его статус в другое состояние, чтобы закончить цикл с экспидицией
				text+= '\nПродолжаем путь...' # Инфа в чат
			add_item(trash[0], user_id, 1, 3) # Функция на добавление предмета в инвентарь
			send_message_to_user(user_id, text) # Функция на вывод текста в чат

		elif situation >= 80: # Исследование
			text = 'Вы нашли немного монет \n' # Инфа в чат
			count = status_planet[5] + random.randint(-20, 20) #
			text += 'Получено: Кредиты' + ' - ' + str(count) + ' шт.' # Инфа в чат
			if state_on == 2: # Если пользователь нажал "Отмена экспидиции" переводим его статус в другое состояние, чтобы закончить цикл с экспидицией
				text+= '\n\nПродолжаем путь...' # Инфа в чат
			add_money(user_id, count) # Функция на добавление валюты в профиль пользователя (Валюта не является предметом, у неё нет ID)
			send_message_to_user(user_id, text) # Функция на вывод текста в чат

		else: # Шанс ничего не найти, если рандом никуда не попал
			text = 'Вы ничего не нашли \n' # Инфа в чат
			if state_on == 2: # Если пользователь нажал "Отмена экспидиции" переводим его статус в другое состояние, чтобы закончить цикл с экспидицией
				text+= '\n\nПродолжаем путь...' # Инфа в чат
			send_message_to_user(user_id, text) # Функция на вывод текста в чат

		# if state_on == 2:
		# 	send_message_to_user(user_id, 'Продолжаем путь...')

	send_message_to_user_keyboard(user_id, 'Вы возвращаетесь к кораблю...', 'empty')
	change_state(user_id, 2, 'возвращение с планеты', None)
	time.sleep(10)
	change_state(user_id, None, None, None)
	send_message_to_user_keyboard(user_id, 'Вы вернулись обратно на орбиту', 'main')






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

while True:
	try:
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
						print('Статус: '+str(state_info))

						if state == None:

							if state_info == 'выбор системы': # СТАТУС ВЫБОРА СИСТЕМЫ
								cur_system = int(state_planet // 10 * 10)
								for key in keyboard_system:
									if response == keyboard_system[key][0].lower():
										if cur_system != key:
											# Перелёт
											travel = threading.Thread(target=create_travel, args=(event.user_id, state_planet, key,))
											send_message_to_user_keyboard(event.user_id, 'Вылетаем в систему ' + keyboard_system[key][0] + '...', 'idle')
											travel.start()

							elif state_info == 'выбор планеты': # СТАТУС ВЫБОРА ПЛАНЕТЫ
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

								if response == 'корабль' or response == 'ship' or response == 'статус корабля':
									get_user_ship(event.user_id)
									ship_img = photo_messages('user_ships/ship' + str(event.user_id))
									send_message_to_user_keyboard(event.user_id, 'Ваш корабль', 'main', ship_img)

								elif response == 'покинуть планетную систему': # ВЫБОР СИСТЕМЫ
									keyboard = VkKeyboard(**settings_keyboard)
									cur_system = int(state_planet // 10 * 10)
									x = 0
									for key in keyboard_system:
										if x != 0 and x % 3 == 0:
											keyboard.add_line()
										if key != cur_system:
											keyboard.add_button(label=keyboard_system[key][0], color=keyboard_system[key][1])
										x += 1
									keyboard.add_line()
									keyboard.add_button(label='Назад', color=VkKeyboardColor.SECONDARY)
									keys = keyboard.get_keyboard()
									change_state(event.user_id, None, 'выбор системы', None) # СТАТУС ВО ВРЕМЯ СМЕНЫ ПЛАНЕТЫ
									send_message_to_user_keys(event.user_id, 'Выберите систему:', keys)

								elif response == 'сменить планету': # ВЫБОР ПЛАНЕТЫ
									keyboard = VkKeyboard(**settings_keyboard)
									cur_system = int(state_planet // 10 * 10)
									print(cur_system)
									planet = keys_planet[cur_system]
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


								elif response == 'выгрузка инвентаря':
									get_items(event.user_id, 3, 2)


								elif response == 'вылазка':
									if state_planet % 10 == 0:
										send_message_to_user(event.user_id, 'Здесь нет возможности высадиться')
									elif state_planet % 10 != 0:
										sortie = threading.Thread(target=create_sortie, args=(event.user_id, state_planet,))
										send_message_to_user_keyboard(event.user_id, 'Вы вылетаете на планету и начинаете её исследование. \n (Следите за состоянием своего героя)', 'back')
										sortie.start()

							if response == 'назад':
								change_state(event.user_id, None, None, None)
								send_message_to_user_keyboard(event.user_id, 'Вы вернулись в панель управления кораблём:', 'main')

						elif state == 1:

							if response == 'ожидайте...':

								x = int(datetime.now().timestamp())
								y = datetime.fromisoformat(end_time).timestamp()
								z = int(abs(x-y))
								send_message_to_user_keyboard(event.user_id, 'До окончания полёта осталось: ' + str(z) 	+ ' секунд.', 'idle')

						elif state == 2:

							if response == 'вернуться':
								change_state(event.user_id, None, None, None)
								send_message_to_user(event.user_id, 'Подготовка к возрату')
								
								




						# 	if response == 'отмена':


					elif allow_to_bot == 0:
						if response == 'начать' or response == 'start':
							create_user(event.user_id, fullname[0], fullname[1])
							send_message_to_user_keyboard(event.user_id, 'Добро пожаловать на ваш космический корабль, '+ fullname[0] + ' ' + fullname[1] +'!', 'main')

				print('/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ \n \n \n')
				
	except requests.exceptions.ReadTimeout:
		print("\n Переподключение к серверам ВК \n")
		time.sleep(3)