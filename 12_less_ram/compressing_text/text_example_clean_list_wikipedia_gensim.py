import gensim
#FILENAME = "/home/ian/workspace/personal_projects/high_performance_python_book_2e/high-performance-python-2e/examples_ian/ian/12_lessram/compressing_text/wikipedia_dump/enwiki_11M/_wordids.txt.bz2"
#FILENAME = "/media/ian/data/wikipedia/enwiki4/_wordids.txt.bz2" # small set of words, 53k words
#FILENAME = "/media/ian/data/wikipedia/big_set/enwiki4/_wordids.txt.bz2" # big set of words, 100k words
#FILENAME = "/media/ian/data/wikipedia/big_set/enwiki4_nocutoff_nomin/_wordids.txt.bz2" # big set of words, 4.7M words
FILENAME = "/media/ian/data/wikipedia/big_set/enwiki4_nocutoff_0min/_wordids.txt.bz2" # big set of words, 11M words

print(f"Reading input from: {FILENAME}")

id2word = gensim.corpora.Dictionary.load_from_text(FILENAME) 
#print(len([w for w in iter(id2word.values())]))
print(len(id2word))

SUMMARISED_FILE = "all_unique_words_wikipedia_via_gensim.txt"

print("Summarising input files into one output set of {} words".format(len(id2word)))
with open(SUMMARISED_FILE, 'w') as f:
    for word in id2word.values():
        f.write(word + "\n")
print(f"Wrote to {SUMMARISED_FILE}")



