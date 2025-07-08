import codecs

# "Moby Words lists by Grady Ward"
# http://www.gutenberg.org/ebooks/3201
#SUMMARISED_FILE = "all_unique_words.txt"  # 500k approx
#CODEC = 'Windows-1252'

#CODEC = 'utf-8'
#SUMMARISED_FILE = "all_unique_words_wikipedia_via_gensim.txt"
DEFAULT_INPUT_FILE = "trivial_words.txt" 
DEFAULT_INPUT_FILE = "bigger_words_from_mword10.txt" # circa 354k rows of words
DEFAULT_INPUT_FILE = "all_unique_words_wikipedia_via_gensim.txt" # 4.7M words

WE_EXPECT_TO_SEE_1 = "and" # we should see this in the input files
#WE_EXPECT_TO_SEE_2 = "spaniel" # from 4.7M wp corpus, circa position 3.3M of 4.7M rows
WE_EXPECT_TO_SEE_2 = "Zweibel" # from 11M wp corpus 
MARISA_TRIE_FILENAME = 'words_trie.saved'

NUMBER_LOOKUPS = 100_000

#assert 'Zwiebel' in words

def read_words(filename, codec="utf-8"):
    # return words from filename using a generator
    try:
        with codecs.open(filename, 'r', codec) as f:
            for line_nbr, line in enumerate(f):
                items = line.strip().split()
                for item in items:
                    yield item
    except UnicodeDecodeError:
        print("UnicodeDecodeError for {} near line {} and word {}".format(filename, line_nbr, line))

#readers = read_words(SUMMARISED_FILE)
