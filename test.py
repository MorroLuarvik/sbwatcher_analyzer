#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Тестовый скрипт """

from stats import ExtremumSeq
import random

raw_data = []

def min_func(new_val, old_val):
    return new_val < old_val

def max_func(new_val, old_val):
    return new_val > old_val

for idx in range(101):
    raw_data.append( {'ts': idx, 'value': round( random.random(), 2 ) } )

length =  10

seq10 = ExtremumSeq(length, min_func)

for row in raw_data:
    print( '{ts}: {value}'.format(**row), end='  \t')
    if seq10.add_value(row['value'], row['ts']):
        print('local min')
    else:
        print('odrinary val')

#print(raw_data)

print('finish')
