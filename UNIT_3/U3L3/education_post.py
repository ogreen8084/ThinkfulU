'''
Take two previously made DataFrames and extract needed data
then run regression to find relationship between GDP and education.
'''

import numpy as np
import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt
import statsmodels.api as sm

'''
The first step will be to pull the set the respective data to
dataframes and set each index to country in order to be able 
to match data from each DataFrame up by country.
'''

#transfer years of education data to DataFrame
education_df = pd.read_csv('school_education.csv')
education_df = education_df.set_index('Country or area', drop = True)

#connect to GDP database and create dataframe of gdp info
con = lite.connect('GDP_EDUCATION.db')
cur = con.cursor()

with con:
	cur.execute("PRAGMA table_info(gdp)")#get column names
	info = pd.DataFrame(cur.fetchall())
	cur.execute("SELECT * FROM gdp")
	gdp_df = pd.DataFrame(cur.fetchall())

gdp_df.columns = info[1] #assign column names to gdp DataFrame
gdp_df = gdp_df.set_index('country_name', drop = True)

#get rid of '_' in front of gdp year columns to enable search by date
new_cols =[]
for item in gdp_df.columns:
	new_cols.append(int(item[1:]))
gdp_df.columns = new_cols

'''
iterate through education DataFrame, by country. If there is a match between 
countries in both DataFrames add a list of the years of education for men, women
along with the applicable year and the gdp for that year. 
'''
get_info = {}
for item in education_df.index:
	if item in gdp_df.index:
		get_info[item]=list(
			[education_df.Year[item],education_df.Men[item], education_df.Women[item],
			gdp_df.ix[item][education_df.Year[item]]])

#create list of women and men years of education and the log of the gdp
gdp_list=[]
women_list = []
men_list = []
for k,v in get_info.iteritems():
	if v[3] != '':
		men_list.append(v[1])
		women_list.append(v[2])
		gdp_list.append(np.log(v[3]))
	else:
		pass

#convert lists of information to numpy arrays to run regression
x = np.array(gdp_list)
women1 = np.array(women_list)
men1 = np.array(men_list)

#fit data for women to regression line
fitwmn = np.polyfit(x,women1 , 1)
fit_wmn=np.poly1d(fitwmn)

#fit data for ment to regression line
fitmen = np.polyfit(x,men1, 1)
fit_men = np.poly1d(fitmen)

#plot women data
plt.figure(1)
plt.plot(x, women1, 'yo', x, fit_wmn(x), '--k')
plt.xlabel('LOG-GDP WOMEN')
plt.ylabel('EDUCATION IN YEARS')

#plot men data
plt.figure(2)
plt.plot(x, men1, 'yo', x, fit_men(x), '--k')
plt.xlabel('LOG-GDP MEN')
plt.ylabel('EDUCATION IN YEARS')
plt.show()


print 'There is a positive correlation between education and GDP levels.'

