import sys
import argparse
import time
import timeit
import text_example
import memory_profiler


__version__ = "3.0"

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

    # load the words directly into the set
    t1 = time.time()
    words_set = set(readers)
    t2 = time.time()
    print("RAM after creating set {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t2 - t1))
    print("The set contains {} words".format(len(words_set)))

    word_to_check = text_example.WE_EXPECT_TO_SEE_2
    assert word_to_check in words_set
    stmt=f"'{word_to_check}' in words_set"
    exec("assert " + stmt)
    print(f"Checking that we'll see {word_to_check} in our words container")
    time_cost = sum(timeit.repeat(stmt="u'{word_to_check}' in words_set",
                                  setup="from __main__ import words_set",
                                  number=1,
                                  repeat=text_example.NUMBER_LOOKUPS))
    print("Summed time to lookup word {:0.4f}s".format(time_cost))
