import torch
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as py

import diffusion_pytorch_compute
import diffusion_pytorch_conv

from _utils import iter_sizes_2ph, plot_add_speedup, cache_df_workload


@cache_df_workload("figure_pytorch_naive_vs_conv.csv")
def workload():
    N = 2500
    torch.set_default_dtype(torch.float32)
    data = []
    for size in iter_sizes_2ph(9, 14):
        print(f"Grid Shape: {size}")
        diffusion_pytorch_compute.grid_shape = (size, size)
        diffusion_pytorch_conv.grid_shape = (size, size)
        data.append({
            "size": size,
            "method": "Naive PyTorch",
            "time": diffusion_pytorch_compute.run_experiment(N) / N
        })
        data.append({
            "size": size,
            "method": "PyTorch Convolutions",
            "time": diffusion_pytorch_conv.run_experiment(N) / N
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
    g.set_xscale('log')
    g.set_xticks(sizes, rotation=45, labels=size_headers, ha='right')
    g.set_title("Time per iteration for naive PyTorch vs Convolutions")
    g.set_xlabel("Grid Size")
    g.set_ylabel("Time per Iteration (s)")

    py.tight_layout()
    py.savefig("images/pytorch_naive_vs_conv.png")
