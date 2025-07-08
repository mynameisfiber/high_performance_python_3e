import time
import pandas as pd
from numpy.testing import assert_almost_equal, assert_array_almost_equal
import numba
from numba import jit
import numpy as np
import matplotlib.pyplot
from utility import ols_lstsq, ols_lstsq_raw


import dask.dataframe as dd
import dask
#import swifter

if __name__ == "__main__":
    df = pd.read_pickle('generated_ols_data.pickle')
    print(f"{df.shape=}")
    df = pd.concat([df]*40)
    print(f"{df.shape=}")
    print(f"Loaded {df.shape} rows")

    t1 = time.time()
    results_ols_lstsq = df.apply(ols_lstsq, axis=1)
    t2 = time.time()
    print(f"Pandas ols_lstsq {t2 - t1}")

    N_PARTITIONS = 8
    ddf = dd.from_pandas(df, npartitions=N_PARTITIONS, sort=False)
    #SCHEDULER = "threads"
    SCHEDULER = "processes"
    # met provides the return type as a name & dtype

    t1 = time.time()
    results = ddf.apply(ols_lstsq, axis=1, meta=(None, 'float64',)).compute(scheduler=SCHEDULER)
    t2 = time.time()
    assert_array_almost_equal(results, results_ols_lstsq)  
    print(f"Dask ols_lstsq {t2 - t1}")
    t1 = time.time()
    results = ddf.apply(ols_lstsq_raw, axis=1, meta=(None, 'float64',), raw=True).compute(scheduler=SCHEDULER)
    t2 = time.time()
    assert_array_almost_equal(results, results_ols_lstsq)  
    print(f"Dask ols_lstsq_raw raw=True {t2 - t1}")

    # without the meta arg it tells us what return type it inferred
    #results_df_ols_np_distributed = ddf.apply(ols_np_distributed, axis=1).compute(scheduler=SCHEDULER)
    assert_array_almost_equal(results, results_ols_lstsq)  


    if False:
        t1 = time.time()
        results = df.swifter.progress_bar(False).apply(ols_lstsq_raw, axis=1, raw=True)
        t2 = time.time()
        print(f"swifter ols_lstsq_raw raw=True {t2 - t1}")
        #results = df.swifter.progress_bar(False).apply(ols_lstsq_raw, axis=1)
        assert_array_almost_equal(results, results_ols_lstsq)  

        #t1 = time.time()
        #results = ddf.apply(ols_lstsq_raw_values_numba, axis=1, meta=(None, 'float64',), raw=True).compute(scheduler=SCHEDULER)
        #t2 = time.time()
        #assert_array_almost_equal(results, results_ols_lstsq)  
        #print(f"Dask ols_lstsq_raw_values_numba  {t2 - t1}")
        #assert_array_almost_equal(results, results_ols_lstsq)  

