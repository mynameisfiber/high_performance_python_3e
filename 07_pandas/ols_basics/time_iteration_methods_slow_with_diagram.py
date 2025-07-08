import time
import pandas as pd
from numpy.testing import assert_almost_equal, assert_array_almost_equal
import numba
from numba import jit
import numpy as np
import matplotlib.pyplot
from utility import ols_lstsq, ols_lstsq_raw
import matplotlib as mpl
import matplotlib.pyplot as plt
import pickle

def set_common_mpl_styles(
    ax,
    legend=True,
    grid_axis="y",
    ylabel=None,
    xlabel=None,
    title=None,
    ymin=None,
    xmin=None,
):
    """Nice common plot configuration
    We might use it via `fig, ax = plt.subplots(constrained_layout=True, figsize=(8, 6))`
    """
    if grid_axis is not None:
        # depending on major/minor grid frequency we might
        # need the simpler form
        # ax.grid(axis=grid_axis)
        ax.grid(visible=True, which="both", axis=grid_axis)
    if legend is False:
        if ax.legend_:
            ax.legend_.remove()
    else:
        ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if title is not None:
        ax.set_title(title)
    if ymin is not None:
        ax.set_ylim(ymin=ymin)
    if xmin is not None:
        ax.set_xlim(xmin=xmin)

df = pd.read_pickle('generated_ols_data.pickle')
print(f"Loaded {df.shape} rows")

#df = df[:100000]

results_ols_lstsq = df.apply(ols_lstsq, axis=1)


t1 = time.time()
t1a = time.time()
t1_start = time.time()
nbr_iterations = df.shape[0]
time_per_chunk = []
results = None
for row_idx in range(nbr_iterations):
    if row_idx % 10000 == 0:
        if row_idx > 0:
            t1b = time.time()
            print(f"At row {row_idx:,} taking {t1b-t1a} for the last block")
            t1a = t1b
    row = df.iloc[row_idx]
    m = ols_lstsq(row)
    if results is None:
        results = pd.Series([m])
    else:
        #results = results.append(pd.Series([m]))  # equivalent to concat
        results = pd.concat((results, pd.Series([m])))

    # capture the time it takes every 10% of the iterations
    if row_idx % (nbr_iterations/10) == 0:
        tdelta = time.time() - t1
        t1 = time.time()
        time_per_chunk.append(tdelta)        

# capture the last chunk
tdelta = time.time() - t1
time_per_chunk.append(tdelta)     

with open("concat_cost_per_iteration_chunk.pickle", "wb") as f:
    pickle.dump(time_per_chunk, f)

t2 = time.time()
assert_array_almost_equal(results_ols_lstsq, results)
print(f"Dereference with iloc and continuous build {t2 - t1_start}")

fig, ax = plt.subplots(constrained_layout=True, figsize=(4, 4))

ax.bar(range(len(time_per_chunk)), time_per_chunk);
set_common_mpl_styles(ax, ylabel="Time (s)", xlabel="Iteration chunk", 
                      title="Concat cost per iteration chunk", legend=False);
ax.set_xlim(xmin=0)

fig.savefig("concat_cost_per_iteration_chunk.png")