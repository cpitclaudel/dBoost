#! /usr/bin/env python3
import sqlite3
import datetime
import sys
import features

def iter_db(path, query):
    with sqlite3.connect(path, detect_types = sqlite3.PARSE_COLNAMES) as connection:
        for row in connection.cursor().execute(query):
            yield tuple(row)

def read_db(path, query):
    return list(iter_db(path, query))

def print_rows(rows, failed_tests, rules, max_w = 40, header = "   "):
    SPACE = 2

    if len(rows) == 0:
        return

    nb_fields = len(rows[0])
    widths = (0,) * nb_fields

    # Compute the ideal column width for each column 
    for row in rows:
        widths = tuple(max(w, min(max_w, len(str(f))))
                       for w, f in zip(widths, row))

    descriptions = features.descriptions(rules)
    for row, row_failed_tests in zip(rows, failed_tests):
        highlight = tuple(x[0] for x in row_failed_tests)
        
        truncated_row = tuple(str(f)[:w].ljust(w + SPACE)
                              for f, w in zip(row, widths))
        
        sys.stdout.write(header + 
                         "".join(colorize(truncated_row, highlight)) + 
                         "\n")
        
        for field_id, _failed_tests in row_failed_tests:
            field_descs = descriptions[type(row[field_id])]
            failed_tests_descriptions = ",".join("'" + field_descs[test_id] + "'"
                                                 for test_id in _failed_tests)
            sys.stdout.write("   > Value {}: '{}' doesn't match feature(s) {}\n".format(
                                   field_id, row[field_id], failed_tests_descriptions))

        sys.stdout.write("\n")
            
def colorize(row, indices):
    row = [str(f) for f in row]
    for index in indices:
        row[index] = highlight(row[index])
    return row

class term:
    PLAIN   = '[0;0m'
    BOLD    = '[01;30m'
    RED     = '[01;31m'
    GREEN   = '[01;32m'
    YELLOW  = '[01;33m'
    BLUE    = '[01;34m'
    PURPLE  = '[01;35m'
    CYAN    = '[01;36m'
    MAGENTA = '[01;37m'
    WHITE   = '[01;38m'

def highlight(msg):
    return term.PLAIN + term.BOLD + term.RED + msg + term.PLAIN
