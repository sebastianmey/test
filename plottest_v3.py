#!/usr/bin/python3
"""
Created on Mon Feb  2 22:20:05 2015

@author:    Sebastian Mey
            Institut für Kernphysik
            Forschungszentrum Jülich GmbH         
            s.mey@fz-juelich.de
"""
import sys, math, time, datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def lorentz(x, xpeak, fwhm):
    return 1 / (math.pi * fwhm /2 * (1 +((x - xpeak) * 2 / fwhm)**2))
    
def createplot(traces, npoints, n0, nmax):
    x = [n0 + n * (nmax - n0) / npoints for n in range(npoints)]
    y = [[0] * npoints]
    plt.ion()
    #plt.rcParams['text.usetex'] = True
    #plt.rcParams['font.size'] = 12
    plt.rcParams['savefig.extension'] = 'pdf'
    l = [0] * (traces + 1)
    for i in range(traces):
        y.append([0] * npoints)
        l[i], = plt.plot(x, y[i], c = str( 1. - 0.2 * float(i)), ls = '-')
    l[traces], = plt.plot(x, [1] * npoints, 'r-', lw = 2, label = "current tune")
    plt.title("Spectrum")
    plt.gca().legend()
    plt.gca().set_xlabel("f / kHz" )
    plt.gca().set_ylabel("Amplitude / arb. Unit" )
    plt.draw()
    return (x, y, l)
    
def updateplot(updateinterv, xdata, ydata, lines):
    peak = 2800. * (1 + np.random.random() / 100)
    ydata.append([lorentz(x, peak, 10.)  + 0.05 * np.random.random() for x in xdata])
    del ydata[0]
    #print(ydata)
    for i, line in enumerate(lines):
        line.set_ydata(ydata[i])
    plt.gca().relim()
    plt.gca().autoscale_view()
    plt.draw()
    plt.pause(updateinterv)
    
traces = 5
npoints = 201
f0 = 3.5 * 750.
fmax = 3.9 * 750.
updinterv = 1.
xdata, ydata, lines = createplot(traces, npoints, f0, fmax)
try:
    while True:
        updateplot(updinterv, xdata, ydata, lines)
except (KeyboardInterrupt):
    sys.exit(0)
