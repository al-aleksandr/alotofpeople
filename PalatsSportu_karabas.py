#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
from lxml.html.clean import Cleaner
import json
from io import StringIO
from bs4 import BeautifulSoup
from datetime import datetime
from common import print_all_event, get_html, convert_month_to_digit

url = 'https://kiev.karabas.com/hall/dvorec-sporta/'
f_name = 'PalatsSportu_karabas_page.txt'
dt_last_update = datetime.today().replace(year=datetime.today().year - 1)

event_ending_name = ' (k)'

def convert_date(date_str, time_str):
    date_formats = '%d %m %Y'
    time_format = '%H:%M'

    # print(date_str)
    # dt2 = datetime(year=2020, month=2, day=1)
    # print dt2.strftime('We are the %s' %date_formats)

    dt = datetime.strptime(date_str.encode('utf-8').strip(), date_formats)

    tm = datetime.strptime(time_str.encode('utf-8').strip(), time_format)
    dt = dt.replace(hour=tm.hour, minute=tm.minute)
    # print(dt)
    return dt

def get_events_karabas(html_file):
    event_list = []

    soup = BeautifulSoup(html_file, 'html.parser')
    events_soup = soup.find_all('div', class_='ct-table-row ctr-body')
    # print(events_soup)
    for event_div in events_soup:
        # print(event_div)
        # return 
        date_str = event_div.find('ins', class_='ct-date').text[1:4] +\
                event_div.find('ins', class_='ct-date').span.text

        event_date = convert_month_to_digit(date_str.replace(',', ''))
        event_time = event_div.find_all('span', class_='ctr-cell')[1].find_all('ins')[2].text
        event_title = event_div.find_all('span', class_='ctr-cell')[1].find_all('span', class_='ctr-cell-link')[1].text.strip()
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
    event_list = get_list()
    event_list = get_list()

    print_all_event(event_list)
