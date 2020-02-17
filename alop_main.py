#! /usr/bin/env python
# -*- coding: utf-8 -*-

import PalatsSportu_main
import OlympicStadium_google
from common import print_all_event, get_date_today
from datetime import timedelta

def get_list():
    PS_list = PalatsSportu_main.get_list()
    OS_list = OlympicStadium_google.get_list()
    return PS_list

def get_db():
    PS_list = PalatsSportu_main.get_list()
    OS_list = OlympicStadium_google.get_list()
    db = []
    db.append({"place" : "ДвСп", "ev_list" : PS_list})
    db.append({"place" : "ОлСт", "ev_list" : OS_list})
    return db

def get_event_by_date(dt, db):
    dt_next = dt + timedelta(days=1)
    ret = []
    # ret.append("%s:" % (db["place"]))
    for item in db["ev_list"]:
        if (item['date'] >= dt) and (item['date'] < dt_next):
            event = u'%s (%s):\n%s' % (item['date'].strftime("%H:%M"), db["place"], item['title'])
            ret.append(event)

    # if len(ret) == 1:
    #     return []

    return ret

def get_upcomming_events(count_days=7):
    ev_db = get_db()

    day = get_date_today()
    end_day = day + timedelta(days=count_days)
    event_list = []

    while day < end_day:
        day_list = []
        for db in ev_db:
            day_ev = get_event_by_date(day, db)
            if day_ev != []:
                day_list.extend(day_ev)

        if day_list != []:
            event_list.append(day.strftime("----------------- %a %d/%m -----------------").decode('utf-8'))
            event_list.extend(day_list)

        day += timedelta(days=1)

    return event_list

if __name__ == '__main__':
    print("alop_main")

    ev_db = get_db()
    
    for ev in ev_db:
        print("%s:" %(ev["place"]))
        print_all_event(ev["ev_list"])
        print

    ev_all = get_upcomming_events(20)
    for ev in ev_all:
        print(ev)
