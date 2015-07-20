'''
Just shortened lines.
'''

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima_model import ARIMA

df = pd.read_csv('LoanStats3d.csv', header=1, low_memory=False)

# converts string to datetime object in pandas:
df = df.dropna(subset= ['issue_d'])

#dictionary created to deal with 
month_dic = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04','May':'05',
'Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

#convert date to a readable time for to_datetime in lists
change_year = []
change_month = []
for item in df['issue_d']:
	change_month.append(month_dic[item[0:3]])
	change_year.append(str(item[4:8]))

#add new columns to df to convert date_time
df['year']=change_year
df['month']= change_month
df['issue_d_format'] = pd.to_datetime(df['year'] + df['month'], format='%Y%m')

#group loans by month
dfts = df.set_index('issue_d_format') 
year_month_summary = dfts.groupby(lambda x : x.year*100+ x.month).count()
loan_count_summary = year_month_summary['issue_d']

#revise index so that data can be plotted ion an ongoing basis
loan_count_summary.index =  range(0, len(loan_count_summary))

#plot raw loan count data
lcs = loan_count_summary.plot(label ='Loans Raw Data')
lcs.set_xlabel('Time (1 unit is a Month)')
lcs.set_ylabel('Loan Count')
lcs.legend(['Loans Raw Data'])
plt.show()


#use regression formula to identify trend in loan counts over time
est = smf.ols(formula = "loan_count_summary ~ loan_count_summary.index", 
	data = loan_count_summary).fit()

     
print '\nThe data has the following regression parameters:'
print 'The intercept is : %r' %(round(est.params[0], 2))
print 'The slope is     : %r' %(round(est.params[1], 2))
print '\nThe data set is not stationary. Consequently, the '\
'regression value will be subtracted from each data point'

#subtract regression line from loan count data to account for non-stationary data
new_loan= []
item_count = 0
for item in loan_count_summary:
	 new_loan.append(item-est.params[0]-est.params[1]*item_count)
	 item_count +=1
loan_count_rev = pd.Series(new_loan, index = loan_count_summary.index)

#create variables to plot regression line 
x = loan_count_summary.index
y = est.params[0]+ est.params[1]*x


#plot regression line with loan data and detrended data
plt.plot(x, y, 'r-')
loan_count_rev.plot()
lcr = loan_count_summary.plot()
lcr.set_xlabel('Time (1 unit is a Month)')
lcr.set_ylabel('Loan Count')
lcr.legend(['OLS Regression Line', 'Loan Count Detrended (Y-Regression Line)', 
	'Loan Count Raw Data'])
plt.show()

#plot auto-correlation and partial auto-correlation
plot_acf(loan_count_rev)
plt.show()
plot_pacf(loan_count_rev)
plt.show()

