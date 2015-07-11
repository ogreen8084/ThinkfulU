'''
Convert database to pandas DataFrame and then to a csv
so that the files are more modular and can be utilized
by different databases.
'''

import numpy as np
import datetime
import pandas as pd
import sqlite3 as lite

#database file 
data = 'weather.db'


con = lite.connect(data)
cur = con.cursor()


with con:
	#get column names from table using PRAGMA
	cur.execute("PRAGMA table_info(temperature)")
	info = pd.DataFrame(cur.fetchall())
	#pull data from table and put it into a dataframe
	cur.execute("SELECT * FROM temperature")
	df =  pd.DataFrame(cur.fetchall())

#set dataframe column names and index
df.columns = info[1]	
df=df.set_index('index', drop=True)

#save dataframe to csv 
df.to_csv('weather.csv')