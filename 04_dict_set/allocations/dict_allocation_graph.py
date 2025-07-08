import pylab as py
import numpy as np

py.rcParams.update({"font.size": 16})


def create_data(N):
    prev = 0
    items = {}
    data = [(0, items.allocated())]
    for i in range(N):
        items[i] = i
        if items.allocated() != prev:
            print(len(items), items.allocated())
            data.append((len(items) - 1, prev))
            data.append((len(items), items.allocated()))
            prev = items.allocated()
    data.append((len(items), items.allocated()))
    return np.asarray(data)


def plot_data(data):
    fig = py.figure()
    py.plot(data[:, 0], data[:, 1] - data[:, 0], color="navy")
    """
    for i in range(0, data.shape[0] - 1, 2):
        py.plot(
            data[i : i + 2, 0], data[i : i + 2, 1] - data[i : i + 2, 0], color="navy"
        )
    """
    py.xlabel("Number of items in the dict")
    py.ylabel("Number of elements overallocated")
    py.title("Overallocation in dicts")
    return fig


if __name__ == "__main__":
    data = create_data(210_000)
    fig = plot_data(data)
    fig.savefig("dict_overallocation.png")
