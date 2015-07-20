'''
Made variable for website to make it easier to switch sites
rounded chi-square score 
'''
from scipy import stats
import collections
import pandas as pd
import matplotlib.pyplot as plt

web_site = 'https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv'
#load data
loansData = pd.read_csv(web_site)
#clean data
loansData.dropna(inplace=True)

#count data by value to perform chi test
freq = collections.Counter(loansData['Open.CREDIT.Lines'])

#perform chi test
chi, p= stats.chisquare(freq.values())

#print chi square score and p-value
print 'The chi-square score is: %.2f' %(chi)
print 'The p-value is: %f' %(p)
print 'From the p-value we can infer that there is a significant relationship'