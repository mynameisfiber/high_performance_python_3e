from pprint import pprint
from itertools import cycle

import torch
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as py

import diffusion_pytorch_compute
import diffusion_pytorch_conv
from _utils import cache_df_workload


@cache_df_workload("figure_pytorch_naive_precision.csv")
def workload():
    precisions = ["float64", "float32", "float16"]
    N = 2500
    data = []
    for p in range(9, 14):
        size = (1<<p)
        print(f"Grid Shape: {size}")
        diffusion_pytorch_compute.grid_shape = (size, size)
        for precision in precisions:
            print(f"Precision: {precision}")
            torch.set_default_dtype(getattr(torch, precision))
            t = diffusion_pytorch_compute.run_experiment(N) / N
            data.append({
                "size": size,
                "precision": precision,
                "time": t,
            })
    return pd.DataFrame.from_records(data)



if __name__ == "__main__":
    df = workload()
    print(df)

    sns.set(font_scale=1.5)
    g = sns.barplot(df, x='size', y='time', hue='precision')
    g.set_yscale('log')
    g.set_title("Time per iteration for PyTorch Float Precisions")
    g.set_xlabel("Grid Size")
    g.set_ylabel("Time per Iteration (s)")
    for container in g.containers:
        g.bar_label(container, fmt=lambda v: f"{v:0.1e}".replace("e-0", "e-"), fontsize=12)

    # Define hatch patterns
    hatch_patterns = ['///', '\\\\\\', '---', '|||', '+', 'x', 'o', 'O', '.', '*']
    
    # Apply hatch patterns manually
    for bars, hatch in zip(g.containers, hatch_patterns[:len(g.containers)]):
        for bar in bars:
            bar.set_hatch(hatch)
    
    # Customize the legend to show hatching
    legend_labels = [t.get_text() for t in g.get_legend().texts]
    handles = g.get_legend().legend_handles
    for handle, hatch in zip(handles, hatch_patterns[:len(handles)]):
        handle.set_hatch(hatch)
    
    g.legend(handles=handles, labels=legend_labels, title="Precision")

    py.tight_layout()
    py.savefig("images/pytorch_float_precision.png")
