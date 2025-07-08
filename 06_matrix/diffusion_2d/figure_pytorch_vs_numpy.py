from pprint import pprint
from collections import defaultdict

import torch
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as py

import diffusion_pytorch_compute
import diffusion_numpy_memory
from _utils import run_experiment_time_limit, iter_sizes_2ph, plot_add_speedup, cache_df_workload


@cache_df_workload("figure_pytorch_vs_numpy.csv")
def workload():
    data = []
    methods = (
        (
            "Numpy+memory",
            diffusion_numpy_memory,
            lambda : run_experiment_time_limit(diffusion_numpy_memory, max_time=10, n_runs=1)[0]
        ),
        (
            "PyTorch",
            diffusion_pytorch_compute,
            lambda : diffusion_pytorch_compute.run_experiment(5000) / 5000
        )
    )
    for size in iter_sizes_2ph(9, 14):
        print(f"Grid Shape: {size}")
        for name, module, method in methods:
            module.grid_shape = (size, size)
            t = method()
            print(f"\t{name}: {t}")
            data.append({
                "size": size,
                "method": name,
                "time": t,
            })

    df = pd.DataFrame.from_records(data)
    df["speedup"] = df.groupby("size")["time"].transform("max") / df["time"]
    return df

if __name__ == "__main__":
    df = workload()
    print(df)

    sizes = list(set(df["size"]))
    size_headers = [f"{size}x{size}" for size in sizes]

    sns.set(font_scale=1.5)
    g = sns.lineplot(df, x='size', y='time', hue='method', style='method', markers=True, dashes=False, markersize=15)
    plot_add_speedup(df, g)

    # g.set_yscale('log')
    g.set_xscale('log')
    g.set_title("Numpy+NumExpr versus PyTorch for various grid sizes")
    g.set_xticks(sizes, rotation=45, labels=size_headers, ha='right')
    g.set_xlabel("Grid Size")
    g.set_ylabel("Time per Iteration (s)")

    py.tight_layout()
    py.savefig("images/pytorch_vs_numpy.png")
