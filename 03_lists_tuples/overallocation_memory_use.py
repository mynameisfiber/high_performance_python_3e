import sys
import random


def total_size(obj):
    """
    Recursively calculates the total size of a Python object in memory,
    including its contents.

    Args:
        obj: The Python object whose size is to be calculated.

    Returns:
        int: The total size of the object in bytes.

    Notes:
        This function recursively traverses the object and its contents to
        compute the total size in memory.

    Raises:
        None
    """
    children = 0
    try:
        children = sum(total_size(item) for item in obj)
    except TypeError:
        pass
    return sys.getsizeof(obj) + children


def sample_comp(a, b, N):
    return [random.randint(a, b) for _ in range(N)]


def sample_list(a, b, N):
    return list([random.randint(a, b) for _ in range(N)])


def sample_tuple(a, b, N):
    return tuple([random.randint(a, b) for _ in range(N)])


N_samples = 1_000_000
sample_size = 9
print(f"Creating {N_samples:,d} samples of {sample_size} items each")

data_comp = [sample_comp(0, 100, sample_size) for _ in range(N_samples)]
size_comp = max_size = total_size(data_comp) / 1e6
print(f"Data Comprehension size: {size_comp:0.2f} Mb")

data_list = [sample_list(0, 100, sample_size) for _ in range(N_samples)]
size_list = total_size(data_list) / 1e6
print(f"Data List size: {size_list:0.2f} Mb ({max_size/size_list:0.2f}x smaller)")

data_tuple = [sample_tuple(0, 100, sample_size) for _ in range(N_samples)]
size_tuple = total_size(data_tuple) / 1e6
print(f"Data Tuple size: {size_tuple:0.2f} Mb ({max_size/size_tuple:0.2f}x smaller)")
