#! /usr/bin/env python
# -*- coding: utf-8 -*-

import PalatsSportu_main
from common import print_all_event

def get_list():
	PS_list = PalatsSportu_main.get_list()
	return PS_list

if __name__ == '__main__':
	print("alop_main")
	
	PS_list = get_list()
	PS_list = get_list()
	print_all_event(PS_list)
