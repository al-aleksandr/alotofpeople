#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

GetDataFromLocalFileOnly = False

def init_settings():
        global GetDataFromLocalFileOnly

        reload(sys)  
        sys.setdefaultencoding('utf-8')

        parser = argparse.ArgumentParser()
        parser.add_argument('-s', '--source', help='Source for data: local - data from local file; internet - data from internet or local file (default).', type=str, default='internet')

        source = parser.parse_args().source
        if source == 'local':
            GetDataFromLocalFileOnly = True
        else:
            GetDataFromLocalFileOnly = False
