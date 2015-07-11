import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

#import file
df = pd.read_csv('LoanStats3d.csv', dtype= 'unicode', skiprows =1 )


'''
tested data on 500 rows because it was too much for my computer
comment line to perform analysis on entire dataset
'''

df=df.drop(df.index[500:])



#clean interest rate by eliminating %-sign and converting to a decimal
percent_gone = []
income = []
del_percent = lambda x: round(float(x[:-1])/100, 2)
for item in df['int_rate']:
	percent_gone.append(del_percent(item))
df['int_rate'] = percent_gone
#make list of annual incomes to plot chart
for item2 in df['annual_inc']:
	income.append(float(item2))

df['annual_inc']= income

plt.scatter(df.annual_inc, df.int_rate)
plt.xlabel('Annual Income')
plt.ylabel('Interest Rate')
plt.show()

#fitting data using annual income as single independent variable
est = smf.ols(formula ="int_rate ~ annual_inc", data=df).fit()
print 'The p values for the coefficient and independent variable is as follows:'
print est.pvalues


#formatting home ownership categorical data
df['home_ownership_ord'] = pd.Categorical(df.home_ownership).codes




#fitting annual income and home ownership as independent variables
est2 = smf.ols(formula = "int_rate ~ annual_inc + home_ownership_ord", data=df).fit()
print 'The p values for the coefficient and independent variables are as follows:'
print est2.pvalues

#fitting annual income and home ownership and including interaction between the two
est3 = smf.ols(formula = "int_rate ~ annual_inc * home_ownership_ord", data=df).fit()
()
print 'The p values for the coefficient and independent variables are as follows:'
print est3.pvalues

print 'From the p values we can see that home ownership is not a significant variable, it should be dropped from futher analysis'


