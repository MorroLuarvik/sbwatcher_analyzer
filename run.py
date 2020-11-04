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

start_date = datetime.datetime.strptime('2018.01.01', '%Y.%m.%d')
end_date = datetime.datetime.strptime('2019.12.30', '%Y.%m.%d')

query = """
SELECT buy_price, sell_price, event_ts 
FROM f_rates WHERE fin_id = 1 and event_ts BETWEEN {0} AND {1} ORDER BY event_ts;
""".format(start_date.timestamp(), end_date.timestamp())

cursor = connect.cursor(dictionary=True)
cursor.execute(query) 
rates = cursor.fetchall()

from analyzer import Analyzer
analyz = Analyzer(rates)


"""
from_uts = time.mktime( datetime.datetime.strptime('2020.3.1', '%Y.%m.%d').timetuple() )
to_uts = time.mktime( datetime.datetime.strptime('2020.3.20', '%Y.%m.%d').timetuple() )
from_idx = analyz._get_left_index(from_uts)
to_idx = analyz._get_left_index(to_uts)
sell_slice = [ item['sell_price'] for item in rates[from_idx:to_idx] ]
min_sell_val = min(sell_slice)
min_idx = from_idx + sell_slice.index(min_sell_val)
print( 'from: {0}, to: {1}: min sell price: {2} at {3}'.format(
	time.strftime( '%Y.%m.%d %H:%M:%S', time.localtime(from_uts) ), 
	time.strftime( '%Y.%m.%d %H:%M:%S', time.localtime(to_uts) ), 
	min_sell_val,
	time.strftime( '%Y.%m.%d %H:%M:%S', time.localtime(rates[min_idx]['event_ts']) )
) )
"""

plt.figure(figsize=(18, 6))
plt.subplots_adjust(left=0.05, right=0.95)

plt.plot( *analyz.get_sells() )
plt.plot( *analyz.get_buys() )

min0 = plt.scatter( *analyz.get_sell_mins(0), marker='x', zorder=10 )
min1 = plt.scatter( *analyz.get_sell_mins(1), zorder=10 )
min2 = plt.scatter( *analyz.get_sell_mins(2), zorder=10 )
min3 = plt.scatter( *analyz.get_sell_mins(3), zorder=10 )
min4 = plt.scatter( *analyz.get_sell_mins(4), zorder=10 )
min5 = plt.scatter( *analyz.get_sell_mins(5), zorder=10 )

plt.legend(
	(min0, min1, min2, min3, min4, min5),
	('year', 'half year', 'quart year', 'month', 'two week', 'week')
)

plt.show()

print('finish!')
