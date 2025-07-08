import os
import sys
import argparse
import time
import timeit
import text_example
import memory_profiler
import pickle
import pygtrie

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
    # avoid building a temporary list of words in Python, store directly in the
    # Trie
    #trie = pygtrie.Trie({k:1})
    words_trie = pygtrie.Trie()
    t1 = time.time()
    for word in readers:
        words_trie[word]=1
    t2 = time.time()
    print("RAM after creating trie {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t2 - t1))
    print("The trie contains {} words".format(len(words_trie)))
    
    word_to_check = text_example.WE_EXPECT_TO_SEE_2
    assert word_to_check in words_trie
    print(f"Checking that we'll see {word_to_check} in our words container")
    stmt=f"'{word_to_check}' in words_trie"
    exec("assert " + stmt)
    time_cost = sum(timeit.repeat(stmt=stmt,
                                  setup="from __main__ import words_trie",
                                  number=1,
                                  repeat=text_example.NUMBER_LOOKUPS))

    print("Summed time to lookup word {:0.4f}s".format(time_cost))

    t1 = time.time()
    TRIE_FILENAME = 'words_trie.saved'
    print(f"Writing to {TRIE_FILENAME}, then will read back")
    with open(TRIE_FILENAME, 'wb') as f:
        pickle.dump(words_trie, f)
    del words_trie
    print("RAM before loading from disk {:0.1f}MiB".format(memory_profiler.memory_usage()[0]))
    t2 = time.time()
    #d = marisa_trie.Trie()
    with open(TRIE_FILENAME, 'rb') as f:
        words_trie2 = pickle.load(f)
    t3 = time.time()
    os.remove(TRIE_FILENAME)
    print("RAM after loading trie from disk {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t2 - t1))
    print("The trie contains {} words".format(len(words_trie2)))
    print(f"time to save {t2 - t1:f}s, time to load {t3-t2:f}s")
    stmt=f"'{word_to_check}' in words_trie2"
    exec(stmt)
    time_cost = sum(timeit.repeat(stmt=stmt,
                                  setup="from __main__ import words_trie2",
                                  number=1,
                                  repeat=text_example.NUMBER_LOOKUPS))
    print("Summed time to lookup word {:0.4f}s".format(time_cost))
    
