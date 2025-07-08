import timeit
import pandas as pd
import matplotlib.pyplot
from sklearn.linear_model import _base
from sklearn.linear_model import LinearRegression
from sklearn.utils import check_X_y
import matplotlib.pyplot as plt
from line_profiler import LineProfiler
import numpy as np 
from utility import ols_lstsq, ols_sklearn

# We learn that
#https://github.com/scikit-learn/scikit-learn/blob/1495f6924/sklearn/linear_model/base.py#L438
# LinearRegression.fit is expensive because
# of calls to check_X_y, _preprocess_data and linalg.lstsq
# https://github.com/scikit-learn/scikit-learn/blob/1495f6924/sklearn/linear_model/base.py#L101
# _preprocess_data
# has 3 expensive lines - check_array, np.asarray, np.average
#https://github.com/scikit-learn/scikit-learn/blob/1495f69242646d239d89a5713982946b8ffcf9d9/sklearn/utils/validation.py#L600
# check_X_y
# checks for array for certain characteristics and lengths
# 


df = pd.read_pickle('generated_ols_data.pickle')
print(f"Loaded {df.shape} rows")

est = LinearRegression()
row = df.iloc[0]
X = np.arange(row.shape[0]).reshape(-1, 1).astype(np.float_)

y = row.values
#est.fit(X, y) # this line is here for debugging/tracing through only

# without wrapped, with sklearn 1.5+, we profile the wrapper not fit!
lp = LineProfiler(est.fit)
print("------------------")
print("Run on a single row")
lp.run("est.fit(X, row.values)") # orig
lp.print_stats()



print("------------------")
# here we can profile both wrapper and the wrapped fn
lp = LineProfiler(est.fit.__wrapped__)
print("Run on a single row with __wrapped__")
lp.run("est.fit(X, row.values)")
lp.print_stats()


print("------------------")
# here we can profile both wrapper and the wrapped fn and costly fns
lp = LineProfiler(est.fit.__wrapped__)
lp.add_function(est._validate_data)
from sklearn.linear_model import _base
lp.add_function(_base._preprocess_data)
from sklearn.utils import check_X_y
lp.add_function(check_X_y)
print("Run on a single row with __wrapped__")
lp.run("est.fit(X, row.values)")
lp.print_stats()


import sklearn
# note that disabling parameter validation saves a little bit of time
# in the wrapper function, but not in fit!
sklearn.set_config(skip_parameter_validation=True)
print("------------------")
# here we can profile both wrapper and the wrapped fn
lp = LineProfiler(est.fit.__wrapped__)
print("Run on a single row with __wrapped__")
lp.run("est.fit(X, row.values)")
lp.print_stats()

import sys
sys.exit(0)
#1/0

print("------------------")
print("Run on 5000 rows")
lp.run("df[:5000].apply(ols_sklearn, axis=1)")
lp.print_stats()

# old 2nd ed code

print("------------------")
lp = LineProfiler(_base._preprocess_data)
lp.run("_base._preprocess_data(X, row, fit_intercept=True)")
lp.print_stats()

print("------------------")
lp = LineProfiler(check_X_y)
lp.run("check_X_y(X, y, accept_sparse=['csr', 'csc', 'coo'], y_numeric=True, multi_output=True)")
lp.print_stats()

#%lprun -f est_diagnosis.fit est_diagnosis.fit(np.arange(rowx.shape[0]).reshape(-1, 1), rowx.values)
#lp.run("est_diagnosis.fit(np.arange(rowx.shape[0]).reshape(-1, 1).astype(np.float_), y.values)")
#lp.run("base._preprocess_data(np.arange(rowx.shape[0]).reshape(-1, 1).astype(np.float_), rowx, fit_intercept=True)")

