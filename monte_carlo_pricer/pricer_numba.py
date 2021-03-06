import numpy as np
import sys
from math import sqrt, exp
from timeit import default_timer as timer
#from matplotlib import pyplot

from numba import jit, double, void

if sys.version_info[0] == 2:
    range = xrange

@jit(double[:](double, double[:], double, double, double[:]))
def step(dt, prices, c0, c1, noises):
    return prices * np.exp(c0 * dt + c1 * noises)

@jit(void(double[:,:], double, double, double))
def monte_carlo_pricer(paths, dt, interest, volatility):
    c0 = interest - 0.5 * volatility ** 2
    c1 = volatility * np.sqrt(dt)

    for j in range(1, paths.shape[1]):
        prices = paths[:, j - 1]
        noises = np.random.normal(0., 1., prices.size)
        paths[:, j] = step(dt, prices, c0, c1, noises)

if __name__ == '__main__':
    from driver import driver
    driver(monte_carlo_pricer)
