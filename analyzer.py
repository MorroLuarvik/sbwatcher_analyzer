#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль подготовки данных """

DAY_LENGTH = 24 * 3600
WEEK_LENGTH = 7 * DAY_LENGTH
TWO_WEEK_LENGTH = 14 * DAY_LENGTH
MONTH_WEEK_LENGTH = 30 * DAY_LENGTH

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

	def get_week_sell_mins(self):
		ret_dates = []
		ret_vals = []

		first_idx = self._get_left_index(self.raw_info[0]['event_ts'] + MONTH_WEEK_LENGTH)

		for cur_idx, item in enumerate(self.raw_info[first_idx:]):
			global_start_idx = self._get_left_index(self.raw_info[cur_idx]['event_ts'] - MONTH_WEEK_LENGTH)
			global_end_idx = cur_idx + first_idx

			range_min = min( [item['sell_price'] for item in self.raw_info[global_start_idx:global_end_idx]])
			if item['sell_price'] <= range_min:
				ret_dates.append( datetime.datetime.fromtimestamp(item['event_ts']) )
				ret_vals.append(item['sell_price'])

		return ret_dates, ret_vals


	def _get_left_index(self, date_time):
		""" получить индекс первого элемента большего чем date_time """
		left_idx = 0
		right_idx = len(self.raw_info) - 1
		
		if (self.raw_info[right_idx]['event_ts'] < date_time):
			return right_idx

		if (self.raw_info[left_idx]['event_ts'] > date_time):
			return left_idx

		if (date_time < self.raw_info[left_idx]['event_ts'] or date_time > self.raw_info[right_idx]['event_ts']):
			raise Exception('Запрашиваемая дата не в диапазоне')
		
		while right_idx - left_idx > 1:
			mid_idx = (left_idx + right_idx) // 2
			if (date_time > self.raw_info[mid_idx]['event_ts']):
				left_idx = mid_idx
			else:
				right_idx = mid_idx
		return left_idx
