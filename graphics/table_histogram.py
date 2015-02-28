#!/usr/bin/env python3
import matplotlib
from utils import TANGO, filename, rcparams
from matplotlib import pyplot
from numpy import linspace

year = 0
length = 1
sig = 2

T = 1

FILL  = [TANGO["red"][0],  TANGO["green"][1]]
EDGES = [TANGO["red"][1],  TANGO["green"][2]]
    
ys = [[1,3,3],[1,6],[1,6]]
sizes = [(1,1),(1,1),(1,1)]

def get_data(hist):
    return ys[hist], sizes[hist]

def make_hist(y, size, name):
    x = linspace(0, len(y), num = len(y))

    colors     = [FILL[v > T] for v in y]
    edgecolors = [EDGES[v > T] if v > 0 else 'none' for v in y]

    figure = pyplot.figure(figsize = size)
    
    ax = pyplot.axes(frameon = False)
    ax.tick_params(top=False, bottom=False)

    #pyplot.xticks(x, ('1970', '2014', '2015'))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    pyplot.bar(x, y, width = 1, color = colors, edgecolor = edgecolors, linewidth = 2, align='center')

    batch_mode, fname = filename(name)

    if batch_mode:
        pyplot.savefig(fname, transparent = True)

    else:
        pyplot.show()
