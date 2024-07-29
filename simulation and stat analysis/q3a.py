import numpy as np
import statsmodels.api as sm
import pylab as py
import matplotlib.pyplot as plt
import scipy.stats as stats


np.random.seed(1)
n0 = 20
k = 3
P = 0.9
d = 0.01
h1 = 2.342
N = []
var = []


sample_systems = [np.random.normal(1, 1, n0), np.random.normal(0.99, 1, n0), np.random.normal(1.01, 1, n0)]

mean1 = []
for i in range(3):
    mean1.append(np.mean(sample_systems[i]))
    var.append(np.var(sample_systems[i], ddof=1))

for i in range(3):
    N.append(max(n0+1, np.ceil(((h1**2) * var[i]) / (d**2))))

n = [int(N[0] - n0), int(N[1] - n0), int(N[2] - n0)]
sample_systems_new = [np.random.normal(1, 1, n[0]), np.random.normal(0.99, 1, n[1]), np.random.normal(1.01, 1, n[2])]

mean2 = []
for i in range(3):
    mean2.append(np.mean(sample_systems_new[i]))

meanW = []
for i in range(3):
    ws = (n0/N[i]) * (1 + np.sqrt(1 - (N[i]/n0) * (1 - (N[i] - n0) * (d**2) / (h1**2 * var[i]))))
    meanWS = ws * mean1[i] + (1 - ws) * mean2[i]
    print('system ', i + 1, ': weighted sample mean = ', meanWS)
