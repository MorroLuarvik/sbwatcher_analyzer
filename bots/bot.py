#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль торгового модуля """

import datetime
import statistics

class Bot:
	""" Класс стандартного торгового алгоритма, что сейчас (2020.11.20) используется в сбере
	Закупается на минимумах, согласно таблице.
	Момент выхода в профит определсяет по скользящей средней. """

	raw_trades = None
	main_balance = None
	sec_balance = None
	cur_price = None

	def __init__(self, raw_trades):
		""" Внесение данных о торгах и инициализация объекта """
		self.raw_trades = raw_trades

	def run(self, from_dt = None, to_dt =  None):
		""" генерация событий бота """
		if self.raw_trades is None:
			return

		if not isinstance(from_dt, datetime.datetime):
			return
		
		if not isinstance(to_dt, datetime.datetime):
			return

		for row in self.raw_trades:
			if row['event_ts'] >= from_dt.timestamp() and row['event_ts'] <= to_dt.timestamp():
				print(row)

	def set_main_balance(self, balance):
		self.main_balance = balance

	def get_total_balance(self, ts):
		return self.main_balance + self.sec_balance
	
	def get_main_balance(self):
		return self.main_balance

	def get_sec_balance(self):
		return self.sec_balance



	def test(self):
		return 'test'
