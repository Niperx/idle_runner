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


vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)


# db_path = 'C://Users//kharo//Desktop//work//sakhproject_longpoll//db//'
# main_path = 'C://Users//kharo//Desktop//work//sakhproject_longpoll//'
# img_path = 'C://Users//kharo//Desktop//work//sakhproject_longpoll//images//'

settings_keyboard = dict(one_time=False, inline=False)



def send_message_to_user(user, msg, attachment=''):
    vk_session.method('messages.send',
        {
        'user_id': user,
        'message': msg,
        'random_id': 0,
        'attachment': attachment
        }
    )


def send_message_to_user_keyboard(user, msg, status_state, attachment=''):
    for place in keyboards:
        if status_state == place:
            keyboard = keyboards[place]

    vk_session.method('messages.send',
        {
        'user_id': user,
        'message': msg,
        'keyboard': keyboards[status_state],
        'random_id': 0,
        'attachment': attachment
        }
    )


def get_user_name(user_id):
    user = session_api.users.get(user_ids=user_id)
    fullname = [user[0]['first_name'], user[0]['last_name']]
    return fullname


