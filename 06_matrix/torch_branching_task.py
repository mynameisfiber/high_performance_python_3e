import torch
import timeit


def task(A, target):
    """
    Given an int array of length N with values from (0, N] and a target value,
    iterates through the array, using the current value to find the next array
    item to look at, until we have seen a total value of at least `target`.
    Returns how many iterations until the value was reached.
    """
    result = 0
    i = 0
    N = 0
    while result < target:
        result += A[i]
        i = A[i]
        N += 1
    return N


if __name__ == "__main__":
    N = 1000

    A_py = (torch.rand(N) * N).type(torch.int).to("cuda:0")
    A_np = A_py.cpu().numpy()

    task(A_py, 500)
    task(A_np, 500)

    gpu_time = timeit.repeat(
        "task(A_py, 500)",
        setup="from __main__ import task, A_py",
        repeat=3,
        number=1_000_000,
    )

    cpu_time = timeit.repeat(
        "task(A_np, 500)",
        setup="from __main__ import task, A_np",
        repeat=3,
        number=1_000_000,
    )

    print(f"Min time using the GPU: {min(gpu_time)}")
    print(f"Min time using the CPU: {min(cpu_time)}")
