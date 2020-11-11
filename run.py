#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Отдельно закупаемый скрипт """

CONFIG_FILE_NAME = 'sbwatcher.json'
CONFIG_FOLDER_NAME = 'configs'

import os
import json
import datetime, time

from mysql import connector as connector

import matplotlib.pyplot as plt

dirName, _ = os.path.split(os.path.abspath(''))
config_file_path = dirName + os.path.sep + os.path.sep + CONFIG_FOLDER_NAME + os.path.sep + CONFIG_FILE_NAME

config_file = open(config_file_path, 'r+')
configs = json.load(config_file)
config_file.close()

connect = connector.connect(**configs['mysql'])

start_date = datetime.datetime.strptime('2019.1.1', '%Y.%m.%d')
end_date = datetime.datetime.strptime('2020.11.11', '%Y.%m.%d')
fin_id = 3 # 1 - usd, 2 - silver, 3 - pld

query = """
SELECT buy_price, sell_price, event_ts 
FROM f_rates WHERE fin_id = {2} and event_ts BETWEEN {0} AND {1} ORDER BY event_ts;
""".format(start_date.timestamp(), end_date.timestamp(), fin_id)

cursor = connect.cursor(dictionary=True)
cursor.execute(query) 
rates = cursor.fetchall()

start_time = time.time()
from analyzer import Analyzer
analyz = Analyzer(rates)
print( 'execution time: {0}'.format( time.time() - start_time ) )

#print(analyz.get_sell_mins(24 * 3600 * 365, 24 * 3600 * 180 ))

#exit()

plt.figure(figsize=(18, 6))
plt.subplots_adjust(left=0.05, right=0.95)

plt.plot( *analyz.get_sells() )
plt.plot( *analyz.get_buys() )

sid = 24 * 3600

min_periods = [
	{
		'from': 365 * 2 * sid,
		'to': 365 * sid,
		'label': 'year'
	},
	{
		'from': 365 * sid,
		'to': 180 * sid,
		'label': 'half year'
	},
	{
		'from': 180 * sid,
		'to': 90 * sid,
		'label': 'quart year'
	},
	{
		'from': 90 * sid,
		'to': 30 * sid,
		'label': 'month'
	},
	{
		'from': 30 * sid,
		'to': 14 * sid,
		'label': 'two weeks'
	},
	{
		'from': 14 * sid,
		'to': 7 * sid,
		'label': 'week'
	}
]

for period in min_periods:
	plt.scatter( *analyz.get_sell_mins(period['from'], period['to']), marker='x', zorder=10, label=period['label'] )

plt.legend()

"""
plt.legend(
	(min0, min1, min2, min3, min4, min5),
	('year', 'half year', 'quart year', 'month', 'two week', 'week')
)
"""

plt.show()

print('finish!')
