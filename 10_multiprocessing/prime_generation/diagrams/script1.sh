python primes_pool_plot_chunksizetimes.py 1 --create_data
python primes_pool_plot_chunksizetimes.py 1  # will generate the plot
#09_primes_pool_plot_chunksizetimes_1to50000_plottype1.png
cp 09_primes_pool_plot_chunksizetimes_1to50000_plottype1.png ../../../../images/hpp_0911.png

python primes_pool_plot_chunksizetimes.py 2 --create_data
python primes_pool_plot_chunksizetimes.py 2  # will generate the plot
#09_primes_pool_plot_chunksizetimes_1to50000_plottype2.png 
cp 09_primes_pool_plot_chunksizetimes_1to50000_plottype2.png ../../../../images/hpp_0910.png

python primes_pool_plot_chunksizetimes.py 1 --create_data --shuffle
python primes_pool_plot_chunksizetimes.py 1 --shuffle # will generate the plot
#09_primes_pool_plot_chunksizetimes_1to50000_shuffled_plottype1.png
cp 09_primes_pool_plot_chunksizetimes_1to50000_shuffled_plottype1.png ../../../../images/hpp_0912.png

python primes_pool_plot_chunksizetimes_by_nbrchunks.py --create_data --shuffle
python primes_pool_plot_chunksizetimes_by_nbrchunks.py --shuffle
#09_primes_pool_plot_chunksizetimes_by_nbrchunks_sawtoothpattern_shuffled.png
cp 09_primes_pool_plot_chunksizetimes_by_nbrchunks_sawtoothpattern_shuffled.png ../../../../images/hpp_0913.png