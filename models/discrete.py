from utils import tupleops
from utils.color import term, highlight
import bisect
import collections
import sys

BLOCK = "█"

def hhistplot(counter, highlighted, indent = "", pipe = sys.stdout, w = 20):
    import os, sys

    W, H = os.get_terminal_size()

    plot_w = min(w, W - 10 - len(indent))
    scale = plot_w / max(counter.values())
    data = sorted(counter.items())

    if highlighted not in counter:
        bisect.insort_left(data, (highlighted, 0))

    header_width = max(len(str(value)) for _, value in data)

    for key, value in data:
        label = str(key)
        bar_size = int(value * scale)
        header = indent + "[" + str(value).rjust(header_width) + "] "
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
            self.counters = tupleops.defaultif(self.counters, X, collections.Counter)
            self.sizes = tupleops.zeroif(self.sizes, X)
            self.counters = tupleops.merge(self.counters, X, tupleops.id, Histogram.add)
            self.sizes = tupleops.merge(self.sizes, X, tupleops.not_null, tupleops.plus)

        self.all_counters = self.counters
        self.counters = tupleops.merge(self.counters, self.counters, self.is_peaked, tupleops.keep_if)

    def find_discrepancies_in_features(self, field_id, features, counters, sizes, discrepancies):
        for feature_id, (xi, mi, si) in enumerate(zip(features, counters, sizes)):
            if mi == None:
                continue
            if mi.get(xi, 0) < self.outlier_threshold * si:
                discrepancies.append(((field_id, feature_id),))

    def find_discrepancies(self, X, index):
        discrepancies = []

        for field_id, (x, m, s) in enumerate(zip(X, self.counters, self.sizes)):
            if field_id > 0:
                self.find_discrepancies_in_features(field_id, x, m, s, discrepancies)

        if len(discrepancies) == 0:
            self.find_discrepancies_in_features(0, X[0], self.counters[0],
                                                self.sizes[0], discrepancies)

        return discrepancies

    def more_info(self, discrepancy, description, X, indent = "", pipe = sys.stdout):
        assert(len(discrepancy) == 1)
        field_id, feature_id = discrepancy[0]
        highlighted = X[field_id][feature_id]
        counter = self.all_counters[field_id][feature_id]
        pipe.write(indent + "• histogram for {}:\n".format(description))
        hhistplot(counter, highlighted, indent + "  ", pipe)
