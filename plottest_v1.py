#!/usr/bin/python3
'''
dynamic plotting with python matpltolib
'''
import time, datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

nmax = 101
readout = 0.1
start = time.time()
timestamps = [start - readout * (nmax - i) for i in range(nmax)]
dates = [dt.datetime.fromtimestamp(t) for t in timestamps]
datenums = [mdates.date2num(d) for d in dates]

x = datenums
y = [[0] * nmax, [1] * nmax]
yerr = [[0.0001] * nmax, [0.0001] * nmax]

plt.ion()
f, axarr = plt.subplots(2, 1, sharex='col')
f.suptitle("Timelines of random data")
plt.xticks(rotation=25 )
plt.xlabel("t / s")
plt.subplots_adjust(bottom=0.15, left=0.15)

l = [0]*len(axarr)
cap = [0]*len(axarr)
bar = [0]*len(axarr)
for i, ax in enumerate(axarr):
    l[i], = ax.plot_date(x, y[i], 'r+', label = r"$y = (t - t_0) \cdot (1 + \frac{%s}{10} \cdot \mathrm{random}[-1,1])$" %i)
    ax.legend()
    ax.set_ylabel("Data %s / Unit" %i)

while True:
    x.append(mdates.date2num(dt.datetime.fromtimestamp(time.time())))
    del x[0]
    for i, ax in enumerate(axarr):
        y[i].append((x[-1] - x[0]) * (1 + i * 0.1 * np.random.random()))
        del y[i][0]
        yerr[i].append(0.1 * y[i][0] + 0.05 * y[i][-1])
        del yerr[i][0]
        l[i].set_data(x, y[i])
        ax.relim()
        ax.autoscale_view()
    plt.draw()
    plt.pause(readout/10)
    time.sleep(readout * (np.random.random() + 1))
