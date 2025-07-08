from matplotlib import pyplot as plt


plt.figure(figsize=(8, 6))

# primes_queue.py on job C
xs = [1, 2, 4, 8]
ys = [69, 72, 86, 91]
#ys = [97, 97, 109, 111] #2nd ed

#plt.scatter(xs, ys, marker='x')
plt.plot(xs, ys, '--x', label="Using Queues", markersize=10)
plt.annotate("1 child process via Queues", (xs[0], ys[0]-5))

# primes_queue_less_work - not sure there's any point showing this?
#xs = [1, 2, 4, 8]
#ys = [57, 36, 48, 49]
#plt.scatter(xs, ys, marker='v')

xs = [1]
#ys = [24] # 2nd ed
ys = [16]
#plt.scatter(xs, ys, marker='o')
plt.plot(xs, ys, '-o', label="No queue", markersize=10)
plt.annotate("No queue", (xs[0], ys[0]))
plt.xlim(0.5, 8.5)
plt.ylim(0, 100)

plt.title("The overhead of Queues on lightweight tasks")
plt.ylabel("Seconds (smaller is better)")
plt.xlabel("Number of processes")
plt.legend(loc="center right")

plt.draw()
plt.tight_layout()
print("Saving to multiprocessing_serial_vs_queue_times.png")
plt.savefig("multiprocessing_serial_vs_queue_times.png")
