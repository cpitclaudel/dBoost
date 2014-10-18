#! /usr/bin/env python3
import sqlite3
import datetime
import sys

def iter_db(path, query):
    with sqlite3.connect(path, detect_types = sqlite3.PARSE_COLNAMES) as connection:
        for row in connection.cursor().execute(query):
            yield tuple(row)

def read_db(path, query):
    return list(iter_db(path, query))

def print_rows(rows, highlights, max_w = 40, header = "   "):
    SPACE = 2
    rows = [tuple(map(str, row)) for row in rows] 

    if len(rows) == 0:
        return

    nb_fields = len(rows[0])
    widths = (0,) * nb_fields

    for row in rows:
        widths = tuple(max(w, min(max_w, len(s))) 
                       for w, s in zip(widths, row))

    for row, highlight in zip(rows, highlights):
        row = (f[:w].ljust(w + SPACE) 
               for f,w in zip(row, widths))
        sys.stdout.write(header + 
                         "".join(colorize(row, highlight)) + 
                         "\n")

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
