from scipy import stats
import collections
import pandas as pd
import matplotlib.pyplot as plt

#load data
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
#clean data
loansData.dropna(inplace=True)

#count data by value to perform chi test
freq = collections.Counter(loansData['Open.CREDIT.Lines'])

#perform chi test
chi, p= stats.chisquare(freq.values())

#print chi square score and p-value
print chi
print p