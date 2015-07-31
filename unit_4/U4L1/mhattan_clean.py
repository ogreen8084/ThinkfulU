'''
File #1, Cleaning file in order to run linear regression.
'''

import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
import numpy as np

sale_data = pd.read_excel('rollingsales_manhattan.xls', skiprows = 4)


'''
Data Cleaning Stage for Regression. Getting rid of '0' sale price and outlying sale prices.
Also getting rid of '0' year built data. Changing multiple variables to categorical.
Finally changing Data Frame column names to make variable names compatible for OLS.
'''

print 'The columns in the DataFrame and the data types are as follows:'
print list(sale_data.columns.values)
print list(sale_data.dtypes)

numerics = ['int64']

'''
Replace column name spaces with underscores and collect numeric column names.
'''
new_col_names = []
numeric_columns = []
for item in sale_data.columns.values:
    item_new = item.replace(" ", "_")
    new_col_names.append(item_new)
    if sale_data[item].dtype in numerics:
    	numeric_columns.append(item_new)
sale_data.columns = new_col_names

'''
#identify numerical columns in sale_data
print numeric_columns
'''
#Describe data
print '\nThe description of the numerical variable is a follows:'
print sale_data.describe()

sale_data['BUILDING_CLASS_CATEGORY'] = sale_data['BUILDING_CLASS_CATEGORY'].astype('category')

#Threshold if more than 20% of data is ZERO, delete zeros.
for item2 in sale_data.columns.values:
	if item2 in numeric_columns:
		if np.percentile(sale_data[item2],20) == 0:
			sale_data= sale_data[sale_data[item2]> 0]

print '\nThe revised description of the numerical variable is a follows:'
print sale_data.describe()


#delete suspiciously cheap purchase outliers
half_percent = np.percentile(sale_data['SALE_PRICE'], .05)
point75_percent = np.percentile(sale_data['SALE_PRICE'], 0.75)
one_percent = np.percentile(sale_data['SALE_PRICE'], 1)

print 'The half percentile of house prices is: %.2f' %(half_percent)
print 'The 0.75 percentile of hous prices is: %.2f' %(point75_percent)
print 'The first percentile of house prices is: %.2f' %(one_percent)

sale_data= sale_data[sale_data['SALE_PRICE'] > point75_percent]

#Check data for outliers, if 99th percentile > 1.5 x 97th percentile delete > 97th percentile
outliers = {}
for item3 in numeric_columns:
	print item3
	ninety_seven = np.percentile(sale_data[item3], 97)
	ninety_nine = np.percentile(sale_data[item3], 99)
	print 'The 97th percentile is: %.2f' %(ninety_seven)
	print 'The 99th percentile is: %.2f' %(ninety_nine)
	if ninety_seven < ninety_nine:
		print 'Proceed with deleting outliers'
		outliers[item3]= ninety_seven
	else:
		pass

#delete outliers if based on previous threshold
for item4 in sale_data.columns.values:
	if item4 in outliers:
		sale_data = sale_data[sale_data[item4]< outliers[item4]]

#print scatter plot
ax = scatter_matrix(sale_data[numeric_columns], alpha = 0.5, diagonal='hist')
plt.show()

print 'The description of the data after cleaning is as follows:'
print sale_data.describe()

print 'The correlation of the numerical variables is as follows:'
print sale_data.corr()


chosen_columns = ['RESIDENTIAL_UNITS', 'TOTAL_UNITS', 'LAND_SQUARE_FEET',
'GROSS_SQUARE_FEET', 'BUILDING_CLASS_CATEGORY', 'SALE_PRICE', 'NEIGHBORHOOD']

print 'The variables chosen for further analysis are as follows:'
print chosen_columns

sale_data = sale_data[chosen_columns]
sale_data.to_csv('sale_data.csv', header = True)
