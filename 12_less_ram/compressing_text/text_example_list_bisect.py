import sys
import argparse
import time
import timeit
import text_example
import memory_profiler
import bisect

__version__ = "3.0"


def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__) # read __doc__ attribute
    parser.add_argument('-i', '--input_filename', type=str, nargs="?",
                        help='csv from someone'
                        ' (default: %(default)s))', # help msg 2 over lines with default
                        default=text_example.DEFAULT_INPUT_FILE)
    parser.add_argument('-v', '--version', action="store_true",
                        help="show version")

    args = parser.parse_args()
    print("Arguments provided:", args)
    if args.version:
        print(f"Version: {__version__}")
        sys.exit()

    print(f"Reading from {args.input_filename}")
    readers = text_example.read_words(args.input_filename)

    print("RAM at start {:0.1f}MiB".format(memory_profiler.memory_usage()[0]))
    t1 = time.time()
    words = [w for w in readers]
    print("Loading {} words".format(len(words)))
    t2 = time.time()
    print("RAM after creating list {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t2 - t1))
    print("The list contains {} words".format(len(words)))
    words.sort()
    t3 = time.time()
    print("Sorting list took {:0.1f}s".format(t3 - t2))

    word_to_check = text_example.WE_EXPECT_TO_SEE_2
    assert word_to_check in words
    word_loc = index(words, word_to_check)

    stmt=f"index(words, '{word_to_check}')"
    exec("assert " + stmt)
    print(f"Checking that we'll see {word_to_check} in our words container")
    print(f"{word_to_check} found at location {word_loc}")
    time_cost = sum(timeit.repeat(stmt=stmt,
                                  setup="from __main__ import words, word_to_check, index",
                                  number=1,
                                  repeat=text_example.NUMBER_LOOKUPS))
    print("Summed time to lookup word {:0.4f}s".format(time_cost))
