import numpy as np
import statsmodels.api as sm
import pylab as py
import matplotlib.pyplot as plt
import scipy.stats as stats
from tables.utils import NailedDict

np.random.seed(1)
J = 3
n = 5
N = J * n
sample = [np.random.normal(1, 1, n), np.random.normal(0.99, 1, n), np.random.normal(1.01, 1, n)]
mean = []
sd = []

sum = 0
for i in range(J):
    sum += sample[i].sum()
    mean.append(np.mean(sample[i]))
    sd.append(np.std(sample[i], ddof=1))
grand_mean = sum/N

SSB = 0
SSW = 0
MSB = 0
MSW = 0

for i in range(J):
    SSB += n * ((mean[i] - grand_mean)**2)
    SSW += (n - 1) * (sd[i]**2)

MSB = SSB / (J - 1)
MSW = SSW / (J * (n - 1))

F = MSB / MSW
print('F = ', F)