To run the text compression files you'll need a way to turn the weekly Wikipedia data dumps into a flat file of words, you should expect circa 12M words at the end of the process.

NOTE that Ian used Gensim and had to modify the source code, your mileage may vary.

# Smaller word list

A smaller list is `bigger_words_from_mword10.txt`. It is generated from https://archive.org/download/mobywordlists03201gut/mword10.zip, 
processed through https://github.com/mynameisfiber/high-performance-python-3e-code-dev/blob/main/12_less_ram/compressing_text/text_example_clean_list.py to generate all_unique_words.txt

# To process the much larger wikipedia set use

Go to via https://dumps.wikimedia.org/enwiki/20240701/ (use current date)
Look for a file like:
```2024-07-03 05:27:31 done Recombine articles, templates, media/file descriptions, and primary meta-pages.
    enwiki-20240701-pages-articles.xml.bz2 21.1 GB```

Fetch it `wget https://dumps.wikimedia.org/enwiki/20240701/enwiki-20240701-pages-articles.xml.bz2`
and I put it in /media/ian/data/wikipedia/big_set

Install gensim using the text environment, make the edits below.
Note that running the full process takes 7 hours but if you use the modified make_wiki it'll take 3 hours (it stops early after writing out the dictionary).
If you get 100_000 words,you've not made the right edits. You're looking for 12M words, mixed case.

```
pip install gensim==4.3.3 
gvim <env>/lib/python3.12/site-packages/gensim/corpora/wikicorpus.py
look for
    def __init__(
            self, fname, processes=None, lemmatize=None, dictionary=None, metadata=False,
            filter_namespaces=('0',), tokenizer_func=tokenize, article_min_tokens=ARTICLE_MIN_WORDS,
            token_min_len=TOKEN_MIN_LEN, token_max_len=TOKEN_MAX_LEN, lower=True, filter_articles=None,
        ):
and change
        if dictionary is None:
            self.dictionary = Dictionary(self.get_texts())
        else:
            self.dictionary = dictionary
to
        if dictionary is None:
            prune_at = 500_000_000
            print("Pruning at ", prune_at, " via WikiCorpus")
            self.dictionary = Dictionary(self.get_texts(), prune_at=prune_at)
        else:
            self.dictionary = dictionary

...
Change in make_wiki.py
        #wiki = WikiCorpus(inp)  
        wiki = WikiCorpus(inp, lower=False)  # need to remove lowercase
        #wiki.dictionary.filter_extremes(no_below=20, no_above=0.1, keep_n=DEFAULT_DICT_SIZE)
        wiki.dictionary.filter_extremes(no_below=0, no_above=1, keep_n=keep_words) # 0 else it'll discard 6M+ low-freq, no_above 100% to keep all frequent
```

This will generate a folder like `enwiki4_nocutoff_0min` which you can pass to `python text_example_clean_list_wikipedia_gensim.py` to generate the `all_unique_words_wikipedia_via_gensim.txt` file.

Run using:

```
nice python -m gensim.scripts.make_wiki enwiki-20240320-pages-articles.xml.bz2  enwiki4_nocutoff_0min/  500000000 
```

