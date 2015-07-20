#pulled out site to make it easier to change sites

import numpy as np 
import pandas as pd
import statsmodels.api as sm

#site to pull data from
web_site = 'https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv'

#make 2 dataframes, one mastere and one for only needed info
loansData = pd.read_csv(web_site)
df = pd.DataFrame()

#lambda functions to clean data
del_percent = lambda x: float(x[:-1])/100
del_months = lambda g: int(g[:-7])
del_fico = lambda g: min(int(g[-3:]), int(g[0:3]))

#empty lists to append cleaned data to
percent_gone, num_months, fico_scr, irtf =[],[],[], []

#iterate over Interest rate data, take out percent sign
#and convert to floating number
for item in loansData['Interest.Rate']:
	percent_gone.append(del_percent(item))
loansData['Interest.Rate']=percent_gone



#iterate over Fico range, convert to integer and pick small number in range 
for obj2 in loansData['FICO.Range']:
	fico_scr.append(del_fico(obj2))
loansData['FICO.Score']=fico_scr


for obj3 in loansData['Interest.Rate']:
	if obj3 <0.12:
		irtf.append(0)
	else:
		irtf.append(1)

#make new dataframe with only needed columns
df['FicoScore'] = loansData['FICO.Score']		
df['Intercept'] = 1
df['IR_TF']= irtf		
df['AmountRequested'] = loansData['Amount.Requested']

#use linear regressino formula to get coefficients
ind_vars = ['Intercept', 'FicoScore','AmountRequested']
logit = sm.Logit(df['IR_TF'], df[ind_vars])
result = logit.fit()
coeff = result.params

#create predictor function that uses score and loan amount requested
def logistic_function(score, loan):
	predictor = 1/(1+ np.exp(coeff[0] + coeff[1]*score+coeff[2]*loan))

	print 'Your income is %.2f and your Fico Score is %.2f' %(score, loan)

	if predictor > 0.70:
		print 'Your prediction score is : %.2f, you will get the loan'\
		' of %.2f ' %(predictor, loan)

	else: 
		print 'Your prediction score is : %.2f, sorry you will not'\
		' get the loan' %(predictor)

#test cases
logistic_function(620, 10000)
logistic_function(720, 10000)
logistic_function(720, 12000)


