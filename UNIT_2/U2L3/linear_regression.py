import numpy as np 
import pandas as pd
import statsmodels.api as sm

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')


#lambda functions to clean data
del_percent = lambda x: float(x[:-1])/100
del_months = lambda g: int(g[:-7])
del_fico = lambda g: min(int(g[-3:]), int(g[0:3]))

#empty lists to append cleaned data to
percent_gone, num_months, fico_scr =[],[],[]

#iterate over Interest rate data, take out percent sign and convert to floating number
for item in loansData['Interest.Rate']:
	percent_gone.append(del_percent(item))
loansData['Interest.Rate']=percent_gone

#iterate over loan length data, take out ' months'
for obj in loansData['Loan.Length']:
	num_months.append(del_months(obj))
loansData['Loan.Length']=num_months

#iterate over Fico range, convert to integer and pick small number in range 
for obj2 in loansData['FICO.Range']:
	fico_scr.append(del_fico(obj2))
loansData['FICO.Score']=fico_scr

#extracting data for regression variables
intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

#regression variables
y = np.matrix(intrate).transpose()
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

#column stack x variables
x = np.column_stack([x1,x2])

#create linear model
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

#linear model output
print f.summary()





