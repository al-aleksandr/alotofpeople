#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
from lxml.html.clean import Cleaner
import requests
import json
from io import StringIO
from bs4 import BeautifulSoup
from datetime import datetime

import global_settings
from common import print_all_event, get_html, convert_month_to_digit, convert_date, add_year_auto

url = 'https://www.google.com/search?client=ubuntu&channel=fs&q=%D0%B4%D0%B2%D0%BE%D1%80%D0%B5%D1%86+%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%B0+%D0%B0%D1%84%D0%B8%D1%88%D0%B0&ie=utf-8&oe=utf-8'
f_name = 'PalatsSportu_google_page.txt'
dt_last_update = datetime.today().replace(year=datetime.today().year - 1)

event_ending_name = ' (g)'

def get_events_google(html_file):
    event_list = []

    soup = BeautifulSoup(html_file, 'lxml')
    events_soup = soup.find_all('div', class_='h998We mlo-c')
    for event_div in events_soup:
        event_date = convert_month_to_digit(event_div.find('div', class_='aXUuyd').text[4:])
        event_date = add_year_auto(event_date)
        div_time = event_div.find('div', class_='HoEOQb')
        if div_time is None:
            event_time = '00:00'
        else:
            event_time = div_time.text
        event_title = event_div.find('div', class_='title').text
        event_title += event_ending_name
        dt = convert_date(event_date, event_time)

        event = {}
        event['title'] = event_title
        event['date'] = dt
        event_list.append(event)

    return sorted(event_list,
        key=lambda x: x['date'].strftime('%y/%m/%d %H:%M')
        )

def get_list():
    global url
    global f_name
    global dt_last_update

    print("PalatsSportu_goole is called")

    html_file = get_html(url, f_name, dt_last_update)
    dt_last_update = datetime.today()
    event_list = get_events_google(html_file)

    return event_list

if __name__ == '__main__':
    global_settings.init_settings()

    event_list = get_list()
    event_list = get_list()

    print_all_event(event_list)
