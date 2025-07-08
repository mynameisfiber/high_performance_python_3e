"""
Readers of the 2nd edition of High Performance Python will remember a
discussion about namespaces and how they relate to dictionary lookups.
This is no longer the case in Python 3.12, however this example code is
still included to help readers benchmark the code themselves and
understand how to experiment with python functionality.
"""

import math
from math import sin


def test1(x):
    """
    # PYTHON 3.7 RESULTS
    >>> %timeit test1(123_456)
    162 µs ± 3.82 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    """
    res = 1
    for _ in range(1000):
        res += math.sin(x)
    return res


def test2(x):
    """
    # PYTHON 3.7 RESULTS
    >>> %timeit test2(123_456)
    124 µs ± 6.77 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    """
    res = 1
    for _ in range(1000):
        res += sin(x)
    return res


def test3(x, sin=math.sin):
    """
    # PYTHON 3.7 RESULTS
    >>> %timeit test3(123_456)
    105 µs ± 3.35 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    """
    res = 1
    for _ in range(1000):
        res += sin(x)
    return res
