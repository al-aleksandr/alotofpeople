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

url = 'https://kiev.karabas.com/hall/dvorec-sporta/'
f_name = 'PalatsSportu_karabas_page.txt'
dt_last_update = datetime.today().replace(year=datetime.today().year - 1)

event_ending_name = ' (k)'

def get_events_karabas(html_file):
    event_list = []

    soup = BeautifulSoup(html_file, 'html.parser')
    events_soup = soup.find_all('div', class_='ct-table-row ctr-body')
    # print(events_soup)
    for event_div in events_soup:
        # print(event_div)
        date_str = event_div.find('ins', class_='ct-date').text[1:4].strip() + ' ' +\
                event_div.find('ins', class_='ct-date').span.text.strip()

        event_date = convert_month_to_digit(date_str.replace(',', ''))
        event_time = event_div.find_all('span', class_='ctr-cell')[1].find_all('ins')[2].text
        event_title = event_div.find_all('span', class_='ctr-cell')[1].find('a', class_='ctr-cell-link').text.strip()
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
    
    return sorted(event_list,
        key=lambda x: x['date'].strftime('%y/%m/%d %H:%M')
        )

def get_list():
    global url
    global f_name
    global dt_last_update

    print("PalatsSportu_karabas is called")

    html_file = get_html(url, f_name, dt_last_update)
    dt_last_update = datetime.today()
    event_list = get_events_karabas(html_file)

    return event_list

if __name__ == '__main__':
    global_settings.init_settings()

    event_list = get_list()
    event_list = get_list()

    print_all_event(event_list)
