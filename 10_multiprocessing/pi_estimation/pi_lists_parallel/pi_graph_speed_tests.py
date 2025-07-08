"""Graph execution time for serial, threaded and processes forms of Pi estimation with lists"""
import numpy as np
import matplotlib.pyplot as plt

# timings generated using
#  pi_lists_series, pi_lists_parallel 1 2 4 8, pi_lists_parallel --processes 1 2 4 8
speeds = [[190],
                   [191, 192, 193, 193, 193], # note tweaked these down a bit
                   [189, 95, 47, 24, 24]]

nbr_cores = [[1],
                      [1, 2, 4, 8, 16],
                      [1, 2, 4, 8, 16]]

labels = np.array(["Serial", "Threads", "Processes"])

plt.figure(1, figsize=(8, 6))
plt.clf()
markers = ['-.o', ':x', '-x']
for nc, sp, label, mk in zip(nbr_cores, speeds, labels, markers):
    plt.plot(nc, sp, mk, label=label, linewidth=2, markersize=10)
plt.annotate("Serial and Threads have similar execution time", (2, speeds[0][0]-5) )

plt.annotate('Serial execution only runs once on one core',
             xy=(1, speeds[0][0]),      # The point being annotated
             xytext=(1+1, speeds[0][0]-20),  # Position of the annotation text
             arrowprops=dict(facecolor='black', shrink=0.05))  # Arrow properties


plt.legend(loc="lower left", framealpha=0.8)
plt.ylim(0, 210)
plt.xlim(0.5, 16.5)
plt.ylabel("Execution time (seconds) - smaller is better")
plt.xlabel("Number of workers")
plt.title("Time to estimate Pi using objects with 400,000,000\ndart throws in series, threaded and with processes")
#plt.grid()
#plt.show()
plt.tight_layout()
plt.savefig("09_pi_lists_graph_speed_tests_threaded_processes.png")
