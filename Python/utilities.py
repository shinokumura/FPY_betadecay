from math import log10, floor, log


def signum_round(x, sig):
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


def slices(s, *args):
    position = 0
    for length in args:
        yield s[position : position + length]
        position += length
