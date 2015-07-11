import requests
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt 
from dateutil.parser import parse 
import sqlite3 as lite
import time
import collections

#create database and define cursor
con = lite.connect('citi_bike.db')
cur = con.cursor()

#pull citibike information to create initial database
r = requests.get('http://www.citibikenyc.com/stations/json')

key_list = [] # list of keys for each station
for station in r.json()['stationBeanList']:
    for k in station.keys():
        if k not in key_list:
            key_list.append(k)

#create dataframe from data in stationbeanlist
df = json_normalize(r.json()['stationBeanList'])

#create database and cursor to write directions
with con:
	cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')

sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

with con:
    for station in r.json()['stationBeanList']:
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

#set station id numbers are not valid for start of a variable
station_id = df['id'].tolist() 

station_id = ['_' + str(x) + ' INT' for x in station_id] 


#create table of available bikes
with con:
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_id) + ");")

#pull information from website once per minute and assign to database
for i in range(60):

	r = requests.get('http://www.citibikenyc.com/stations/json')

	exec_time = parse(r.json()['executionTime'])

	with con:
	    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))


	id_bikes = collections.defaultdict(int) 


	for station in r.json()['stationBeanList']:
	    id_bikes[station['id']] = station['availableBikes']


	with con:
	    for k, v in id_bikes.iteritems():
	        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")
	#counter to make sure iterations are working
	print 'iteration: %s' %(i+1)
	time.sleep(60)
con.close()

#create new database from information from website
df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time", con, index_col = 'execution_time')

hour_change = collections.defaultdict(int)

#iterate through columns (stations) and count total number of changes create a dictionary where the number
#of changes is the value and the name of the station is the key
for col in df.columns:
	station_vals = df[col].tolist()
	station_id = col[1:]
	station_change = 0
	for k, v in enumerate(station_vals):
		if k < len(station_vals)-1:
			station_change += abs(v- station_vals[k+1])

	hour_change[int(station_id)] = station_change

#function to find station with maximum number of changes, station is the key, value is number of changes
def keywithmaxval(d):
	v = list(d.values())
	k = list(d.keys())

	return k[v.index(max(v))]

max_station = keywithmaxval(hour_change)


print 'The station with the most changes is %d and the number of changes is %d' %(max_station, hour_change[max_station])

#plot to verify that 
plt.bar(hour_change.keys(), hour_change.values())
plt.show()

#Pull information about station with max number of changes from reference database
cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print "The most active station is station id %s at %s latitude: %s longitude: %s " % data
print "With " + str(hour_change[max_station]) + " bicycles coming and going in the hour between " + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')


