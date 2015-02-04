import sys
from math import exp
from matplotlib import pyplot
from utils import TANGO

sys.path.append('../dboost')

from dboost.models.discrete import Histogram
from dboost.models.discretepart import PartitionedHistogram

import matplotlib
matplotlib.rc('text', usetex=True)
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath,amssymb}"]

HISTOGRAMS = [
    [1, 100], # True-False
    [44, 45, 49, 100, 101, 102], # Samll increments
    [exp(-(x/3)**2) for x in range(-6, 1)], # Exp shape
    [1, 1, 2, 4, 80, 82, 84, 88] # Many large columns
]

def normalize(hist):
    mx = max(hist)
    return [x / mx for x in hist]

HISTOGRAMS = [normalize(hist) for hist in HISTOGRAMS]
HIST_LENGTH = max(len(hist) for hist in HISTOGRAMS)

def is_peaked(hist, model):
    hist = dict(enumerate(hist))
    return model.IsPeaked(hist, 0.8)

BAR_WIDTH = 0.8
PLOTS_PER_LINE = 4
DISABLED_AXES = ("left", "right", "top")
fig, axes = pyplot.subplots(len(HISTOGRAMS) // PLOTS_PER_LINE, PLOTS_PER_LINE, sharex = True, sharey = True, squeeze = False, frameon = False)

def ax(hid):
    row, column = hid // PLOTS_PER_LINE, hid % PLOTS_PER_LINE
    return axes[row][column]

for hid, hist in enumerate(HISTOGRAMS):
    left = HIST_LENGTH / 2 - len(hist) / 2
    xs = [left + offset for offset in range(len(hist))]

    axis = ax(hid)
    bars = axis.bar(xs, hist, width=BAR_WIDTH)

    axis.xaxis.set_ticks([])
    axis.yaxis.set_ticks([])
    axis.yaxis.set_ticks_position('none')
    for side in DISABLED_AXES:
        axis.spines[side].set_color('none')
    axis.set_xlim(xmin=-1, xmax=HIST_LENGTH + 1)
    axis.patch.set_visible(False)

    delta, min_hi, max_low, first_hi = PartitionedHistogram.PeakProps(hist)
    annot_x = left + first_hi - 1 + BAR_WIDTH / 2
    annot_y = (hist[first_hi - 1] + hist[first_hi]) / 2
    axis.annotate(
        '', xy=(annot_x, hist[first_hi - 1]), xycoords='data',
        xytext=(annot_x, hist[first_hi]), textcoords='data',
        arrowprops={'arrowstyle': '<->'})
    annot_color = 'black' # TANGO["green" if delta >= 5 else "red"][2] '$\boldsymbol\times\mathbf{{{:.0f}}}$'
    axis.text(annot_x - 0.1, annot_y, r'$\times\,{:.0f}$'.format(delta), horizontalalignment='right', color=annot_color, fontsize=14)
    nb_peaks = Histogram.NbPeaks(hist)
    for bid, bar in enumerate(bars):
        in_simple_peak = bid >= len(bars) - nb_peaks
        in_tricky_peak = bid >= first_hi
        bar.set_color(TANGO['blue' if in_simple_peak else 'grey'][0])
        bar.set_edgecolor(TANGO['black'][1])
        if in_tricky_peak:
            bar.set_hatch(r'//')

    peaked = lambda model: [r'$\boxtimes$', r'$\square$'][is_peaked(hist, model)]
    axis.set_xlabel('DI: {} DD: {}'.format(peaked(Histogram), peaked(PartitionedHistogram)))

pyplot.show()


    # transform = axis.get_xaxis_transform() # Using data coordinates doesn't allow drawing outside of the axes. annotation_clip=False would work too
    # axis.annotate(
        # '', xy=(left + 3 - (1 - BAR_WIDTH) / 2, 0.02), xycoords = transform,
        # xytext=(left + 8 - (1 - BAR_WIDTH) / 2, 0.02), textcoords = transform,
        # arrowprops={'connectionstyle': 'bar,fraction=-0.2', 'arrowstyle': '-'})
