#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

import PalatsSportu_main
import OlympicStadium_google
import global_settings
from common import print_all_event, get_date_today

def get_list():
    PS_list = PalatsSportu_main.get_list()
    OS_list = OlympicStadium_google.get_list()
    return PS_list

def get_db():
    PS_list = PalatsSportu_main.get_list()
    OS_list = OlympicStadium_google.get_list()
    db = []
    db.append({"place" : "Дворец Спорта", "ev_list" : PS_list})
    db.append({"place" : "Олимпийский Стадион", "ev_list" : OS_list})
    return db

def get_event_by_date(dt, db):
    dt_next = dt + timedelta(days=1)
    ret = []
    for item in db["ev_list"]:
        if (item['date'] >= dt) and (item['date'] < dt_next):
            event = u'%s, %s:\n%s' % (item['date'].strftime("%H:%M"), db["place"], item['title'])
            ret.append(event)

    return ret

def get_upcomming_events(count_days=7):
    ev_db = get_db()

    day = get_date_today()
    end_day = day + timedelta(days=count_days)
    event_list = []
    no_event = True

    day_list = []
    for db in ev_db:
        day_ev = get_event_by_date(day, db)
        if day_ev != []:
            day_list.extend(day_ev)

    event_list.append(day.strftime(u'----------------- %a %d/%m (Сегодня) -'))
    if day_list != []:
        event_list.extend(day_list)
        no_event = 0
    else:
        event_list.append(u'Нет событий\n')

    day += timedelta(days=1)

    while day < end_day:
        day_list = []
        for db in ev_db:
            day_ev = get_event_by_date(day, db)
            if day_ev != []:
                day_list.extend(day_ev)

        if day_list != []:
            event_list.append(day.strftime(u'----------------- %a %d/%m -----------------'))
            event_list.extend(day_list)
            no_event = 0

        day += timedelta(days=1)

    if no_event:
        return [u'Нет событий на ближайшие %d дн.' %(count_days)]

    return event_list

if __name__ == '__main__':
    global_settings.init_settings()

    print("alop_main")

    ev_db = get_db()
    for ev in ev_db:
        print("%s:" %(ev["place"]))
        print_all_event(ev["ev_list"])
        print

    ev_all = get_upcomming_events(20)
    for ev in ev_all:
        print(ev)
