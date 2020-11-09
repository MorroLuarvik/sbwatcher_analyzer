#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль подготовки данных """

"""
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
"""

import datetime

class Analyzer:

	DAY_LENGTH = 24 * 3600
	MIN_MIN_LENGTH = 7 * DAY_LENGTH

	raw_info = None
	min_values = {}

	def __init__(self, raw_info = None):
		""" Установка данных при инициализации класса """
		self.set_data(raw_info)

	def set_data(self, raw_info):
		""" Установка данных """
		self.raw_info = raw_info
		self._set_mins()
		self._clear_mins()

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

	def get_sell_mins(self, max_period = None, min_period = None):
		""" тестовая функция """

		if max_period is None:
			max_period = self.MIN_MIN_LENGTH * 2

		if min_period is None:
			min_period = self.MIN_MIN_LENGTH

		#print(self.min_values)

		slice_by_period = [self.min_values[idx] for idx in self.min_values if self.min_values[idx]['length'] <= max_period and self.min_values[idx]['length'] > min_period]
		
		#print( [item['sell_price'] for item in self.min_values if item['length'] <= max_period and item['length'] > min_period] ) 

		return [datetime.datetime.fromtimestamp(item['event_ts']) for item in slice_by_period], [item['sell_price'] for item in slice_by_period]

	def _clear_mins( self, value_types = ['sell_price'] ):
		""" удаление неактуальных минимальных значений без учёта послезнания """
		keys = list( self.min_values.keys() )
		keys.sort()

		for value_name in value_types:
			for cur in range( len(keys) - 1, 0, -1 ):
				cur_ts = keys[cur]
				prev_ts = keys[cur - 1]
				if self.min_values[prev_ts][value_name] <= self.min_values[cur_ts][value_name] and cur_ts - prev_ts < self.min_values[cur_ts]['length']:
					del(self.min_values[cur_ts])

	def _set_mins(self, from_idx = None, to_idx = None, prev_min_idx = None, value_type = 'sell_price'):
		""" заполняем self.min_values минимальными значениями """
		if from_idx is None:
			from_idx = 0

		if to_idx is None:
			to_idx = len(self.raw_info) - 1

		if abs(to_idx - from_idx) <= 1:
			return

		if abs(self.raw_info[to_idx]['event_ts'] - self.raw_info[from_idx]['event_ts']) < self.MIN_MIN_LENGTH:
			return

		values_by_type = [ item[value_type] for item in self.raw_info[from_idx:to_idx] ]
		min_idx = values_by_type.index( min(values_by_type) ) + from_idx
		

		need_add = False
		min_val = self.raw_info[min_idx][value_type]
		min_dt = datetime.datetime.fromtimestamp(self.raw_info[min_idx]['event_ts'])
		if prev_min_idx is None:
			print( 'First Value {0} at {1}'.format(min_val, min_dt) )
			need_add = True

		if not need_add and prev_min_idx > to_idx:
			print( 'Prev min in future Value {0} at {1}'.format(min_val, min_dt) )
			need_add = True

		if not need_add and self.raw_info[min_idx]['event_ts'] - self.raw_info[prev_min_idx]['event_ts'] > self.raw_info[to_idx]['event_ts'] - self.raw_info[from_idx]['event_ts']:
			print( 'Big range Value {0} at {1} ({2} > {3})'.format(min_val, min_dt, self.raw_info[min_idx]['event_ts'] - self.raw_info[prev_min_idx]['event_ts'], self.raw_info[to_idx]['event_ts'] - self.raw_info[from_idx]['event_ts']) )
			need_add = True

		need_add = True
		if need_add:
			self.min_values[ self.raw_info[min_idx]['event_ts'] ] = {
				value_type: self.raw_info[min_idx][value_type],
				'event_ts': self.raw_info[min_idx]['event_ts'],
				'length': self.raw_info[to_idx]['event_ts'] - self.raw_info[from_idx]['event_ts']
			}
		
		if min_idx - 1 > from_idx:
			self._set_mins(from_idx, min_idx - 1, min_idx)
		if min_idx + 1 < to_idx:
			self._set_mins(min_idx + 1, to_idx, min_idx)

	def _get_period_mins(self, priod, exclude_ts = set(), value_type = 'sell_price'):
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
			if item[value_type] < range_min and not (item['event_ts'] in exclude_ts):
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
