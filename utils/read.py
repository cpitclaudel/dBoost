from utils.autoconv import autoconv
import sys

def parse_line(line, fs, floats_only):
    line = line.strip().split(fs)
    return tuple(autoconv(field, floats_only) for field in line)
    
def stream_tuples(input, fs, floats_only, preload):
    def stream():
        if stream.call_count > 0:
            input.seek(0)
        stream.call_count += 1
        
        row_length = None
        for line in input:
            row = parse_line(line, fs, floats_only)
            
            if row_length != None and len(row) != row_length:
                sys.stderr.write("Discarding {}\n".format(line))
                continue

            row_length = len(row)
            yield row

    stream.call_count = 0

    if preload:
        dataset = list(stream())
        return (lambda: dataset)
    else:
        return stream
