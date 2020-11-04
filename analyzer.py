#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль подготовки данных """

DAY_LENGTH = 24 * 3600
WEEK_LENGTH = 7 * DAY_LENGTH
TWO_WEEK_LENGTH = 14 * DAY_LENGTH
MONTH_LENGTH = 30 * DAY_LENGTH
QUART_YEAR_LENGTH = 90 * DAY_LENGTH
HALF_YEAR_LENGTH = 180 * DAY_LENGTH
YEAR_LENGTH = 365 * DAY_LENGTH

min_values = [
	{
		'alias': 'year',
		'length': YEAR_LENGTH,
		'datas' : {}
	},
	{
		'alias': 'half_year',
		'length': HALF_YEAR_LENGTH,
		'datas' : []
	},
	{
		'alias': 'quart_year',
		'length': QUART_YEAR_LENGTH,
		'datas' : []
	},
	{
		'alias': 'month',
		'length': MONTH_LENGTH,
		'datas' : []
	},
	{
		'alias': 'two_week',
		'length': TWO_WEEK_LENGTH,
		'datas' : []
	},
	{
		'alias': 'week',
		'length': WEEK_LENGTH,
		'datas' : []
	}
]

import datetime

class Analyzer:

	raw_info = None

	def __init__(self, raw_info = None):
		""" Установка данных при инициализации класса """
		self.set_data(raw_info)

	def set_data(self, raw_info):
		""" Установка данных """
		self.raw_info = raw_info
		self._set_mins()

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

	def get_sell_mins(self, idx = 0):
		""" тестовая функция """

		week_datas = min_values[idx]['datas'] #self._get_period_mins(MONTH_LENGTH)
		return [ datetime.datetime.fromtimestamp(uts) for uts in week_datas.keys() ], week_datas.values()

	def _set_mins(self):
		""" установка всех доступных минимумов """
		for idx, item in enumerate(min_values):
			print(idx)
			cur_mins = self._get_period_mins(item['length'])
			#copy_mins = cur_mins.copy()
			for subidx in range(idx):
				print('subrenga ', subidx)
				for event_ts in cur_mins.copy():
					if event_ts in min_values[subidx]['datas']:
						del(cur_mins[event_ts])
						#print('delete {0}'.format(event_ts))
			item['datas'] = cur_mins

		#print(min_values)


	def _get_period_mins(self, priod, value_type = 'sell_price'):
		""" получить словарь минимальных значение типа value_type
		за период priod секунд  
		{
			event_ts1: value1,
			event_ts2: value2
		}
		"""
		ret = {}

		first_idx = self._get_left_index(self.raw_info[0]['event_ts'] + priod)

		for cur_idx, item in enumerate(self.raw_info[first_idx:]):
			global_start_idx = self._get_left_index(self.raw_info[cur_idx]['event_ts'] - priod)
			global_end_idx = cur_idx + first_idx

			range_min = min( [item[value_type] for item in self.raw_info[global_start_idx:global_end_idx]])
			if item[value_type] <= range_min:
				ret[ item['event_ts'] ] = item[value_type]

		return ret


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
