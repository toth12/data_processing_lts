import pandas as pd
import numpy as np
import itertools
from itertools import chain, combinations
import statsmodels.formula.api as smf
import scipy.stats as scipystats
import statsmodels.api as sm
import statsmodels.stats.stattools as stools
import statsmodels.stats as stats 
from statsmodels.graphics.regressionplots import *
import matplotlib.pyplot as plt
import seaborn as sns
import copy
from sklearn.cross_validation import train_test_split
import math
import time
import pdb
import os,sys
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import text
import numpy as np

input_data=text.ReadCSVasDict('base_data_for_second_qc.csv')
original_x=[record['video_lenght'] for record in input_data if record['video_lenght']!='']

x1=np.array([np.log(float(record['video_lenght'])) for record in input_data if record['video_lenght']!=''])
y1=np.array([np.log(int(record['token_in_current_folia'])) for record in input_data if record['video_lenght']!=''])

pdb.set_trace()


plt.rcParams['figure.figsize'] = (12, 8)

'''
np.random.seed(0)
x1 = np.random.normal(20, 3, 20)
y0 = 5 + 0.5 * x1
y1 = 5 + 0.5 * x1 + np.random.normal(0, 1, 20)

'''

lm = sm.OLS(y1, sm.add_constant(x1)).fit()
print "The rsquared values is " + str(lm.rsquared)


plt.scatter(np.sort(x1), y1[np.argsort(x1)])
plt.scatter(np.mean(x1), np.mean(y1), color = "green")
#plt.plot(np.sort(x1), y0[np.argsort(x1)], label = "actual")
plt.plot(np.sort(x1), lm.predict()[np.argsort(x1)], label = "regression")
plt.title("Linear Regression plots with the regression line")
plt.legend()



fig, ax = plt.subplots(figsize=(12,8))
fig = sm.graphics.influence_plot(lm, alpha  = 0.05, ax = ax, criterion="cooks")
plt.show()

pdb.set_trace()