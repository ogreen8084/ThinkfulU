'''
pulls data from website and converts table into dataframe.
saves dataframe to csv.

'''


from bs4 import BeautifulSoup
import requests
import unicodedata
import numpy as np
import pandas as pd

#url to pull school demographic data from
url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/\
	unsd/demographic/products/socind/education.htm"

r= requests.get(url)


soup = BeautifulSoup(r.content, "html.parser")
table = soup('table')[6]

#safe all 'tr' tagged data
rows = table.find_all('tr')

#iterate through 'tr' data to 
data = []
for row in rows:
	cols = row.find_all('td')
	cols = [ele.text.strip() for ele in cols]
	data.append([ele for ele in cols if ele])

#printed the data until I found only the relevant fields
#saving that data to a new list
new_data =  data[3][4:]

'''
cleaning data by getting rid of misc. letters
and converting to ascii
'''
new_data2 = []
alphabet = ['a','b','c','d','e','f','g','h']
for item in new_data:
	if item.encode('ascii', 'ignore') not in alphabet:
		new_data2.append(item.encode('ascii', 'ignore'))
	else:
		pass

#reshaping data and converting to dataframe
data_final = np.reshape(new_data2, (184, 5))
data_final2 = pd.DataFrame(data_final, columns = data_final[0])
data_final2 = data_final2[data_final2.index != 0]
data_final2 = data_final2.drop('Total', 1)

#converting columns to numpy arrays to get statistical info
women_data = np.asarray(data_final2['Women'], dtype = int)
men_data = np.asarray(data_final2['Men'], dtype = int)

print 'The mean school life expectancy by gender is as follows: '
print 'Men Mean : %.2f Years' %(men_data.mean())
print 'Women Mean : %.2f Years' %(women_data.mean())

print '\n\nThe median school life expectancy by gender is as follows: '
print 'Men Median : %.1f Years' %(np.median(men_data))
print 'Women Median : %.1f Years' %(np.median(women_data))

data_final2.to_csv('school_education.csv')
