import pandas as pd
import seaborn as sns
import matplotlib.pyplot as py

import norm_array
import norm_numpy
import norm_numpy_dot
import norm_python
import norm_python_comprehension

methods = [
    ("norm_array", norm_array),
    ("norm_python", norm_python),
    ("norm_python_comprehension", norm_python_comprehension),
    ("norm_numpy", norm_numpy),
    ("norm_numpy_dot", norm_numpy_dot),
]


if __name__ == "__main__":
    N = 50
    data = []
    for e in range(7, 21):  # 21
        size = int(2**e)
        print(e, size)
        for name, method in methods:
            print(name)
            t = method.run_experiment(size, num_iter=N)/N
            data.append({
                "method": name,
                "size": size,
                "time": t * 1000,
            })
    df = pd.DataFrame.from_records(data)
    print(df)

    sns.set(rc={"ytick.left": True})
    sns.set(font_scale=1.5)
    g = sns.lineplot(df, x='size', y='time', hue='method', style='method', markers=True, dashes=False, markersize=15)
    g.set_xscale('log')
    g.set_yscale('log')
    g.set_xticks(
        list(set(df["size"])),
        rotation=-45,
        labels=[f"{size:,}" for size in set(df["size"])],
    )
    g.set_title("Runtime for various norm squared routines")
    g.set_xlabel("Vector Length")
    g.set_ylabel("Runtime (milliseconds, less is better)")
    py.tight_layout()
    py.savefig("images/figure_compare_norms.png")
