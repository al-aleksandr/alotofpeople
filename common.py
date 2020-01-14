#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests

def get_html_from_file(file_name=''):
    print("html form %s" %(file_name))

    if file_name == '':
        return None

    html_file = open(file_name).read()

    return html_file

def get_html_from_internet(url=''):
    print("html form Internet")

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

def print_all_event(event_list):
    for item in event_list:
        print('%70s: %s at %s' % (item['title'], item['date'].strftime("%d/%m/%Y"), item['date'].strftime("%H:%M")))

