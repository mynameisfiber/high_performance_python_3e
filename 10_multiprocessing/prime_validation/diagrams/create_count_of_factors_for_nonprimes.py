import argparse
import math
import multiprocessing
import pickle
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib as mpl


def check_prime(n):
    if n % 100000 == 0:
        print(n)
    if n % 2 == 0:
        return False, 2
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False, i
    return True, None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('--create_data', action="store_true", default=False, help='if present then calculate data, if absent then plot')
    args = parser.parse_args()

    filename = "primes_validation_count_of_factors.pickle".format()
    png_filename = "primes_validation_count_of_factors.png".format()

    if args.create_data:
        upper_bound = 10000000
        number_range = range(3, upper_bound)
        NBR_PROCESSES = 4
        pool = multiprocessing.Pool(processes=NBR_PROCESSES)
        are_primes = pool.map(check_prime, number_range)
        c = Counter()
        for is_prime, factor in are_primes:
            if not is_prime:
                c.update([factor])
        #for n in number_range:
            #is_prime, factor = check_prime(n)
            #if not is_prime:
                #c.update([factor])
        PICKLED_DATA = (upper_bound, c)
        pickle.dump(PICKLED_DATA, open(filename, 'wb'))
    else:
        (upper_bound, c) = pickle.load(open(filename, "rb"))
        # make a figure, show the experimental timings
        f = plt.figure(1)
        plt.barh(list(c.keys()), list(c.values()), log=True, height=5)
        title = "Frequency of {:,} non-prime factors up to {:,}".format(len(c), upper_bound)
        title += "\nMost common factors: 2, 3, 5, 7, ..."
        plt.title(title)
        plt.ylabel("Factor for non-prime")
        plt.xlabel("Frequency of factor (log scale)")
        plt.ylim(ymin=-40, ymax=max(c.keys()) + 40)
        plt.xlim(xmin=1, xmax=c[2] + 1_000_000)

        ax = plt.gca()
        ax.grid(b=True, which='both', axis='x')
        ax.get_xaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        
        plt.tight_layout()
        plt.savefig(png_filename)
        print(png_filename)
        #plt.show()
