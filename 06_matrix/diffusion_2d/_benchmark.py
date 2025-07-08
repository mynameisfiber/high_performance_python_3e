#!/usr/bin/env python3

from collections import namedtuple

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as py

import diffusion_numpy_naive
import diffusion_numpy_memory
import diffusion_numpy_memory2
import diffusion_numpy_memory2_numexpr
import diffusion_python
import diffusion_python_memory
import diffusion_scipy
import diffusion_pytorch_compute
import diffusion_pytorch_conv

from _utils import run_experiment_time_limit, create_table, cache_df_workload


Method = namedtuple("Method", "module xref".split(" "))

methods = [
    ("python", Method(diffusion_python, "matrix_pure_python_run")),
    ("python+memory", Method(diffusion_python_memory, "matrix_pure_python_memory")),
    ("numpy", Method(diffusion_numpy_naive, "matrix_numpy_naive")),
    ("numpy+memory", Method(diffusion_numpy_memory, "matrix_numpy_memory1")),
    ("numpy+memory+laplace", Method(diffusion_numpy_memory2, "matrix_numpy_memory2")),
    ("numpy+memory+laplace+numexpr", Method(diffusion_numpy_memory2_numexpr, "matrix_numpy_numexpr")),
    ("numpy+memory+scipy", Method(diffusion_scipy, "matrix_numpy_scipy")),
    ("pytorch", Method(diffusion_pytorch_compute, "compilation-diffusion-pytorch")),
    ("pytorch+convolution", Method(diffusion_pytorch_conv, "diffusion-pytorch-conv")),
]


@cache_df_workload("_benchmark.csv")
def workload():
    sizes = (64, 256, 512, 2048, 4096, 8192)
    data = []
    for grid_width in sizes:
        print("Grid size: ", grid_width)
        for name, module in methods:
            module.grid_shape = (grid_width, grid_width)
            t, iterations = run_experiment_time_limit(
                module,
                name,
                max_iterations=5000,
                target_time=60,
                max_time=180,
                n_runs=1,
            )
            data.append({
                "method": name,
                "size": grid_width,
                "time": t,
                "iterations": iterations,
            })
        print()
    
    df = pd.DataFrame.from_records(data)
    df["speedup"] = df["size"].map(df[df["method"] == "python"].set_index("size")["time"]) / df["time"]
    return df


if __name__ == "__main__":
    df = workload()
    print(df)
    size_headers = [f"{size}x{size}" for size in set(df["size"])]

    sns.set(rc={"ytick.left": True})
    sns.set(font_scale=1.3)
    g = sns.lineplot(df.query("method != 'python'"), x='size', y='speedup', hue='method', style='method', markers=True, dashes=False, markersize=15)
    g.set_xscale('log')
    g.set_yscale('log')
    g.set_xticks(list(set(df["size"])), labels=size_headers, rotation=45, ha="right")
    g.set_title("Summary of Code Performance")
    g.set_xlabel("Grid Size")
    g.set_ylabel("Speedup over pure Python (larger is better)")
    g.set_ylim(top=50e5)
    py.tight_layout()
    py.savefig("images/_benchmark.png")


    xref_lookup = {name: method.xref for name, method in methods}
    df["xref"] = df["method"].map(lambda method: f"<<{xref_lookup[method]},{method}>>")

    df["time_1000_str"] = df.time.map(lambda t: f"{t * 1000:0.2f}s")
    table = create_table(df, xaxis="size", yaxis="xref", values="time_1000_str", headers=size_headers)
    print(table)

    df["speedup_str"] = df["speedup"].map(lambda s: f"{s:0.2f}x")
    table = create_table(df, xaxis="size", yaxis="xref", values="speedup_str", headers=size_headers)
    print(table)
