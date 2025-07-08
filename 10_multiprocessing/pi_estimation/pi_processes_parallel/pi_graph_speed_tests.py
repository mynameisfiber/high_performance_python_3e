"""Graph execution time for serial, threaded and processes forms of Pi estimation with numpy"""
import numpy as np
import matplotlib.pyplot as plt

# timings generated using
# pi_numpy_serial_blocks.py
# (serial.py - same as serial blocks but for 1 large array only)
# pi_numpy_parallel_worker.py
speeds = [[11.1],
                   [11.1, 9.6, 9.0, 8.3, 8.2], # slight massage
                   [11.1, 5.6, 3.2, 2.3, 2.3]]

nbr_cores = [[1],
                      [1, 2, 4, 8, 16],
                      [1, 2, 4, 8, 16]]

labels = np.array(["Serial", "Threads", "Processes"])

plt.figure(1, figsize=(8, 6))
plt.clf()
markers = ['-.o', ':x', '-x']
for nc, sp, label, mk in zip(nbr_cores, speeds, labels, markers):
    plt.plot(nc, sp, mk, label=label, linewidth=2, markersize=10)

plt.annotate('Serial execution only runs once on one core',
             xy=(1, speeds[0][0]),      # The point being annotated
             xytext=(1+1, speeds[0][0]-0.5),  # Position of the annotation text
             arrowprops=dict(facecolor='black', shrink=0.05))  # Arrow properties


plt.legend(loc="lower left", framealpha=0.8)
plt.ylim(0, 12)
plt.xlim(0.5, 16.5)
plt.ylabel("Execution time (seconds) - smaller is better")
plt.xlabel("Number of workers")
plt.title("Time to estimate Pi using numpy with 400,000,000\ndart throws in series, threaded and with processes")
#plt.grid()
#plt.show()
plt.tight_layout()
plt.savefig("09_pi_numpy_graph_speed_tests_threaded_processes.png")
