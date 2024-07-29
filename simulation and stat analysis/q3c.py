import numpy as np
import statsmodels.api as sm
import pylab as py
import matplotlib.pyplot as plt
import scipy.stats as stats

np.random.seed(1)
k = 3
n = 5
a = 0.05
c = k * (k-1)/2
CL = a/c
mean = []
var = []

sample = [np.random.normal(1, 1, n), np.random.normal(0.99, 1, n), np.random.normal(1.01, 1, n)]

for i in range(k):
    mean.append(np.mean(sample[i]))
    var.append(np.var(sample[i], ddof=1))

for i in range(k):
    for j in range(i+1, k):
        dof = (var[i] / n + var[j] / n)**2 / ((((var[i]/n)**2) * (1 / (n-1)) + ((var[j]/n)**2)*(1/(n-1))))
        t = stats.t.ppf(1-CL/2, dof)
        LCIE = round(mean[i] - mean[j] - t, 3)
        UCIE = round(mean[i] - mean[j] + t, 3)
        print('The confidence interval with 95% significance level between systems ', i+1, ' and ', j + 1, 'is [', LCIE, ', ', UCIE, '] ')


