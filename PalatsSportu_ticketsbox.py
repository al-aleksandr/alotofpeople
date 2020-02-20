#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
from lxml.html.clean import Cleaner
import json
from io import StringIO
from bs4 import BeautifulSoup
from datetime import datetime

import global_settings
from common import print_all_event, get_html, convert_month_to_digit, convert_date

url = 'https://ticketsbox.com/dvorets-sporta3/'
f_name = 'PalatsSportu_ticketsbox_page.txt'
dt_last_update = datetime.today().replace(year=datetime.today().year - 1)

event_ending_name = ' (t)'

def get_ev_date(elem):
    return elem['date']

def get_events_ticketbox(html_file):
    event_list = []

    soup = BeautifulSoup(html_file, 'lxml')
    events_soup = soup.find_all('div', class_='et-tour-row')
    for event_div in events_soup:
        event_ar = event_div.find_all('div', class_='et-tour-cell')

        event_date = convert_month_to_digit(event_ar[0].b.text[2:])
        event_time = event_ar[0].em.text
        event_title = event_ar[1].a.text
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

    print("PalatsSportu_ticketsbox is called")

    html_file = get_html(url, f_name, dt_last_update)
    dt_last_update = datetime.today()
    event_list = get_events_ticketbox(html_file)

    return event_list

if __name__ == '__main__':
    global_settings.init_settings()

    event_list = get_list()
    event_list = get_list()

    print_all_event(event_list)
