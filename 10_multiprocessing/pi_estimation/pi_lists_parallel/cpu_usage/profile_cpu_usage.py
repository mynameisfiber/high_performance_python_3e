import time
import numpy as np
import psutil
from matplotlib import pyplot as plt
import subprocess
import argparse
import pickle


SHRINK = 1  # fraction to shrink colorbar by if it overextends

# generate the data
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('--build', action="store_true", default=False, help='required positional argument')
    parser.add_argument('--processes', action="store_true", default=False, help='required positional argument')
    parser.add_argument('--nbr_processes', default=1, type=int, help='required positional argument')
    args = parser.parse_args()

    xargs = ["python", "../pi_lists_parallel.py"]
    xargs.append(str(args.nbr_processes))
    xargs.append("--nbr_samples_in_total")
    xargs.append("400000000")    
    if args.processes:
        xargs.append("--processes")
    else:
        print("THREADED VERSION")

    SLEEP_FOR = 2
    MAX_TIME = 80

    print("Using:", xargs)

    ROOT_NAME = "09_" + "_".join(s.replace("-", "").replace(".", "_").replace("=", "_").replace("/", "_") for s in xargs[1:])
    print(ROOT_NAME)
    PICKLE_NAME = ROOT_NAME + ".pickle"
    FIG_NAME = ROOT_NAME + ".png"

    if args.build:

        sts = subprocess.Popen(xargs)
        t = 0
        time_labels = []
        time.sleep(0.2) # pause right at the start briefly

        while True:
            # [27.3, 90.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            percents_now = psutil.cpu_percent(percpu=True)
            percents_now.sort(reverse=True)
            if t == 0:
                percents = np.array([percents_now])  # , dtype=np.float_)
            else:
                percents = np.append(percents, [percents_now], axis=0)

            time_labels.append(t)
            #print(time_labels, percents) # IAN

            # break when workers are finished
            time.sleep(SLEEP_FOR)
            if sts.poll() is not None:
                break
            t += SLEEP_FOR

        pickle.dump((percents, time_labels), open(PICKLE_NAME, 'wb'))
    else:
        # generate the plots
        (percents, time_labels_stored) = pickle.load(open(PICKLE_NAME, 'rb'))
        print(f"{percents.shape} {percents=}")

        time_labels = time_labels_stored
        #breakpoint()

        # jump every n for slower (few-core) runs to keep to circa 10 columns
        jump_every = max(1, round(percents.shape[0] / 10))        
        #jump_every = 1
        print(f"Jumping every {jump_every} of a total of {percents.shape[0]} percents")

        # specific to each plot?
        
        time_labels = time_labels[::jump_every]
        percents = percents[::jump_every]

        f = plt.figure(figsize=(8, 8))

        # cmap='hot' looks lovely on color screens
        plt.imshow(percents.T, interpolation='nearest', cmap='binary', origin='lower')
        plt.xlabel('Time (seconds)')
        plt.ylabel('CPU (8 cores and 8 HyperThreads)')
        plt.title(f"Under {max(time_labels)+SLEEP_FOR} seconds of execution time")
        plt.clim(0, 100)  # max sure we plot 0..100% even if cpu doesn't get to 100% usage

        y_ticks_labels = np.arange(1, 18)
        y_ticks_labels = [str(v) for v in np.arange(1, 18)]
        y_ticks_labels[-1] = ""
        plt.yticks(np.arange(-0.5, 16.5), y_ticks_labels)

        time_labels_str = [str(t) for t in time_labels]
        print(f"{time_labels_str=}")
        print(f"{percents=}")
        plt.xticks(np.arange(0, len(percents)), time_labels_str)
        plt.xlim(xmin=0)

        cb = plt.colorbar(shrink=SHRINK)
        cb.set_label("CPU %")

        plt.draw()
        plt.tight_layout()
        print(f"Writing {FIG_NAME}")
        plt.savefig(FIG_NAME)
