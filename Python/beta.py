import pandas as pd

from decaydata import *
from fpy import read_fpy_data



def cumlative():
    ''' read calculated independent yield '''
    ind = read_fpy_data()
    ''' initial yield value '''
    y1 = ind.copy()
    ''' number of defalult iterations '''
    iteration = 100
    ''' convergence threshold '''
    eps = 1.0E-3

    ''' create full list of FPs '''
    fplist = list(ind.keys())
    fp = []
    for t in range(iteration):
        add = []
        for f in fp:
            dd = DecayData(f)
            for m in range(dd.get_ndm()):
                add += [dd.get_next(int(m))]
        fp = fplist + add
    fp = sorted(set(fp))

    ''' run decay chain calculations '''
    y2 = {}
    for t in range(iteration):
        # print("iteration:", t)
        for i in fp:
            ''' initialize daughter nuclides (i)　'''
            y2[i] = 0.00
            if y1.get(i) is None:
                y1[i] = 0.00
            for j in fp: 
                ''' j is for decaying nuclide　'''
                if i == j:
                    continue
                dd = DecayData(j)
                ''' follow all decay modes '''
                for m in range(dd.get_ndm()):
                    ''' count from 0 '''
                    next = dd.get_next(int(m))
                    if next == i:
                        if y1.get(j) is not None:
                            y2[i] = y2[i] +  ( float(y1[j]) * float(dd.get_branchingratio(int(m))) )
                    else:
                        continue
        d = 0.0
        for k in fp:
            if y2.get(k) is None:
                y2[k] = 0.00
            if ind.get(k) is None:
                ind[k] = 0.00
                # print(y1)
            if y1.get(k) is not None:
                if float(y1.get(k)) > 0.0:
                    d = d + abs(1.0 - ( float(y2[k]) + float(ind[k]) )/ float(y1[k]) )
            y1[k] = "{:.4E}".format( float(y2[k]) + float(ind[k]) )
        print("# iteration: {0:3d}   convergence: {1:11.4e}".format(t, d))
        if d < eps:
            break  

    ''' resort the dictionary '''
    y = {}
    cfps = sorted(y1.keys())
    y = {key:y1[key] for key in cfps}
    # df = pd.DataFrame.from_dict(y,orient = 'index')
    # df.to_csv("cumulative.dat", sep=' ', header=False)

    ''' output cmulative yiled  '''
    print("#\n#\n#       Nuclide     cumulative     branchingR     DN yield")
    ''' delayed neutrons '''
    delayedn(y)

    return y


def delayedn(y):
    dn = 0.00
    totaldn = 0.00
    for i, v in y.items():
        dd = DecayData(i)
        for m in range(dd.get_ndm()):
            rtyp = float(dd.get_rtyp(int(m)))
            if rtyp >= 1.5 and rtyp < 2.0:
                dn = float(v) * float(dd.get_branchingratio(int(m)))
                totaldn = totaldn + dn
                print ("{0:>15s}{1:15.4E}{2:15.4E}{3:15.4E}".format(i, float(v), float(dd.get_branchingratio(int(m))), float(dn)))
    print("\n# total delayed neutron yield/fission: ", "{:.4E}".format(totaldn))




if __name__ == '__main__':
# read decay data
    read_decay_data()
    cumlative()



