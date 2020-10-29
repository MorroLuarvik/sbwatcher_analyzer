#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль подготовки данных """

import datetime

class Analyzer():

    raw_info = None

    funcntion_list = {'f1': 'self.f1'}

    def set_data(self, raw_info):
        self.raw_info = raw_info

    

    def get_sells(self):
        if (not raw_info)
            raise Exception('Нет данных')
        
        return [datetime.datetime.fromtimestamp(item['event_ts']) for item in self.raw_info], [item['sell_price'] for item in self.rates]

    def get_buys(self):
        if (not raw_info)
            raise Exception('Нет данных')
        
        return [datetime.datetime.fromtimestamp(item['event_ts']) for item in self.raw_info], [item['buy_price'] for item in self.rates]
