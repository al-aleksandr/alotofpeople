# -*- coding: utf-8 -*-

# https://habr.com/ru/post/442800/

import telebot
import my_token
from telebot import types
import alop_main
from datetime import datetime
import locale

my_bot = telebot.TeleBot(my_token.token)

def send_events(message, event_list, count=10000):
    for item in event_list:
    	date_now = datetime.now().replace(hour=0, minute=0, second=0)
    	if date_now > item['date']:
    		continue
    	resp = u'%s, %s:\n%s' % (item['date'].strftime("%a %d/%m").decode('utf-8'), item['date'].strftime("%H:%M"), item['title'])
    	print(resp)
        my_bot.send_message(message.from_user.id, resp)
        count -= 1
        if count == 0:
        	return

def GetCountEventsToResp(s):
    try: 
        int(s)
        return int(s)
    except ValueError:
        return 5

@my_bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message.text)
    event_list = alop_main.get_list()
    send_events(message, event_list, count=GetCountEventsToResp(message.text))

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
print('--------------------------- %s ---------------------------' % datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
my_bot.polling(none_stop=True, interval=0)
