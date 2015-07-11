#Importing to work with sqlite3 and pandas
import sqlite3 as lite
import pandas as pd

#Connect to database.
con = lite.connect('getting_started.db')

with con:
	cur = con.cursor()
	cur.executescript('DROP TABLE IF EXISTS weather')
	cur.executescript('DROP TABLE IF EXISTS cities')
	#create cities table and add rows
	cur.execute('CREATE TABLE cities (name text, state text)')
	cur.execute("INSERT INTO cities VALUES ('New York City', 'NY')")
	cur.execute("INSERT INTO cities VALUES ('Boston', 'MA')")
	cur.execute("INSERT INTO cities VALUES ('Chicago', 'IL')")
	cur.execute("INSERT INTO cities VALUES ('Miami', 'FL')")
	cur.execute("INSERT INTO cities VALUES ('Dallas', 'TX')")
	cur.execute("INSERT INTO cities VALUES ('Seattle', 'WA')")
	cur.execute("INSERT INTO cities VALUES ('Portland', 'OR')")
	cur.execute("INSERT INTO cities VALUES ('San Francisco', 'CA')")
	cur.execute("INSERT INTO cities VALUES ('Los Angeles', 'CA')")
	

	#create weather table and add rows
	cur.execute('CREATE TABLE weather (city, year, warm_month, cold_month, average_high)')
	cur.execute("INSERT INTO weather (city, year, warm_month, cold_month, average_high) VALUES ('New York City',2013,'July','January', 62)")
	cur.execute("INSERT INTO weather (city, year, warm_month, cold_month, average_high) VALUES ('Boston',2013,'July','January', 59)")
	cur.execute("INSERT INTO weather (city, year, warm_month, cold_month, average_high) VALUES ('Chicago',2013,'July','January', 59)")
	cur.execute("INSERT INTO weather (city, year, warm_month, cold_month, average_high) VALUES ('Miami',2013,'August','January', 84)")
	cur.execute("INSERT INTO weather (city, year, warm_month, cold_month, average_high) VALUES ('Dallas',2013,'July','January', 77)")
	cur.execute("INSERT INTO weather (city, year, warm_month, cold_month, average_high) VALUES ('Seattle',2013,'July','January', 61)")
	cur.execute("INSERT INTO weather (city, year, warm_month, cold_month, average_high) VALUES ('Portland',2013,'July','December', 63)")
	cur.execute("INSERT INTO weather (city, year, warm_month, cold_month, average_high) VALUES ('San Francisco',2013,'September','December', 64)")
	cur.execute("INSERT INTO weather (city, year, warm_month, cold_month, average_high) VALUES ('Los Angeles',2013,'September','December', 75)")

	#join tables 
	cur.execute("SELECT name, state, warm_month FROM cities INNER JOIN weather ON name = city ORDER BY warm_month")
	rows = cur.fetchall()

	df = pd.DataFrame(rows)

	iterator = 0
	month_group = dict();

	while iterator < len(df):
		if df[2][iterator] in month_group:
			month_group[df[2][iterator]]= month_group[df[2][iterator]]+', '+ df[0][iterator] +' ' + df[1][iterator];
		else:
			month_group[df[2][iterator]]= df[0][iterator] + ' ' + df[1][iterator];
		iterator +=1;
	print month_group;
	for key in month_group:
		print 'The cities that are the warmest in ' + key + ' are: ' + month_group[key]; 
