High Performance Python 3e: The Code
=================================

This repository contains the code from ["High Performance
Python 3e"](https://www.oreilly.com/library/view/high-performance-python/9781098165956/) by Micha Gorelick
and Ian Ozsvald with O'Reilly Media.  Each directory contains the examples from
the chapter in addition to other interesting code on the subject.

You can find out more about the authors here:

* https://github.com/mynameisfiber
* http://micha.codes/
* https://github.com/ianozsvald/
* https://ianozsvald.com/
  * Ian's twice-a-month newsletter contains Higher Performance and Data Science tips: https://ianozsvald.com/data-science-jobs/
  * Ian runs a training course on Higher Performance - see https://ianozsvald.com/training/
* https://twitter.com/ianozsvald

Errata
------

Errata can be filed here https://www.oreilly.com/catalog/errata.csp?isbn=0790145478603 (no login required, just a form with a few details) or file a bug on this repo, whatever's easiest.


Running the Code
----------------

Each chapter directory has an included `requirements.txt` file that contains all the required external modules for that chapter. With python3.12 enabled, go into the directory and run `pip install -r requirements.txt` then use the included code to help you follow along with the book!


Topics Covered
--------------

This book ranges in topic from native Python to external modules to writing your
own modules.  Code is shown to run on one CPU, multiple coroutines, multiple
CPU's and multiple computers.  In addition, throughout this exploration a focus
is kept on keeping development time fast and learning from profiling output in
order to direct optimizations.

The following topics are covered in the code repo:


- Chapter 1: Understanding Performant Programming
    * What are the elements of a computer's architecture?
    * What are some common alternate computer architectures?
    * How does Python abstract the underlying computer architecture?
    * What are some of the hurdles to making performant Python code?
    * What strategies can help you become a highly performant programmer?

- Chapter 2: Profiling
    * How can I identify speed and RAM bottlenecks in my code?
    * How do I profile CPU and memory usage?
    * What depth of profiling should I use?
    * How can I profile a long-running application?
    * What's happening under the hood with CPython?
    * How do I keep my code correct while tuning performance?

- Chapter 3: Lists and Tuples
    * What are lists and tuples good for?
    * What is the complexity of a lookup in a list/tuple?
    * How is that complexity achieved?
    * What are the differences between lists and tuples?
    * How does appending to a list work?
    * When should I use lists and tuples?

- Chapter 4: Dictionaries and Sets
    * What are dictionaries and sets good for?
    * How are dictionaries and sets the same?
    * What is the overhead when using a dictionary?
    * How can I optimize the performance of a dictionary?
    * How does Python use dictionaries to keep track of namespaces?

- Chapter 5: Iterators
    * How do generators save memory?
    * When is the best time to use a generator?
    * How can I use +itertools+ to create complex generator workflows?
    * When is lazy evaluation beneficial, and when is it not?

- Chapter 6: Matrix and Vector Computation
    * What are the bottlenecks in vector calculations?
    * What tools can I use to see how efficiently the CPU is doing my calculations?
    * Why is `numpy` better at numerical calculations than pure Python?
    * What are ++cache-misses++ and ++page-faults++?
    * How can I track the memory allocations in my code?
    * How can I use a GPU to speed up my computation?
    * What are the subtleties when using GPUs for numerical code or deep learning?

- Chapter 7: Pandas
    * What's the fastest way to apply a function to a Pandas DataFrame?
    * What's the quickest way to build a DataFrame from partial results?
    * Can we use Numba to compile for more performance inside Pandas?
    * Can Dask be used for distributed CPU computation?
    * How can Polars execute similar queries faster than Pandas?
    * How can I parallelize Pandas using Dask and Swifter?

- Chapter 8: Compiling to C
    * How can I have my Python code run as lower-level code?
    * What is the difference between a JIT compiler and an AOT compiler?
    * What tasks can compiled Python code perform faster than native Python?
    * Why do type annotations speed up compiled Python code?
    * How can I write modules for Python using C or Fortran?
    * How can I use libraries from C or Fortran in Python?

- Chapter 9: Asynchronous I/O
    * What is concurrency, and how is it helpful?
    * What is the difference between concurrency and parallelism?
    * Which tasks can be done concurrently, and which can't?
    * What are the various paradigms for concurrency?
    * When is the right time to take advantage of concurrency?
    * How can concurrency speed up my programs?

- Chapter 10: Multiprocessing
    * What does the ++multiprocessing++ module offer?
    * What's the difference between processes and threads?
    * How do I choose the right size for a process pool?
    * How do I use nonpersistent queues for work processing?
    * What are the costs and benefits of interprocess communication?
    * How can I process ++numpy++ data with many CPUs?
    * How would I use Joblib to simplify parallelized and cached scientific work?
    * Why do I need locking to avoid data loss?

- Chapter 11: Clusters and Job Queues
    * Why are clusters useful?
    * What are the costs of clustering?
    * How can I convert a ++multiprocessing++ solution into a clustered solution?
    * How does an IPython cluster work?
    * What considerations should I take when picking a messaging platform?

- Chapter 12: Using Less Ram
    * Why should I use less RAM?
    * Why are `numpy` and `array` better for storing lots of numbers?
    * How can lots of text be efficiently stored in RAM?
    * How could I count (approximately!) to latexmath:[$10^{76}$] using just 1 byte?
    * What are Bloom filters, and why might I need them?

- Chapter 13: Lessons from the Field (no code)
    * Some stories from the field on performance python


Using the code base
-------------------

This code base is a live document and should be freely commented on and used.
It is distributed with a license that amounts to: don't use the code for
profit, however read the [provided license](LICENSE.md) file for the
law-jargon.  Feel free to share, fork and comment on the code!

If any errors are found, or you have a bone to pick with how we go about doing
things, leave an issue on this repo!  Just keep in mind that all code was
written for educational purposes and sometimes this means favouring readability
over "the right thing" (although in Python these two things are generally one
and the same!).

