import numpy as np
import matplotlib.pyplot as plt

ns = np.arange(-10, 10)


def sigmoid(z):
    s = 1.0 / (1.0 + np.exp(-1.0 * z))
    return s

s = sigmoid(ns)
plt.figure(0)
plt.clf()
plt.plot(s)
plt.title("Quick wins and diminishing returns")
plt.xlabel("Increasing effort")
plt.ylabel("Faster execution")
plt.annotate("Profile to understand\nprogram's behavior", (2.9, 0.15))
plt.annotate("Improve algorithm\nbased on evidence", (4.5, 0.4))
plt.annotate("Use a compiler or JIT\nto achieve quick wins", (5.7, 0.7))
plt.annotate("Beware diminishing\nreturns with \nextended effort", (13, 0.8))
plt.xticks([])
plt.yticks([])
plt.ylim(-0.02, 1.02)
plt.xlim(-0.01, 19.01)
plt.tight_layout()
#plt.show()
plt.savefig("07_diminishing_returns.png")
