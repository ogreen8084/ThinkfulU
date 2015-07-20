'''File 1 of 3. Pulls weather info from cities via the API
and converts to SQL database.
'''


import datetime
import requests
import pandas as pd
import json
import numpy as np
import sqlite3 as lite

#cities to pull weather information from 
cities = { 	"Jacksonville": '30.33695, -81.66145',
			"San_Francisco": '37.727239,-123.032229',
			"Las_Vegas": '36.229214,-115.26008',
			"New_Orleans": '30.053420,-89.934502',
			"Lincoln" : '40.81065, -96.68035'
		 }

#create dicionary of lists to hold temperature data for each city
holder = {}
for key1, val1 in cities.iteritems():
	holder[key1] = []

#get the date
start_date = datetime.datetime.now()

#while function to pull temperature for each city for the past 30 days
num_days = 0

#list for dates to create index for database table
date = []
api_key= #omitted

while num_days <=29:
	for key2, val2 in cities.iteritems():
		url = 'https://api.forecast.io/forecast/%s/%s,%s' %(api_key, \
		val2, start_date.strftime("%Y-%m-%dT%H:%M:%S"))
		r = requests.get(url)
		temp = []
		for item in r.json()['hourly']['data']:
			temp.append(item['temperature'])
		temp = np.asarray(temp) #read list as arraytype to easily get max value
		holder[key2].append(round(max(temp), 2))
		start_date = datetime.datetime.now()-datetime.timedelta(days=num_days) #change date
	date.append(start_date)
	num_days +=1

#create dataframe with city as columns, date as index
temperature_log = pd.DataFrame(holder, index =date)

#create weather database
con = lite.connect('weather.db')

#convert dataframe to sql table "temperature" via to_sql as type sqlite 
temperature_log.to_sql("temperature", con, 'sqlite')

con.close()

