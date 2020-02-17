# -*- coding: utf-8 -*-

# https://habr.com/ru/post/442800/

import telebot
import sys
import my_token
from telebot import types
import alop_main
from datetime import datetime, timedelta
import locale
from common import get_date_today

my_bot = telebot.TeleBot(my_token.token)

def get_event_by_date(dt):
    # for item in event_list:
    pass

def send_events_old(message, event_list, count=10):
    day = get_date_today()
    end_day = day + timedelta(days=count)
    # while day < end_day:
    #     day += timedelta(days=1)
    #     get_event_by_date(day)
    date_now = get_date_today()
    for item in event_list:
        if date_now > item['date']:
            continue
        resp = u'%s, %s:\n%s' % (item['date'].strftime("%a %d/%m").decode('utf-8'), item['date'].strftime("%H:%M"), item['title'])
        print(resp)
        my_bot.send_message(message.from_user.id, resp)
        count -= 1
        if count == 0:
            return

def send_events(message, count):
    ev_all = alop_main.get_upcomming_events(count)
    resp = u'\n'.join(ev_all)
    my_bot.send_message(message.from_user.id, resp)

def GetCountToResp(s):
    try: 
        int(s)
        return int(s)
    except ValueError:
        return 7

@my_bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message.text)
    # event_list = alop_main.get_list()
    # send_events(message, event_list, count=GetCountToResp(message.text))
    send_events(message, count=GetCountToResp(message.text))

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

reload(sys)
sys.setdefaultencoding('utf-8')

print('--------------------------- %s ---------------------------' % datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
my_bot.polling(none_stop=True, interval=0)
