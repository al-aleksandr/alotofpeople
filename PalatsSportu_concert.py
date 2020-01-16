#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
from lxml.html.clean import Cleaner
import json
from io import StringIO
from bs4 import BeautifulSoup
from datetime import datetime
from common import print_all_event, get_html, convert_month_to_digit

url = 'https://concert.ua/ru/search-result?query=%D0%B4%D0%B2%D0%BE%D1%80%D0%B5%D1%86+%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%B0'
f_name = 'PalatsSportu_concert_page.txt'
dt_last_update = datetime.today().replace(year=datetime.today().year - 1)

event_ending_name = ' (c)'

def convert_date(date_str, time_str):
    date_formats = '%d %m'
    time_format = '%H:%M'

    # print(date_str)
    # dt2 = datetime(year=2020, month=2, day=1)
    # print dt2.strftime('We are the %s' %date_formats)

    dt = datetime.strptime(date_str.encode('utf-8').strip(), date_formats)
    if dt.month >= datetime.today().month:
        dt = dt.replace(year=datetime.today().year)
    else:
        dt = dt.replace(year=datetime.today().year + 1)

    tm = datetime.strptime(time_str.encode('utf-8').strip(), time_format)
    dt = dt.replace(hour=tm.hour, minute=tm.minute)

    return dt

def get_events_concert(html_file):
    event_list = []

    soup = BeautifulSoup(html_file, 'lxml')
    events_soup = soup.find_all('a', class_='event')
    for event_div in events_soup:
        # print(event_div)
        # return

        event_ar = event_div.find('span', class_='event__date').text.strip()[0:-4]
        event_date = convert_month_to_digit(event_ar[0:-6])
        event_time = event_ar[-6:].strip()
        event_title = event_div.find('span', class_='event__name').text.strip()
        event_title += event_ending_name

        # print('\n\n\n')
        # print('event_date ---> %s' %(event_date))
        # print('event_time ---> %s' %(event_time))
        # print('event_title ---> %s' %(event_title))

        dt = convert_date(event_date, event_time)
        event = {}
        event['title'] = event_title
        event['date'] = dt
        event_list.append(event)
        # return event_list

    return sorted(event_list,
        key=lambda x: x['date'].strftime('%y/%m/%d %H:%M')
        )

def get_list():
    global url
    global f_name
    global dt_last_update

    print("PalatsSportu_concert is called")

    html_file = get_html(url, f_name, dt_last_update)
    dt_last_update = datetime.today()
    event_list = get_events_concert(html_file)

    return event_list

if __name__ == '__main__':
    event_list = get_list()
    event_list = get_list()

    print_all_event(event_list)
