import numpy as np
import statsmodels.api as sm
import pylab as py
import matplotlib.pyplot as plt
import scipy.stats as stats


np.random.seed(1)
n = 5
sample = np.random.standard_t(df = 30, size = n)
quantiles = np.sort(sample)

sm.qqplot(quantiles, line ='45')
py.show()