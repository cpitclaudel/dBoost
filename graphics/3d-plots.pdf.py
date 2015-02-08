#!/usr/bin/env python2
from utils import filename, save2pdf
from utils.plots_helper import sensors3D
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot

batch, fname = filename("sensor-mix-plots.pdf")
dfile = "../datasets/real/intel/sensors-1000-dirty.txt"

# e, p, t
args = [(0,1,0.005),  # from sensor-plots (p3)
        (0.7,1,0.1),  # from sensor-plots (p1 and p2)
        (0.7,2,0.05)] # from sensor-mix-plots (p1 and p2)

if batch:
    pdf = PdfPages(fname)

for e, p, t in args:
    ofile = "../results/sensors_dirty_stat" + str(e) + "_mix" + str(p) + "_" + str(t) + ".out"
    sensors3D(dfile,ofile)
    if batch:
        pyplot.savefig(pdf, pad_inches=1, format = 'pdf')
    else:
        pyplot.show()

if batch:
    pdf.close()
