import collections
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt


x = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]
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
