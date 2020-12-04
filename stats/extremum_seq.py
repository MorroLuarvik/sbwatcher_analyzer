#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль очереди экстремальных значений """

class ExtremumSeq:
	""" Класс последовательности с отслеживанием экстремальных значений """

	length = None
	compare_function = None

	extrem_value = None
	exterm_ts = None

	sequence = []

	def __init__(self, length = None, is_extremum = None):
		""" инициализация задаётся:
		   отслеживаемая длина length в секундах
		   и функция определения экстремума f(new_val, old_val) - True - значение экстремальное"""
		if not type(length) in (int, float):
			raise Exception('Wrong type of length, must be int or float')
		
		self.length = length

		if not callable(is_extremum):
			raise Exception('compare_function, must be a function')

		self.is_extremum = is_extremum

	def add_value(self, value = None, ts = None):
		""" добавляет значение в очередь 
		и возврещает True, если значене окзалось экстремалным согласно функции is_extremum """
		
		if not type(value) in (int, float):
			raise Exception('Wrong type of length, must be int or float')

		if not type(ts) is int:
			raise Exception('Wrong type of length, must be int or float')

		ret = False
		if self.extrem_value is not None and ts - self.sequence[0]['event_ts'] >= self.length and self.is_extremum(value, self.extrem_value):
			self.extrem_value = value
			self.exterm_ts = ts
			ret = True

		self.sequence.append({'value': value, 'event_ts': ts})

		self.reduce_sequence()

		return ret

	def reduce_sequence(self):
		""" убираем значения с начала очереди, чтобы её длина <= self.length
		отслеживаем пропажу текущего экстремума """

		while len(self.sequence) > 0 and self.sequence[-1]['event_ts'] - self.sequence[0]['event_ts'] > self.length:
			removed_item = self.sequence.pop(0)
			if removed_item['event_ts'] == self.exterm_ts and removed_item['value'] == self.extrem_value:
				self.extrem_value = None
				self.exterm_ts = None


		if self.extrem_value is None:
			self.select_extremum()

	def select_extremum(self):
		""" определение экстремума в последовательности """
		
		self.extrem_value = self.sequence[0]['value']
		self.exterm_ts = self.sequence[0]['event_ts']

		for item in self.sequence[1:]:
			if self.is_extremum(item['value'], self.extrem_value):
				self.extrem_value = item['value']
				self.exterm_ts = item['event_ts']

