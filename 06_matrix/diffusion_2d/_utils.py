import pandas as pd

def run_experiment_time_limit(experiment, label=None, iterations=None, max_iterations=None, target_time=60, max_time=120, n_runs=3):
    iterations_tot = 0
    if not iterations:
        iterations_tot += 5
        t_one = experiment.run_experiment(5) / 5
        if t_one > max_time:
            return 0, 0
            raise RuntimeError("One iteration too slow")
        iterations = max(1, int(target_time // t_one))
        if max_iterations:
            iterations = min(iterations, max_iterations)
    t_per_its = []
    t_tot = 0
    for _ in range(n_runs):
        t = experiment.run_experiment(iterations)
        iterations_tot += iterations
        t_tot += t
        t_per_its.append(t / iterations)
        if t / iterations > max_time:
            return 0, 0
        iterations = max(1, int(target_time * iterations / t))
        if max_iterations:
            iterations = min(iterations, max_iterations)
    t_per_it = min(t_per_its)

    if label:
        print(f"\t{label}: {t_tot:0.2f}s, {t_per_it:0.6f}s/it, {iterations}it")
    return t_per_it, iterations


def iter_sizes_2ph(low, high):
    for p in range(low, high):
        for phalf in (0, 1):
            yield (1<<p) + phalf * (1 << (p-1))


def plot_add_speedup(df, g, y="time", offset=0.01):
    dy = df[y].max() * offset
    for item in df.itertuples():
        if item.speedup > 1:
            g.axes.text(item.size, getattr(item, y) + dy, f'{item.speedup:0.1f}x')

def create_table(df, xaxis, yaxis, values, **kwargs):
    return (
        df
        .pivot_table(columns=xaxis, values=values, index=yaxis, sort=False, aggfunc=lambda x: x)
        .to_markdown(
            tablefmt="asciidoc",
            **kwargs
        )
    )


def cache_df_workload(filename):
    def _(fxn):
        def __(*args, **kwargs):
            try:
                df = pd.read_csv(filename).reset_index()
                print("Loaded from cache")
            except Exception as e:
                print(f"Recalculating {filename}: {e}")
                df = fxn(*args, **kwargs)
                df.to_csv(filename, index=False)
            return df
        return __
    return _
