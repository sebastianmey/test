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

def set_errdata(line, caplines, barlinecols, x, xerr, y, yerr):
    x = np.array(x)
    xerr = np.array(xerr)
    y = np.array(y)
    yerr = np.array(yerr)
    line.set_data(x, y)
    errpos = (x-xerr,y), (x+xerr,y), (x, y - yerr), (x, y + yerr)
    for i, pos in enumerate(errpos):
        caplines[i].set_data(pos)
    barlinecols[0].set_segments(zip(zip(x-xerr,y), zip(x+xerr,y)))
    barlinecols[1].set_segments(zip(zip(x,y-yerr), zip(x,y+yerr)))
    return (line, caplines, barlinecols)
    
def createplot(p, n, u):
    global start, x, xerr, y, yerr, f, axarr, l, c, b    
    start = time.time()
    timestamps = [start - u * (n - i) for i in range(n)]
    x = [mdates.date2num(dt.datetime.fromtimestamp(t)) for t in timestamps]
    start = x[0]
    xerr = [0] * n
    y = []
    yerr = []
    l = [0] * p
    c = [0] * p
    b = [0] * p

    plt.ion()
    #plt.rcParams['text.usetex'] = True
    plt.rcParams['font.size'] = 12
    plt.rcParams['savefig.extension'] = 'pdf'
    f, axarr = plt.subplots(p, 1, sharex='col')
    f.suptitle(r"$\mathrm{Timelines}$")
    plt.xticks(rotation=25 )
    plt.xlabel(r"$t\, /\, \mathrm{s}$")
    plt.subplots_adjust(bottom=0.15)
    for i, ax in enumerate(axarr):
        y.append([0] * n)
        yerr.append([0] * n)        
        l[i], c[i], b[i] = ax.errorbar(x, y[i], yerr = yerr[i], xerr = xerr, fmt='r+', label = r"$y \propto \sin(x)^{%s + 1}$" %i)
        ax.legend()
        ax.set_ylabel(r"$\mathrm{Data}\, %s\, /\, \mathrm{Unit}$" %i)
        ax.xaxis.set_major_formatter(mdates.DateFormatter(r'$%H:%M:%S$'))
    plt.draw()
    
def updateplot(u):
    x.append(mdates.date2num(dt.datetime.fromtimestamp(time.time())))
    del x[0]
    for i, ax in enumerate(axarr):
        y[i].append(100*(i+1) * math.sin(10000 * (x[-1]-start))**(1+i))
        del y[i][0]
        yerr[i].append(0.05 * y[i][-1])
        del yerr[i][0]
        set_errdata(l[i], c[i], b[i], x, xerr ,y[i], yerr[i])
        ax.relim()
        ax.autoscale_view()
        #print(i, mdates.num2date(x[0]), mdates.num2date(x[-1]), y[i][-1])
    plt.draw()
    plt.pause(u)
    
plots = 5
npoints = 201
updinterv = 0.1    
createplot(plots, npoints, updinterv)
try:
    while True:
        updateplot(updinterv)
except (KeyboardInterrupt):
    sys.exit(0)
