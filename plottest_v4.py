#!/usr/bin/python3
"""
Created on Mi Apr 8 21:32:05 2015

@author:    Sebastian Mey
            Institut für Kernphysik
            Forschungszentrum Jülich GmbH         
            s.mey@fz-juelich.de
"""
import sys, os, math, time, datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def lorentz(x, xpeak, fwhm):
    return 1 / (math.pi * fwhm /2 * (1 +((x - xpeak) * 2 / fwhm)**2))
    
def createplot(traces, npoints, n0, nmax):
    x = [n0 + n * (nmax - n0) / npoints for n in range(npoints)]
    y = [[[0] * npoints], [[0] * npoints]]

    plt.ion()
    #plt.rcParams['text.usetex'] = True
    #plt.rcParams['font.size'] = 12
    plt.rcParams['savefig.extension'] = 'pdf'
    f, axarr = plt.subplots(2, 1, sharex='col')
    f.suptitle("Spectra")
    plt.xlabel("f / kHz" )
    l = [[0] * (traces + 1), [0] * (traces + 1)]
    for j, ax in enumerate(axarr):
        if j == 0:
            color = "r"
            direction = "horizontal"
        elif j == 1:
            color = "b"
            direction = "vertical"
        for i in range(traces):
            y[j].append([0] * npoints)
            l[j][i], = ax.plot(x, y[j][i], c = str( 1. - 0.2 * float(i)), ls = '-')
        l[j][traces], = ax.plot(x, [1] * npoints, '%s-' %color, lw = 2, label = "current %s tune" % direction)
        ax.legend()
        ax.set_ylabel("Amplitude %s / arb. Unit" % direction)
    plt.draw()
    return (x, y, l, axarr)
    
def updateplot(u):#, xdata, ydata, lines):
    peak = [0, 0]
    for j, ax in enumerate(axarr):
        peak[j] = (2800. + j * 50.) * (1 + np.random.random() / 100)
        ydata[j].append([lorentz(x, peak[j], 10.)  + 0.05 * np.random.random() for x in xdata])
        del ydata[j][0]
        #print(ydata)
        for i, line in enumerate(lines[j]):
            line.set_ydata(ydata[j][i])
        ax.relim()
        ax.autoscale_view()
    plt.draw()
    plt.pause(u)
    
traces = 5
npoints = 201
f0 = 3.5 * 750.
fmax = 3.9 * 750.
updinterv = 1.
xdata, ydata, lines, axarr = createplot(traces, npoints, f0, fmax)
try:
    while True:
        updateplot(updinterv)#, xdata, ydata, lines)
except (KeyboardInterrupt):
    sys.exit(0)
