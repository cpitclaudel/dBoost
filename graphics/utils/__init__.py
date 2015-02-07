TANGO = {"yellow": ("#fce94f", "#edd400", "#c4a000"),
         "orange": ("#fcaf3e", "#f57900", "#ce5c00"),
         "brown": ("#e9b96e", "#c17d11", "#8f5902"),
         "green": ("#8ae234", "#73d216", "#4e9a06"),
         "blue": ("#729fcf", "#3465a4", "#204a87"),
         "purple": ("#ad7fa8", "#75507b", "#5c3566"),
         "red": ("#ef2929", "#cc0000", "#a40000"),
         "grey": ("#eeeeec", "#d3d7cf", "#babdb6"),
         "black": ("#888a85", "#555753", "#2e3436")}

import sys
import matplotlib as mpl
from matplotlib import pyplot
from os.path import dirname, join

def filename(default):
    has_name = len(sys.argv) > 1
    return (has_name, sys.argv[1] if has_name else join(dirname(__file__), default))

def save2pdf(pdf):
    pyplot.tight_layout()
    pyplot.savefig(pdf, format = 'pdf', bbox_inches = "tight", transparent = True)
    pyplot.clf()

def setup():
    FS = 9.5
    mpl.rcParams['font.size'] = FS
    mpl.rcParams['legend.fontsize'] = FS
    mpl.rcParams['axes.titlesize'] = FS
    pyplot.gcf().set_size_inches(4, 4)
