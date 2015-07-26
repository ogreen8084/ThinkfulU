import pandas as pd
import statsmodels.api as sm 
import numpy as np
import matplotlib.pyplot as plt 
import statsmodels.formula.api as smf

xls = pd.read_excel('rollingsales_manhattan.xls', skiprows = 4)


'''
Data Cleaning Stage for Regression. Getting rid of '0' sale price and outlying sale prices.
Also getting rid of '0' year built data. Changing multiple variables to categorical.
Finally changing Data Frame column names to make variable names compatible for OLS.
'''
sale_data = xls[xls['SALE PRICE'] > 0] 
sale_data.is_copy = False #suppress warnings about altering a copy
sale_data = sale_data[sale_data['YEAR BUILT'] > 0]
sale_data = sale_data[sale_data['SALE PRICE'] < 5000000]
sale_data['ZIP CODE'] = sale_data['ZIP CODE'].apply(str)
sale_data['ZIP CODE'] = sale_data['ZIP CODE'].astype('category')
sale_data['TAX CLASS AT TIME OF SALE'] = sale_data['TAX CLASS AT TIME OF SALE'].astype('category')
sale_data['TAX CLASS AT PRESENT'] = sale_data['TAX CLASS AT PRESENT'].astype('category')
sale_data['BLOCK'] = sale_data['BLOCK'].astype('category')
sale_data['BUILDING CLASS CATEGORY']= sale_data['BUILDING CLASS CATEGORY'].astype('category')
sale_data = sale_data.rename(columns = {'SALE PRICE' : 'SALE_PRICE', 
	'YEAR BUILT' : 'YEAR', 'LAND SQUARE FEET' : 'LSQFT', 
	'GROSS SQUARE FEET' : 'GSQFT', 'ZIP CODE': 'ZIP', 
	'TAX CLASS AT TIME OF SALE': 'TXCL_SALE', 'TAX CLASS AT PRESENT': 'TXCL_NOW',
	'BUILDING CLASS CATEGORY' : 'BLD_CLASS', 'RESIDENTIAL UNITS' : 'R_UNITS',
	'COMMERCIAL UNITS' : 'C_UNITS', 'TOTAL UNITS' : 'T_UNITS' })
sale_data = sale_data[['SALE_PRICE', 'YEAR', 'LSQFT', 'GSQFT', 'ZIP', 'TXCL_SALE', 'TXCL_NOW', 
'BLD_CLASS', 'R_UNITS' , 'C_UNITS', 'T_UNITS']]

#too many zeroes so changing r_units, c_units, to categorical variables 
sale_data.loc[sale_data.R_UNITS != 0, 'R_UNITS'] = 1
sale_data.loc[sale_data.C_UNITS != 0, 'C_UNITS'] = 1
sale_data['R_UNITS'] = sale_data['R_UNITS'].astype('category')
sale_data['C_UNITS'] = sale_data['C_UNITS'].astype('category')
sale_data['ZIP'] = sale_data['ZIP'].astype('category')

sale_data.to_csv('sale_data.csv', header = True)
