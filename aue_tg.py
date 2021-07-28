from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from emoji import emojize

import random
import math
import os.path
import json
import requests
from PIL import Image, ImageDraw, ImageFont


import vk_api
from vk_api.upload import VkUpload

vk_session = vk_api.VkApi(token='93f1723b61b66da0a90236b27b0015ad7a57ad49c79d383db875ffbf77b91c058b3cd51b9d8ef8f0a6157')

session_api = vk_session.get_api()
upload = VkUpload(vk_session)

vk_groups = [-27456813, -156666557, -35927256]

def get_quot():
	err = True
	grp = vk_groups[random.randint(0, 2)]
	print(grp)
	quot = session_api.wall.get(owner_id=grp, count=50, filter='owner', extended=1)
	quot_list = []
	for x in quot['items']:
		quot_list.append(x['text'])
	
	while err == True:	
		try:
			result = quot_list[random.randint(1, len(quot_list))]
			if len(result) > 25 and 'http' not in result and 'подпис' not in result and 'vk.com' not in result and 'пригла' not in result:
				# print('\nПОДХОДИТ\n')
				err = False
		except IndexError:
			continue
	# print(f'Фраза: {result}')
	print(f'Список: {quot_list}')
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


bot = Bot(token='1813315511:AAHXpSNouWe98mBtIUm3wZPze9GhLPWUD4M')
dp = Dispatcher(bot)



# @dp.message_handler(text=['ауф'])
# async def process_start_command(message: types.Message):
#     await message.reply("Привет!\nАуф ёпта!")

# @dp.message_handler(commands=['photo'])

@dp.message_handler(text=['ауф'])
@dp.message_handler(commands=['auf'])
async def process_photo_command(message: types.Message):
    caption = 'Какие глазки! :eyes:'
    get_answer()
    imageFile = r"images/wolfs/wolf.jpg"
    img = open(imageFile, 'rb')
    await bot.send_photo(message.from_user.id, img, reply_to_message_id=message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp)