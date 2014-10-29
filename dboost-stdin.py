#! /usr/bin/python
#! /usr/bin/env python3
import dboost
import sys
import utils

dataset = []
row_length = None

def autoconv(field):
    try:
        field = int(field)
    except:
        pass
    return field

for line in sys.stdin:
    line = line.strip().split("\t")
    
    if row_length != None and len(line) != row_length:
        print("Discarding", line)

    row_length = len(line)
    dataset.append(tuple(autoconv(field) for field in line))

outliers = dboost.outliers_static(dataset)

if len(outliers) == 0:
    print("   All clean!")
else:
    rows, _, outlier_fields = zip(*outliers)
    utils.print_rows(rows, outlier_fields)
