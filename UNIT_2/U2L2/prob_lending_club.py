#Made website a variable to make it easier to change sites

import matplotlib.pyplot as plt
import pandas as pd 
import scipy.stats as stats

web_site = 'https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv'

loansData = pd.read_csv(web_site)

#clean data by dropping na values
loansData.dropna(inplace=True)

#create and save box plot
loansData.boxplot(column='Amount.Requested')
plt.savefig('am_request_box.png')
plt.figure()

#create and save histogram
loansData.hist(column='Amount.Requested')
plt.savefig('am_request_hist.png')
plt.figure()

#create and save qqplot
graph = stats.probplot(loansData['Amount.Requested'], dist="norm", plot=plt)
plt.savefig('am_request_qqplot.png')