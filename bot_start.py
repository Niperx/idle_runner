# -*- coding: utf-8 -*-
import vk_api
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import json
import requests
from datetime import datetime
import time
import sqlite3
import threading
import random

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
	'empty' : create_keyboard(keyboard_empty)
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
			keyboard = keyboards[key_state]

	vk_session.method('messages.send',
		{
		'user_id': user,
		'message': msg,
		'keyboard': keyboards[key_state],
		'random_id': 0,
		'attachment': photo_messages(attachment)
		}
	)


def photo_messages(img):
	photo = 'images/' + img + '.jpg'
	print('Фото ID: '+photo)
	url = session_api.photos.getMessagesUploadServer(peer_id=0)['upload_url']
	res = requests.post(url, files={'photo': open(img, 'rb')}).json()
	result = session_api.photos.saveMessagesPhoto(**res)[0]
	photo_name = "photo{}_{}".format(result["owner_id"], result["id"])
	print('Фото ID: '+photo_name)
	return photo_name


def get_user_name(user_id):
	user = session_api.users.get(user_ids=user_id)
	fullname = [user[0]['first_name'], user[0]['last_name']]
	return fullname


def create_user(user_id, name, surname):
	user_info = (user_id, 1, 100, 0, None, datetime.now())
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("INSERT INTO users VALUES(?,?,?,?,?,?);", user_info)
	conn.commit()

def change_state(user_id, state):
	conn = sqlite3.connect('db/main.db')
	cur = conn.cursor()
	cur.execute("UPDATE users SET state = ? WHERE user_id = ?", (state, user_id,))
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

				print("ACCESS")
				send_message_to_user_keyboard(event.user_id, 'Hello', 'empty', 'hello')






			elif allow_to_bot == 0:
				if response == 'начать' or response == 'start':
					create_user(event.user_id, fullname[0], fullname[1])
					send_message_to_user(event.user_id, 'Добро пожаловать на ваш космический корабль, '+ fullname[0] + ' ' + fullname[1] +'!')

		print('/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ \n \n \n')