'''
Truncated sig digits on numbers and adjusted lines too long.
'''

import pandas as pd
from scipy import stats

data = '''Region,Alcohol,Tobacco
North, 6.47, 4.03
Yorkshire,6.13,3.76
Northeast,6.19,3.77
East Midlands,4.89,3.34
West Midlands,5.63,3.47
East Anglia,4.52,2.92
Southeast,5.89,3.20
Southwest,4.79,2.71
Wales,5.27,3.53
Scotland,6.08,4.51
Northern Ireland,4.02,4.56'''

data = data.splitlines()

data = [i.split(',') for i in data]

column_names = data[0]
data_rows = data[1::]
df = pd.DataFrame(data_rows, columns= column_names)

df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)
print 'The mean for the Alcohol and Tobacco set is '\
+ str(df['Alcohol'].mean()) +' for Alcohol and ' +str(df['Tobacco'].mean())\
+ ' for Tobacco.'

print 'The median for the Alcohol and Tobacco set is '\
+ str(df['Alcohol'].median()) +' for Alcohol and ' +str(df['Tobacco'].median())\
+ ' for Tobacco.'

print 'The mode for the Alcohol and Tobacco set is '\
+ str(stats.mode(df['Alcohol'])[0]) +' for Alcohol and '\
+str(stats.mode(df['Tobacco'])[0]) + ' for Tobacco.'

print 'The range for the Alcohol and Tobacco set is '\
+ str(max(df['Alcohol'])-min(df['Tobacco']))+' for Alcohol and '\
+ str(max(df['Tobacco'])-min(df['Tobacco']))+' for Tobacco.'

print 'The variance for the Alcohol and Tobacco set is '\
+ str(round(df['Alcohol'].var(), 2)) + ' for Alcohol and '\
+ str(round(df['Tobacco'].var(),2))+ ' for Tobacco.'

print 'The standard deviation for the Alcohol and Tobacco set is '\
+ str(round(df['Alcohol'].std(), 2)) + ' for Alcohol and '\
+ str(round(df['Tobacco'].std(),2)) + ' for Tobacco.'



