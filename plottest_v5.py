#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on Do Oct 22 22:06:50 2015

@author:    Sebastian Mey
            Institut für Kernphysik
            Forschungszentrum Jülich GmbH
            
            s.mey@fz-juelich.de
'''
import math, time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.lines as lines
from matplotlib.animation import FuncAnimation
import numpy as np



def gendata():
    # data as provided by the mqtt_nmr.py publisher
    if np.random.random() > 0.9: # probability of 10%
        field = .5 +  2. * np.random.random() # random numbers from [.5, 2.5] 
        if field > 1.1 and field < 1.8:
            state = "L"
        elif field < 1. or field > 1.9:
            state = "N"
        else:
            state = "S"
        return time.time(), state, field


def color(string):
    colors = {"L": 'g', "S": 'y', "N": 'r', "none": 'k'} # Green, yellow, red, black
    c = colors["none"]
    for key in colors.keys():
        if key == string:
            c = colors[string]
    return c


def createplot(npoints = 120, updinterv = 1.):
    global f, ax, x, y, c, coll
    plt.rcParams['font.size'] = 14
    plt.rcParams['savefig.format'] = 'pdf'
    plt.rcParams['mathtext.default'] = 'regular'
    f, ax  = plt.subplots(1, 1)
    f.suptitle("Matplotlib Animation Test with Simulated NMR Data")
    start = time.time()
    #x = [start - updinterv * (npoints - i) for i in range(npoints)]
    timestamps = [start - updinterv * (npoints - i) for i in range(npoints)] # generate list of n timestamps backwards from start
    x = [dates.date2num(dt.datetime.fromtimestamp(t)) for t in timestamps] # reformat to python.datetime and from there to matplotlib.dates floats and use as x-data
    y = [0.] * npoints
    c = ['w'] * npoints
    coll = ax.scatter(x, y, s = 20, color = c, marker = 'o')
    f.autofmt_xdate() # or
    #plt.xticks(rotation = 25)
    ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))
    ax.set_xlabel("t / s")
    ax.set_ylabel("B / T")
    lock = lines.Line2D([], [], color='g', marker='o', markeredgecolor = 'g', markersize=10, linestyle = 'NONE', label='Locked')
    search = lines.Line2D([], [], color='y', marker='o', markeredgecolor = 'y', markersize=10, linestyle = 'NONE', label='Searching')
    nolock = lines.Line2D([], [], color='r', marker='o', markeredgecolor = 'r', markersize=10, linestyle = 'NONE', label='No Lock')
    ax.legend([lock, search, nolock], ["Locked", "Searching", "No Lock"]) # manual legend
    return coll,


def updateplot(frame):
    try:
        data = gendata()
        if data:
            time = float(data[0])
            lock = str(data[1])
            field = float(data[2])
            print(time, lock, field, len(x))
            #x.append(time)
            x.append(dates.date2num(dt.datetime.fromtimestamp(time))) # add timestamp from x data to x
            del x[0] # loose oldest x data
            y.append(field) # same for y data
            del y[0]
            c.append(color(lock)) #same for color data
            del c[0]
        coll = ax.scatter(x, y, s = 30, color = c, marker = 'o')
        ax.relim() # new axes limits from data
        #ax.autoscale_view() #autoscale axes to new limits, breaks matplotlib.dates.Dateformatter???
    except KeyboardInterrupt:
        print("exiting")
    return coll,


def main():
    createplot(60, .1)
    an = FuncAnimation(f, updateplot, interval = 10)#, blit = True)
    plt.show()


if __name__ == '__main__':
    main()
