'''
File #2, running linear regression on manhattan data.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import statsmodels.formula.api as smf
from sklearn.cross_validation import train_test_split


sale_data = pd.DataFrame.from_csv('sale_data.csv', header = 0)

print list(sale_data.columns.values)




#fit data for residential units to regression line
fit_res_units = np.polyfit(sale_data['RESIDENTIAL_UNITS'], sale_data['SALE_PRICE'] , 1)
fit_runits = np.poly1d(fit_res_units)

'''
plot residential units vs sale price
'''
plt.figure(1)
plt.plot(sale_data['RESIDENTIAL_UNITS'], sale_data['SALE_PRICE'], 'yo', 
	sale_data['RESIDENTIAL_UNITS'], fit_runits(sale_data['RESIDENTIAL_UNITS']), '--k')
plt.xlabel('RESIDENTIAL UNITS')
plt.ylabel('SALE PRICE')
plt.show()



#fit data for total units to regression line
fit_tot_units = np.polyfit(sale_data['TOTAL_UNITS'], sale_data['SALE_PRICE'] , 1)
fit_tunits = np.poly1d(fit_tot_units)

#plot total units vs sale price
plt.figure(2)
plt.plot(sale_data['TOTAL_UNITS'], sale_data['SALE_PRICE'], 'yo', 
	sale_data['TOTAL_UNITS'], fit_tunits(sale_data['TOTAL_UNITS']), '--k')
plt.xlabel('TOTAL UNITS')
plt.ylabel('SALE PRICE')
plt.show()



#fit data for total units to regression line
fit_lnd_sqft = np.polyfit(sale_data['LAND_SQUARE_FEET'], sale_data['SALE_PRICE'] , 1)
fit_lsqft = np.poly1d(fit_lnd_sqft)

#plot total units vs sale price
plt.figure(2)
plt.plot(sale_data['LAND_SQUARE_FEET'], sale_data['SALE_PRICE'], 'yo', 
	sale_data['LAND_SQUARE_FEET'], fit_lsqft(sale_data['LAND_SQUARE_FEET']), '--k')
plt.xlabel('LAND SQUARE FEET')
plt.ylabel('SALE PRICE')
plt.show()



#fit data for total units to regression line
fit_grs_sqft = np.polyfit(sale_data['GROSS_SQUARE_FEET'], sale_data['SALE_PRICE'] , 1)
fit_gsqft = np.poly1d(fit_grs_sqft)

#plot total units vs sale price
plt.figure(2)
plt.plot(sale_data['GROSS_SQUARE_FEET'], sale_data['SALE_PRICE'], 'yo', 
	sale_data['GROSS_SQUARE_FEET'], fit_gsqft(sale_data['GROSS_SQUARE_FEET']), '--k')
plt.xlabel('GROSS SQUARE FEET')
plt.ylabel('SALE PRICE')
plt.show()


saleTrain, saleTest = train_test_split(sale_data, test_size = 0.2)



#plot information
print 'Training Regression to get error statistics.'
est = smf.ols(formula = "SALE_PRICE ~ GROSS_SQUARE_FEET + np.log(TOTAL_UNITS) + RESIDENTIAL_UNITS**2",
 data= saleTrain).fit() 

print est.summary()
print '\nThe parameters from this regression attempt were as follows:'
print est.params



predicted_sales = est.predict(saleTest)
actual_sales = saleTest['SALE_PRICE']
df_error = np.abs(predicted_sales - actual_sales)/actual_sales
print "Statistics of percentage error between predicted and actual sales: "
print df_error.describe()

form = "SALE_PRICE ~ GROSS_SQUARE_FEET + np.log(TOTAL_UNITS) + RESIDENTIAL_UNITS**2" +\
"+ C(BUILDING_CLASS_CATEGORY) + C(NEIGHBORHOOD)"

#plot information
print 'Regression using Building Class Category and Neighborhood as Categorical Variables'
est = smf.ols(formula = form, data= sale_data).fit() 

print est.summary()
print '\nThe parameters from this regression attempt were as follows:'
print est.params
