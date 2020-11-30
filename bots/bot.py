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
			'volume': 5
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

	profit_logs = {}

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

		self.profit_logs = {}

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
		if not self.main_balance:
			return False

		if self.cur_price is not None and self.cur_price < trade_row['sell_price']:
			return False

		if trade_row['event_ts'] in self.sell_mins:
			if self.cur_price:
				return True
			
			if self.sell_mins[ trade_row['event_ts'] ]['length'] > self.buy_volumes[3]['from']:
				return True
		
		return False

	def _is_profit_event(self, trade_row):
		""" определение момента профита """
		if not self.sec_balance:
			return False

		if self.cur_price > trade_row['buy_price']:
			return False

		if self.cur_trend < 0:
			return True

		if self.prev_trend > self.cur_trend:
			return True

		return False

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

		self.main_balance -= self.ceil(trade_row['sell_price'] * buy_volume)
		
		if self.total_invest is None:
			self.total_invest = 0	
		self.total_invest += self.ceil( trade_row['sell_price'] * buy_volume, 2 )

		if self.sec_balance is None:
			self.sec_balance = 0	
		self.sec_balance += buy_volume

		self.cur_price = self.ceil(self.total_invest / self.sec_balance, 2)

		print( '{0} buy {1} @ {2} eq {3} cur price: {4}'.format( datetime.datetime.fromtimestamp(trade_row['event_ts']), buy_volume, trade_row['sell_price'], trade_row['sell_price'] * buy_volume, self.cur_price) )

	
	def _profit(self, trade_row):
		""" получение profit с sec_balance """
		if not self.main_balance:
			return False

		if self.prev_trend < self.cur_trend:
			return False

		print( 'At {0} accept {1} vs {2} invested. Sell price: {3}'.format( datetime.datetime.fromtimestamp(trade_row['event_ts']), trade_row['buy_price'] * self.sec_balance, self.total_invest, trade_row['buy_price'] ) )

		self.profit_logs[trade_row['event_ts']] = trade_row['buy_price']

		self.main_balance += self.ceil( trade_row['buy_price'] * self.sec_balance, 2)
		self.sec_balance = None
		self.cur_price = None
		self.total_invest = None

		print( 'main balance: {0}'.format(self.main_balance) )

	def set_main_balance(self, balance):
		self.main_balance = balance

	def get_total_balance(self, trade_row):
		""" Возвращает полный баланс бота для указанной даты """
		return self.main_balance + self.ceil( self.sec_balance * trade_row['buy_price'], 2 )
	
	def get_profit_events(self):
		return [datetime.datetime.fromtimestamp(event_ts) for event_ts in self.profit_logs.keys()], list( self.profit_logs.values() )

	def get_main_balance(self):
		return self.main_balance

	def get_sec_balance(self):
		return self.sec_balance

	def ceil(self, i, n=0):
		""" Отбрасываем дробную часть """ 
		return int(i * 10 ** n) / float(10 ** n)


	def test(self):
		return 'test'
