import numpy as np
import statsmodels.api as sm
import pylab as py
import matplotlib.pyplot as plt
import scipy.stats as stats


np.random.seed(1)

n = 300
k = 5
p = 1/k
sample = np.random.uniform(0,1,n)
count, edge, bars = plt.hist(sample, bins = k)
plt.title('Sample distribution')

D = 0
for freq in count:
    D += (freq - n*p)**2 / (n*p)
print('D from chi-square goodness-to-fit test = ', D)
