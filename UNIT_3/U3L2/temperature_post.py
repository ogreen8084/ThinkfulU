'''
Last of three files. Takes csv of weather info and returns city with the max
change in temperature for the past 30 days.
Written modularly so that you can use different csv data go get info.
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#csv weather info file to be converted to DataFrame
csv_file = 'weather.csv'

#convert csv to DataFrame and set index
df = pd.read_csv(csv_file)
df=df.set_index('index', drop=True)

#convert DataFrame to matrix type to easily sum temperature variation
df_matrix = df.as_matrix()

#takes the absolute value of each day vs the prior day
temp_change = np.abs(df_matrix[1:]-df_matrix[:-1]).sum(axis=0)

#assigns max_temp column location with the max temp variation
max_temp = temp_change.argmax()

#uses max_temp to find column name that is city with the most temp variation
max_city = df.columns[max_temp]


print "The city with the most temperature variation over the past 30 days was: %s" %(max_city)
print "%s had a temperature variation of %.2f degrees" %(max_city, temp_change[max_temp])

#plot differences in temperature variation for the cities chosen
plt.bar(range(len(temp_change)),temp_change, align= 'center')
plt.xlabel('City')
plt.ylabel('Temperature Variation in Degrees Fahrenheit')
plt.xticks(range(len(temp_change)), df.columns)
plt.show()

