import random

def random_timestamp(min=1388534400, max=1420070400):
    return random.randint(min, max)

def randbool():
    return bool(random.randint(0, 1))

def choose_n(n, pool):
    shuffled = [x for x in pool]
    random.shuffle(shuffled)
    return shuffled[:n]

SEP = "\t"
def write_lines(fname, nb_lines, generator):
    with open(fname, mode='w') as stream:
        for _ in range(nb_lines):
            stream.write(SEP.join(str(field) for field in generator()) + "\n")

from datetime import datetime

def isweekend(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%A") in ["Saturday", "Sunday"]
