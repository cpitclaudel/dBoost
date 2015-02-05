from .autoconv import autoconv
from .printing import debug
import sys, csv

def parse_line(row, floats_only):
    return tuple(autoconv(field, floats_only) for field in row)

def stream_tuples(input, fs, floats_only, preload, maxrecords = float("+inf")):
    def stream():
        if stream.call_count > 0:
            input.seek(0)
        stream.call_count += 1

        row_length = None
        for rid, row in enumerate(csv.reader(input, delimiter = fs)):
            if rid > maxrecords:
                break

            row = parse_line(row, floats_only)

            if row_length == None:
                row_length = len(row)
            elif len(row) != row_length:
                sys.stderr.write("Discarding {}\n".format(row))
                continue

            if stream.call_count == 1 and rid == 0 and row_length == 1:
                debug("Your dataset seems to have only one column. Did you need -F?")

            yield row

    stream.call_count = 0

    if preload:
        dataset = list(stream())
        return (lambda: dataset)
    else:
        return stream
