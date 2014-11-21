#! /usr/bin/env python3
import dboost
import sys
import utils
import features
#from models import gaussian
from models import statistical 

dataset = []
row_length = None

def autoconv(field):
    try:
        field = int(field)
    except:
        pass
    return field

for line in sys.stdin:
    line_stripped = line.strip().split("\t")
    if len(line_stripped) == 1:
        # In the absence of tabs, fall back to any blank character
        line_stripped = line.split()
    line = line_stripped
    
    if row_length != None and len(line) != row_length:
        print("Discarding", line)

    row_length = len(line)
    dataset.append(tuple(autoconv(field) for field in line))

#model = gaussian.Mixture(2)
model = statistical.Pearson(.001) 
outliers = dboost.outliers_static_stats(dataset, model)

if len(outliers) == 0:
    print("   All clean!")
else:
    rows, _, failed_tests = zip(*outliers)
    utils.print_rows(rows, failed_tests, features.rules)
