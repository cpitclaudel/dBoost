from utils.autoconv import autoconv
import sys, csv

def parse_line(row, floats_only):
    return tuple(autoconv(field, floats_only) for field in row)

def stream_tuples(input, fs, floats_only, preload, maxrecords = float("+inf")):
    def stream():
        if stream.call_count > 0:
            input.seek(0)
        stream.call_count += 1

        row_length = None
        for id, row in enumerate(csv.reader(input, delimiter = fs)):
            if id > maxrecords:
                break

            row = parse_line(row, floats_only)

            if row_length != None and len(row) != row_length:
                sys.stderr.write("Discarding {}\n".format(row))
                continue

            row_length = len(row)
            yield row

    stream.call_count = 0

    if preload:
        dataset = list(stream())
        return (lambda: dataset)
    else:
        return stream
