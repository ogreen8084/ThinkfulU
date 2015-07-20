'''
Shortened line and re-did how list was created. 
'''

import collections
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt


x = [1] * 8  +  [2] * 3 + [3] + [4] * 4 + [5] + [6] * 3
x = x +[7] * 8 +[8] * 2 + [9] *2
c = collections.Counter(x)

print c

plt.figure()
plt.boxplot(x)
plt.savefig('boxplot_x.png')
plt.figure()
plt.hist(x, histtype='bar')
plt.savefig('hist_x.png')
plt.figure()
graph1 = stats.probplot(x, dist='norm', plot =plt)
plt.savefig('qqplot_x.png')
