import time
import timeit
import text_example
import memory_profiler
import marisa_trie
import argparse
from text_example import MARISA_TRIE_FILENAME

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

    word_to_check = text_example.WE_EXPECT_TO_SEE_2

    print("RAM before loading from disk {:0.1f}MiB".format(memory_profiler.memory_usage()[0]))
    t2 = time.time()
    d = marisa_trie.Trie()
    with open(MARISA_TRIE_FILENAME, 'rb') as f:
        words_trie2 = d.read(f)
    t3 = time.time()
    #os.remove(MARISA_TRIE_FILENAME)
    print("RAM after loading trie from disk {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t3 - t2))
    print("The trie contains {} words".format(len(words_trie2)))
    print(f"time to load {t3-t2:f}s")
    stmt=f"'{word_to_check}' in words_trie2"
    exec("assert " + stmt)
    time_cost = sum(timeit.repeat(stmt=stmt,
                                  setup="from __main__ import words_trie2",
                                  number=1,
                                  repeat=text_example.NUMBER_LOOKUPS))
    print("Summed time to lookup word {:0.4f}s".format(time_cost))
