from . import utils
from utils.color import term, highlight
import collections
import sys

BLOCK = "█"

def histplot(counter, height = None):
    import os, sys
    W, H = os.get_terminal_size()

    if height == None:
        height = H
        
    if 2 * len(counter) > W - 1:
        sys.stderr.print("Console too narrow to show {} values".format(len(counter)))
        return None
        
    data = sorted(counter.items())
    scale = height / max(counter.values())
    
    legends = ["{:.2f}".format(rowid / scale) for rowid in range(height)]
    widest_legend = max(map(len, legends))
    legend_formatter = "{:>" + str(widest_legend) + "} "

    for rowid in reversed(range(height)):
        sys.stdout.write(legend_formatter.format(legends[rowid]))
        for _, v in data:
            v *= scale
            sys.stdout.write("█ " if v >= rowid + 0.5
                             else "▄ " if v > rowid else "  ")
        sys.stdout.write("\n")


def hhistplot(counter, highlighted, indent = "", pipe = sys.stdout, w = 20):
    import os, sys
    
    W, H = os.get_terminal_size()
    
    plot_w = min(w, W - 10 - len(indent))
    scale = plot_w / max(counter.values())
    data = sorted(counter.items())
    
    for key, value in data:
        label = str(key)
        bar_size = int(value * scale)
        header = indent
        bar = BLOCK * bar_size + " " if bar_size > 0 else ""

        label_avail_space = W - 2 - len(bar) - len(header)
        if len(label) > label_avail_space:
            label = label[:label_avail_space - 3] + "..."

        line = bar + label
        if key == highlighted:
            line = highlight(line, term.PLAIN, term.RED)

        pipe.write(header + line + "\n")

class Histogram:
    ID = "histogram"
    
    def __init__(self, peak_threshold, outlier_threshold):
        self.peak_threshold = peak_threshold
        self.outlier_threshold = outlier_threshold
        self.reset()

    def reset(self):
        self.all_counters = None
        self.counters = None
        self.sizes = None        
        
    @staticmethod
    def register(parser):
        parser.add_argument("--" + Histogram.ID, nargs = 2,
                            metavar = ("peak_s", "outlier_s"),
                            help = "Use a discrete histogram-based model, identifying fields that" +
                            "have a peaked distribution (peakiness is determined using the peak_s " +
                            "parameter), and reporting values that fall in classes totaling less than "
                            "outlier_s of the corresponding histogram. Suggested values: 0.8 0.2.")
        
    @staticmethod
    def from_parse(params):
        return Histogram(*map(float, params))
        
    @staticmethod
    def add(counter, x):
        counter[x] += 1
        return counter

    def is_peaked(self, distribution):
        import heapq
        if len(distribution) > 16: # TODO
            return False
        else:
            nb_peaks = max(1, min(3, len(distribution) // 2)) # TODO
            total_weight = sum(distribution.values())
            peaks_weight = sum(heapq.nlargest(nb_peaks, distribution.values()))
            return peaks_weight > self.peak_threshold * total_weight
    
    def fit(self, Xs):
        for X in Xs:
            self.counters = utils.defaultif(self.counters, X, collections.Counter)
            self.sizes = utils.zeroif(self.sizes, X)
            self.counters = utils.merge(self.counters, X, utils.id, Histogram.add)
            self.sizes = utils.merge(self.sizes, X, utils.not_null, utils.plus)

        self.all_counters = self.counters
        self.counters = utils.merge(self.counters, self.counters, self.is_peaked, utils.keep_if)
        
    def find_discrepancies(self, X, index):
        discrepancies = []
        
        for field_id, (x, m, s) in enumerate(zip(X, self.counters, self.sizes)):
            failed_tests = []
            for test_id, (xi, mi, si) in enumerate(zip(x, m, s)):
                if mi == None:
                    continue
                if mi.get(xi, 0) < self.outlier_threshold * si:
                    failed_tests.append(test_id)
            if failed_tests != []:
                discrepancies.append((field_id, failed_tests))

        return discrepancies

    def more_info(self, field_id, feature_id, feature_name, X, indent = "", pipe = sys.stdout):
        highlighted = X[field_id][feature_id]
        counter = self.all_counters[field_id][feature_id]
        pipe.write(indent + "• histogram for {}/{}:\n".format(field_id, feature_name))
        hhistplot(counter, highlighted, indent + "  ", pipe)

