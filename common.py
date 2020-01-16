#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import locale
from datetime import datetime

def get_html_from_file(file_name=''):
    print("html form %s" %(file_name))

    if file_name == '':
        return None

    html_file = open(file_name).read()

    return html_file

def get_html_from_internet(url=''):
    print("html form Internet")
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    if url == '':
        return None

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        # 'Accept-Language': 'en-US,en;q=0.5',
        }
    page = requests.get(url, headers=headers, verify=False)
    html_file = page.text.encode('utf-8')

    return html_file

def save_to_file(file_name, str_to_save):
    text_file = open(file_name, "w")
    text_file.write(str_to_save)
    text_file.close()

def get_html(url, f_name, dt_last_update):
    if (datetime.today() - dt_last_update).days >= 1:
        html_file = get_html_from_internet(url)
        save_to_file(f_name, html_file)
    else:
        html_file = get_html_from_file(f_name)

    return html_file


def convert_month_to_digit(date_str):
    date_str = date_str.lower()

    date_str = date_str.replace(u"февр.", u"02")
    date_str = date_str.replace(u"мая",   u"05")
    date_str = date_str.replace(u"сент.", u"09")
    date_str = date_str.replace(u"нояб.", u"11")

    date_str = date_str.replace(u"січ.",  u"01")
    date_str = date_str.replace(u"лют.",  u"02")
    date_str = date_str.replace(u"бер.",  u"03")
    date_str = date_str.replace(u"квіт.", u"04")
    date_str = date_str.replace(u"трав.", u"05")
    date_str = date_str.replace(u"черв.", u"06")
    date_str = date_str.replace(u"лип.",  u"07")
    date_str = date_str.replace(u"серп.", u"08")
    date_str = date_str.replace(u"вер.",  u"09")
    date_str = date_str.replace(u"жовт.", u"10")
    date_str = date_str.replace(u"лист.", u"11")
    date_str = date_str.replace(u"груд.", u"12")

    date_str = date_str.replace(u"января",   u"01")
    date_str = date_str.replace(u"февраля",  u"02")
    date_str = date_str.replace(u"марта",    u"03")
    date_str = date_str.replace(u"апреля",   u"04")
    date_str = date_str.replace(u"мая",      u"05")
    date_str = date_str.replace(u"июня",     u"06")
    date_str = date_str.replace(u"июля",     u"07")
    date_str = date_str.replace(u"августа",  u"08")
    date_str = date_str.replace(u"сентября", u"09")
    date_str = date_str.replace(u"октября",  u"10")
    date_str = date_str.replace(u"ноября",   u"11")
    date_str = date_str.replace(u"декабря",  u"12")

    date_str = date_str.replace(u"январь",   u"01")
    date_str = date_str.replace(u"февраль",  u"02")
    date_str = date_str.replace(u"март",     u"03")
    date_str = date_str.replace(u"апрель",   u"04")
    date_str = date_str.replace(u"май",      u"05")
    date_str = date_str.replace(u"июнь",     u"06")
    date_str = date_str.replace(u"июль",     u"07")
    date_str = date_str.replace(u"август",   u"08")
    date_str = date_str.replace(u"сентябрь", u"09")
    date_str = date_str.replace(u"октябрь",  u"10")
    date_str = date_str.replace(u"ноябрь",   u"11")
    date_str = date_str.replace(u"декабрь",  u"12")

    return date_str

def print_all_event(event_list):
    for item in event_list:
        print('%70s: %s at %s' % (item['title'], item['date'].strftime("%d/%m/%Y"), item['date'].strftime("%H:%M")))

