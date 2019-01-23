import matplotlib.pyplot as plt
import numpy as np
import os
import math as m
from scipy.constants import *
from util.constants import *
plt.rcParams.update(pgf_with_latex)
plt.style.use("classic")
plt.grid(True)
x = np.arange(1e-6, 0.25e-3, 1e-6)

def planck(x, T):
    a = 2 * pi * h * c**2
    b = h*c/(x*k*T)
    intensity = a/ ( (x**5) * (np.exp(b) - 1.0) )
    return intensity

y3 = planck(x, 10)
y1 = planck(x, 20)
y2 = planck(x, 100)
y4 = planck(x, 200)
plt.plot(x*1e6, y1/np.amax(y1), label = "20 K")
plt.plot(x*1e6, y2/np.amax(y2), label= "100 K")
plt.plot(x*1e6, y4/np.amax(y4), label= "200 K")
plt.xticks(np.arange(0, 250, 50))
xlabel = plt.xlabel("$\mathrm{\mu m}$")
plt.ylabel("$B_{\lambda, T}/B_{\mathrm{max}}$")
# plt.legend(loc="upper right")
plt.text(200, 0.81, '20 K')

plt.vlines(x[np.argmax(y1)]*1e6, 0, 1, linestyles="--")
plt.text(45, 0.7, '100 K')
plt.vlines(x[np.argmax(y2)]*1e6, 0, 1, linestyles="--")
plt.text(33, 0.3, '200 K')
plt.vlines(x[np.argmax(y4)]*1e6, 0, 1, linestyles="--")
plt.ylim(0, plt.ylim()[1])
plt.xticks(list(plt.xticks()[0]) + [ x[np.argmax(y2)]*1e6, x[np.argmax(y4)]*1e6])

plt.savefig("planck.png", bbox_inches='tight', bbox_extra_artists=[xlabel])
