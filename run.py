#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Отдельно закупаемый скрипт """

CONFIG_FILE_NAME = 'sbwatcher.json'
CONFIG_FOLDER_NAME = 'configs'

import os
import json
import datetime

import matplotlib.pyplot as plt

fig1_arr = (
	[-1, 0, 1, 0, -1],
	[0, 1, 0, -1, 0]
)

fig2_arr = (
	[-1, -1, 1, 1, -1],
	[-1, 1, 1, -1, -1]
)

plt.plot(*fig1_arr)
plt.plot(*fig2_arr)

plt.show()