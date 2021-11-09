import math

from decaydata import *
from fpy import read_fpy_data
from config import DEFAULT_LONG_LIVED


def singledecay(N0, tau, hl, time):
    return tau * N0 * math.exp((-0.693/hl)*time)

def track_chain():
    pass

# def bateman(lmbd, t):
def bateman():
    max_number_of_chain = 10
    # if lmbd is None or t is None:
    # ind = read_fpy_data()
    ind = {'65-Tb-144-01': 0.001, '65-Tb-142-00': 0.005}
    # https://github.com/bjodah/batemaneq/blob/master/batemaneq/bateman.py
    for nuk in ind:
        print(nuk)
        track = {}
        ''' parent nuclide '''
        track[nuk] = {}
        pp = DecayData(nuk)
        ''' first set of daughters '''
        i = 0
        for m in range(pp.get_ndm()):
            hl =  pp.get_halflife()
            lmbd = pp.get_branchingratio(int(m))
            next = pp.get_next(int(m))
            while True:
                track[nuk][i] = get_next_info(next)
                if track[nuk][i]['next'] is None:
                    break
                if float(hl) > DEFAULT_LONG_LIVED:
                    break
                if max_number_of_chain < i:
                    break
                i += 1
                print(i, track)


def get_next_info(nuclide):
    dd = DecayData(nuclide)
    track = {}
    for m in range(dd.get_ndm()):
        hl =  dd.get_halflife()
        lmbd = dd.get_branchingratio(int(m))
        next = dd.get_next(int(m))
        track = {'hl': hl, 'lmbd': lmbd, 'next': next}
    return dict(track)




bateman()


