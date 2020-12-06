#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Отдельно закупаемый скрипт """

CONFIG_FILE_NAME = 'sbwatcher.json'
CONFIG_FOLDER_NAME = 'configs'

import os
import json
import datetime, time

from mysql import connector as connector

import matplotlib.dates
import matplotlib.pyplot as plt

dirName, _ = os.path.split(os.path.abspath(''))
config_file_path = dirName + os.path.sep + os.path.sep + CONFIG_FOLDER_NAME + os.path.sep + CONFIG_FILE_NAME

config_file = open(config_file_path, 'r+')
configs = json.load(config_file)
config_file.close()

connect = connector.connect(**configs['mysql'])

start_date = datetime.datetime.strptime('2017.1.1', '%Y.%m.%d')
end_date = datetime.datetime.strptime('2019.1.1', '%Y.%m.%d')
fin_id = 1 # 1 - usd, 2 - silver, 3 - pld
main_balance = 60000

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

analyz.generate_trends(7, 10)

"""
from bots import Bot

cur_bot = Bot(rates)
cur_bot.set_params(analyz.min_values, analyz.trends)
cur_bot.set_main_balance(main_balance)
cur_bot.run(start_date, end_date)"""

print( 'execution time: {0}'.format( time.time() - start_time ) )

#print(analyz.get_sell_mins(24 * 3600 * 365, 24 * 3600 * 180 ))

#exit()

fig = plt.figure(figsize=(18, 6))
#a1 = plt.subplot(211)
a1 = fig.add_subplot(111, label='trades')
#a1.subplots_adjust(left=0.05, right=0.95)

a1.plot( *analyz.get_sells() )
a1.plot( *analyz.get_buys() )

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

# =========== тестовое создание минимумов ===========
analyz._generate_mins(7 * sid)
analyz._generate_maxs(30 * sid)
# =========== тестовое создание минимумов ===========

for period in [min_periods[-1]]:
	a1.scatter( *analyz.get_sell_mins(period['from'], period['to']), marker='x', zorder=10, label=period['label'] )

a1.scatter( *analyz._get_sell_mins(), marker='o', zorder=10, label='another mins' )
a1.scatter( *analyz._get_buy_maxs(), marker='v', zorder=10, label='another maxs' )



"""
#a2 = plt.subplot(212)

#a2 = fig.add_subplot(111, label='trends', frame_on=False)
a2 = a1.twinx()

a2.xaxis.tick_top()
#a2.yaxis.set_visible(False) #a2.yaxis.tick_right()

a2.hlines(0, start_date, end_date )
a2.plot( *analyz.get_trends(), color="#00ffff", zorder=1 )

a1.scatter( *cur_bot.get_profit_events(), marker='^', zorder=20, label='Profit events' )"""

a1.legend()

plt.gca().fmt_xdata = matplotlib.dates.DateFormatter('%Y.%m.%d %H:%M')
plt.show()

print('finish!')
