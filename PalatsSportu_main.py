#! /usr/bin/env python
# -*- coding: utf-8 -*-

import global_settings
import PalatsSportu_google
import PalatsSportu_karabas
import PalatsSportu_ticketsbox
import PalatsSportu_concert
from common import print_all_event

def remove_same_event(ev_list):
	new_list = []
	new_list.append(ev_list[0])
	for ev in ev_list:
		if ev['date'] == new_list[-1]['date']:
			continue
		new_list.append(ev)
	return new_list

def get_list():
	print("PalatsSportu_main is called")
	PS_google_list = PalatsSportu_google.get_list()
	PS_karabas_list = PalatsSportu_karabas.get_list()
	PS_ticketsbox_list = PalatsSportu_ticketsbox.get_list()
	PS_concert_list = PalatsSportu_concert.get_list()
	
	PS_list = sorted(PS_ticketsbox_list + PS_karabas_list + PS_concert_list + PS_google_list,
        key=lambda x: x['date'].strftime('%y/%m/%d %H:%M')
        )

	return remove_same_event(PS_list)

if __name__ == '__main__':
    global_settings.init_settings()

	print("PalatsSportu_main")
