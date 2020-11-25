#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль торгового модуля """

import datetime
import statistics

class Bot:
	""" Класс стандартного торгового алгоритма, что сейчас (2020.11.20) используется в сбере
	Закупается на минимумах, согласно таблице.
	Момент выхода в профит определсяет по скользящей средней. """

	SID = 24 * 3600

	buy_volumes = [
		{
			'from': 365 * 2 * SID,
			'to': 365 * SID,
			'label': 'year',
			'volume': 200
		},
		{
			'from': 365 * SID,
			'to': 180 * SID,
			'label': 'half year',
			'volume': 100
		},
		{
			'from': 180 * SID,
			'to': 90 * SID,
			'label': 'quart year',
			'volume': 20
		},
		{
			'from': 90 * SID,
			'to': 30 * SID,
			'label': 'month',
			'volume': 10
		},
		{
			'from': 30 * SID,
			'to': 14 * SID,
			'label': 'two weeks',
			'volume': 4
		},
		{
			'from': 14 * SID,
			'to': 7 * SID,
			'label': 'week',
			'volume': 2
		}
	]

	raw_trades = None
	sell_mins = None
	mid_trends = None
	
	main_balance = None
	sec_balance = None
	cur_price = None
	total_invest = None

	cur_trend = None
	prev_trend = None

	def __init__(self, raw_trades):
		""" Внесение данных о торгах и инициализация объекта """
		self.raw_trades = raw_trades

	def set_params(self, sell_mins=None, mid_trends=None):
		""" устанавливаем статистические значения """
		self.sell_mins = sell_mins
		self.mid_trends = mid_trends

	def run(self, from_dt = None, to_dt = None):
		""" генерация событий бота """
		if self.raw_trades is None:
			return

		if not isinstance(from_dt, datetime.datetime):
			return
		
		if not isinstance(to_dt, datetime.datetime):
			return

		for row in self.raw_trades:
			if row['event_ts'] in self.mid_trends:
				self.cur_trend = self.mid_trends[row['event_ts']]
			
			if row['event_ts'] < from_dt.timestamp() or row['event_ts'] > to_dt.timestamp():
				continue # skip out of date event
			
			if self._is_invest_event(row):
				self._invest(row)
			
			if self._is_profit_event(row):
				self._profit(row)
			
			self.prev_trend = self.cur_trend

	def _is_invest_event(self, trade_row):
		""" определение момента инвестиции """
		if self.main_balance is None:
			return False

		if self.main_balance == 0:
			return False
		
		if self.cur_price is not None and self.cur_price > trade_row['sell_price']:
			return False

		if trade_row['event_ts'] in self.sell_mins:
			return True
		
		return False

	def _is_profit_event(self, trade_row):
		""" определение момента профита """
		if self.sec_balance is None:
			return False

		if self.sec_balance == 0:
			return False

		if self.cur_price is not None and self.cur_price < trade_row['buy_price']:
			return False

		return True

	def _invest(self, trade_row):
		""" инвестирование средств с main_balance в sec_balance """
		if not self.main_balance:
			return False

		if trade_row['event_ts'] not in self.sell_mins:
			return False

		buy_volume = None
		for template_volume in self.buy_volumes:
			if self.sell_mins[ trade_row['event_ts'] ]['length'] < template_volume['from'] and self.sell_mins[ trade_row['event_ts'] ]['length'] > template_volume['to']:
				buy_volume = template_volume['volume']
				break

		if buy_volume is None:
			return False

		buy_volume = min( self.ceil(self.main_balance / trade_row['sell_price'], 2 ), buy_volume )

		self.main_balance -= trade_row['sell_price'] * buy_volume
		self.sec_balance += buy_volume

		print( '{0} buy {1} @ {2} eq {3}'.format( datetime.datetime.fromtimestamp(trade_row['event_ts']), buy_volume, trade_row['sell_price'], trade_row['sell_price'] * buy_volume ) )

	
	def _profit(self, trade_row):
		""" получение profit с sec_balance """
		raise Exception('Данная функция не реализована')

	def set_main_balance(self, balance):
		self.main_balance = balance

	def get_total_balance(self):
		return self.main_balance + self.sec_balance
	
	def get_main_balance(self):
		return self.main_balance

	def get_sec_balance(self):
		return self.sec_balance

	def ceil(self, i, n=0):
		""" Отбрасываем дробную часть """ 
		return int(i * 10 ** n) / float(10 ** n)


	def test(self):
		return 'test'
