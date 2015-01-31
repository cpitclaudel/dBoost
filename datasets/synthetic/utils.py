import random
import os

BASE = os.path.dirname(os.path.realpath(__file__))

def random_timestamp(min=1388534400, max=1420070400):
    return random.randint(min, max)

def randbool():
    return bool(random.randint(0, 1))

def choose_n(n, pool):
    shuffled = [x for x in pool]
    random.shuffle(shuffled)
    return shuffled[:n]

SEP = "\t"
def write_lines(fname, nb_lines, generator, report_outliers):
    outliers_fname = fname + "-outliers"
    with open(os.path.join(BASE, fname), mode='w') as db:
        with open(os.path.join(BASE, outliers_fname), mode='w') as outliers:
            for linum in range(nb_lines):
                outlier, row = generator()
                if report_outliers and outlier:
                    outliers.write(str(linum) + "\n")
                db.write(SEP.join(str(field) for field in row) + "\n")
    # if not report_outliers:
    #     try:
    #         os.remove(outliers_fname)
    #     except FileNotFoundError:
    #         pass

import time

def isweekend(timestamp):
    wday = time.gmtime(timestamp).tm_wday
    wkend = wday in [5, 6]
    return wkend
