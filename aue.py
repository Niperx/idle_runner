# -*- coding: utf-8 -*-
import vk_api
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime

import random
import math
import os.path
import json
import requests
from PIL import Image, ImageDraw, ImageFont

vk_session = vk_api.VkApi(token='93f1723b61b66da0a90236b27b0015ad7a57ad49c79d383db875ffbf77b91c058b3cd51b9d8ef8f0a6157')

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)


def send_user_reply(user, msg, reply='', attachment=''):
	vk_session.method('messages.send',
		{
		'user_id': user,
		'message': msg,
		'random_id': 0,
		'attachment': attachment,
		'reply_to': reply
		}
	)

def send_chat_reply(chat, msg, reply='', attachment=''):
	vk_session.method('messages.send',
		{
		'chat_id': chat,
		'message': msg,
		'random_id': 0,
		'attachment': attachment,
		'reply_to': reply
		}
	)


def get_user_name(user_id):
	user = session_api.users.get(user_ids=user_id)
	fullname = [user[0]['first_name'], user[0]['last_name']]
	return fullname

vk_groups = [-27456813, -156666557, -35927256]

def get_quot():
	grp = vk_groups[random.randint(0, 2)]
	print(grp)
	quot = session_api.wall.get(owner_id=grp, count=50, filter='owner', extended=1)
	quot_list = []
	while len(quot_list) < 25:
		for x in quot['items']:
			quot_list.append(x['text'])
		result = quot_list[random.randint(0, len(quot_list))]
	return result


def get_answer():

	info = get_quot()
	info = info.replace(', ',',\n')
	info = info.replace(' и ','\nи ')
	info = info.replace('. ','.\n')
	info = info.replace('... ','...\n')
	info = info.replace('" ','"\n')
	info = info.replace("' ","'\n")
	info = info.replace(' чем','\nчем')
	info = info.replace('то что','то\nчто')

	maxsize = (1028, 1028)
	img = Image.open('images/wolfs/wolf'+str(random.randint(1, 5))+'.jpg')
	img.thumbnail(maxsize, Image.ANTIALIAS)
	font = ImageFont.truetype('fonts/Bellota-Regular.ttf', size=42)
	draw_text = ImageDraw.Draw(img, "RGBA")
	w, h = draw_text.textsize(info, font)
	x, y = (img.width / 2 - (w/2), img.height / 2 - (h/2))
	
	draw_text.rectangle((x - 10, y - 10, x + w + 30, y + h + 20), fill=(0, 0, 0, 150))
	draw_text.rectangle((x - 10, y - 10, x + w + 30, y + h + 20), outline=(0, 0, 0, 127), width=2)
	draw_text.text(
		(x, y),
		info.title(),
		font=font,
		fill='#ffffff'
	)
	img.save('images/wolfs/wolf.jpg')
	# return photo_messages('user_ships/ship' + str(user_id))

	img = 'images/wolfs/wolf.jpg'
	url = session_api.photos.getMessagesUploadServer(peer_id=0)['upload_url']
	res = requests.post(url, files={'photo': open(img, 'rb')}).json()
	result = session_api.photos.saveMessagesPhoto(**res)[0]
	photo_name = "photo{}_{}".format(result["owner_id"], result["id"])
	print('Фото ID: '+ photo_name)
	return photo_name


# while True:
# 	try:
for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
		print('\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/')
		print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
		print('Текст сообщения: ' + str(event.text))
		print('ID пользователя: ' + str(event.user_id))
		print('===========================================')

		if event.from_chat and not (event.from_me):
			response = event.text.lower()
			text = ''
			fullname = get_user_name(event.user_id)
			print('Кто: '+fullname[0]+' '+fullname[1])
			print(event.message_id)

			if 'еблан' in response:
				send_chat_reply(event.chat_id, 'Сам такой', event.message_id)

			if 'ауф' in response:
				photo = get_answer()
				send_chat_reply(event.chat_id, '', event.message_id, photo)

		if event.from_user and not (event.from_me):
			response = event.text.lower()
			text = ''
			fullname = get_user_name(event.user_id)
			print('Кто: '+fullname[0]+' '+fullname[1])
			print(event.message_id)

			if 'еблан' in response:
				send_user_reply(event.user_id, 'Сам такой', event.message_id)

			if 'ауф' in response:
				photo = get_answer()
				send_user_reply(event.user_id, '', event.message_id, photo)


	# except requests.exceptions.ReadTimeout:
	# 	print("\n Переподключение к серверам ВК \n")
	# 	time.sleep(3)