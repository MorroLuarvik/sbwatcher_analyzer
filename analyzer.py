#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль подготовки данных """

import datetime

class Analyzer:

	raw_info = None

	def __init__(self, raw_info = None):
		""" Установка данных при инициализации класса """
		self.set_data(raw_info)

	def set_data(self, raw_info):
		""" Установка данных """
		self.raw_info = raw_info

	def get_sells(self):
		""" данные о продажах """
		if (self.raw_info is None):
			raise Exception('Нет данных')
		
		return [datetime.datetime.fromtimestamp(item['event_ts']) for item in self.raw_info], [item['sell_price'] for item in self.raw_info]

	def get_buys(self):
		""" данные о покупках """
		if (self.raw_info is None):
			raise Exception('Нет данных')
		
		return [datetime.datetime.fromtimestamp(item['event_ts']) for item in self.raw_info], [item['buy_price'] for item in self.raw_info]

	def get_spreads(self):
		""" данные о разнице между покупкой и продажей """
		if (self.raw_info is None):
			raise Exception('Нет данных')
		
		rate_range = [datetime.datetime.fromtimestamp(item['event_ts']) for item in self.raw_info]
		spred_data = [item['sell_price'] - item['buy_price'] for item in self.raw_info]
		min_spred = min(spred_data)
		spred_data = spred_data + [min_spred] + [min_spred]

		return rate_range + [rate_range[-1]] + [rate_range[0]], spred_data

	def _get_from_index(self, date_time):
		""" получить индекс первого элемента большего чем date_time """
		return None

	def _get_to_index(self, date_time):
		""" получить индекс последнего элемента меньшего чем date_time """
		return None