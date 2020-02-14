#! /usr/bin/env python
# -*- coding: utf-8 -*-

import PalatsSportu_main
import OlympicStadium_google
from common import print_all_event

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

if __name__ == '__main__':
	print("alop_main")
	
	ev_db = get_db()
	
	for ev in ev_db:
		print("%s:" %(ev["place"]))
		print_all_event(ev["ev_list"])
		print
