'''
File #2, running linear regression on manhattan data.
'''

import pandas as pd
import statsmodels.api as sm 
import numpy as np
import matplotlib.pyplot as plt 
import statsmodels.formula.api as smf


sale_data = pd.DataFrame.from_csv('sale_data.csv', header = 0)

#Printing description of the numerical data after it has been cleaned.
print 'The description of the numerical variables is as follows:'
print sale_data.describe()
print '\n The correlation of the numerical variables is as follows:'
print sale_data.corr()
print '\nThe median of the numerical variables are as follows: '
print sale_data.median()


sale_price = sale_data['SALE_PRICE']
year = sale_data['YEAR']
comunits = sale_data['C_UNITS']
resunits = sale_data['R_UNITS']
gsqft = sale_data['GSQFT']
zip_code = sale_data['ZIP']
txcl_sale = sale_data['TXCL_SALE']
txcl_now = sale_data['TXCL_NOW']
bld_class = sale_data['BLD_CLASS']


#fit data for year to regression line
fit_year = np.polyfit(year, sale_price , 1)
fit_yr =np.poly1d(fit_year)


#plot year vs sale price
plt.figure(1)
plt.plot(year, sale_price, 'yo', year, fit_yr(year), '--k')
plt.xlabel('YEAR BUILT')
plt.ylabel('SALE PRICE')
plt.show()




est = smf.ols(formula = "SALE_PRICE ~ YEAR + GSQFT + LSQFT", data= sale_data).fit() 

print est.summary()
print '\nThe parameters from this regression attempt were as follows:'
print est.params

print "\nThe p-value of 'YEAR' indicates that it is not a significant variable."

print "\nThis next regression attempt will take out year and add build class."

est2 = smf.ols(formula = "SALE_PRICE ~ GSQFT + LSQFT + BLD_CLASS", data = sale_data).fit()

print est2.summary()
print '\nThe parameters from this improved regression attempt were as follows:'
print est2.params