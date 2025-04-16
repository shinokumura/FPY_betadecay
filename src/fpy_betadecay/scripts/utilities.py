from math import log10, floor, log


def signum_round(x, sig):
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


def slices(s, *args):
    position = 0
    for length in args:
        yield s[position : position + length]
        position += length


def format_nuclide(nuclide):
    #  43-Tc-99-01
    meta = ""
    if nuclide != "FP":
        charge, elem, mass, iso = nuclide.split("-")
        if iso == "00":
            meta = ""
        elif iso == "01":
            meta = "m"
        elif iso == "02":
            meta = "m2"
        return "$^{" + mass + meta + "}$" + elem
    else:
        return "Fission Products"
