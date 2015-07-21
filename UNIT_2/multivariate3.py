import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

#import file
df = pd.read_csv('LoanStats3d.csv', low_memory=False, skiprows =1 )

#drop Nan values for relevant columns
df = df.dropna(subset = ['int_rate', 'home_ownership', 'annual_inc'])


#function to clean interest rate by eliminating %-sign and converting to a decimal
convert_percent = lambda x: round(float(x[:-1])/100, 2)
convert_income = lambda y: float(y)

#map functions to series
df['int_rate']=df['int_rate'].map(convert_percent)
df['annual_inc'] = df['annual_inc'].map(convert_income)


#single regression using annual income as the dependent variable
est = smf.ols(formula = "int_rate ~ annual_inc", data = df).fit()
print 'The coefficients and p-values of the single regression are as follows:'
print ' Type            Coefficient           p-value:'
print 'Intercept    ' + str(round(est.params[0], 10)) +'           '+ str(round(est.pvalues[0],4))
print 'Dep. Var     ' + str(round(est.params[1], 10)) +'           '+ str(round(est.pvalues[1],4))
print '*All variables are significant based on p-values, the rsquared value is: %f' %(est.rsquared)+ '\n'

#convert home ownership to useable categorical values
df['home_ownership_ord'] = pd.Categorical(df.home_ownership).codes

#fitting annual income and home ownership as independent variables
est2 = smf.ols(formula = "int_rate ~ annual_inc + home_ownership_ord", data=df).fit()
print 'The coefficients and p-values of the multiple regression are as follows: '
print ' Type            Coefficient          p-value:'
print 'Intercept    ' + str(round(est2.params[0], 10)) +'           '+ str(round(est2.pvalues[0],4))
print 'Dep. Var 1   ' + str(round(est2.params[1], 10)) +'           '+ str(round(est2.pvalues[1],4))
print 'Dep. Var 2   ' + str(round(est2.params[2], 10)) +'           '+ str(round(est2.pvalues[2],4))
print '*All variables are significant based on p-values, the rsquared value is: %f' %(est2.rsquared)+ '\n'


#fitting annual income and home ownership and including interaction between the two
est3 = smf.ols(formula = "int_rate ~ annual_inc * home_ownership_ord", data=df).fit()
print 'The coefficients and p-values of the multiple regression are as follows: '
print ' Type            Coefficient          p-value:'
print 'Intercept    ' + str(round(est3.params[0], 10)) +'           '+ str(round(est3.pvalues[0],4))
print 'Dep. Var 1   ' + str(round(est3.params[1], 10)) +'           '+ str(round(est3.pvalues[1],4))
print 'Dep. Var 2   ' + str(round(est3.params[2], 10)) +'           '+ str(round(est3.pvalues[2],4))
print 'Var Interact ' + str(round(est3.params[2], 10)) +'           '+ str(round(est3.pvalues[2],4))
print '*All variables are significant based on p-values, the rsquared value is: %f' %(est3.rsquared)+ '\n'

