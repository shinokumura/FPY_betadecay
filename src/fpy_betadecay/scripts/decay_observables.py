# import pandas as pd
import sys
import matplotlib.pyplot as plt
import pandas as pd
import math
import json

from config import DECAY_HEAT_CALC_TIME
from scripts.decay_data import DecayData
from scripts.decay_chain import decaychain
from scripts.fpy import read_fpy_data
from scripts.bateman import bateman_solver


# pd.reset_option("display.max_columns")
# pd.set_option("display.max_colwidth", None)
# pd.set_option("display.max_columns", None)
# pd.set_option("display.max_rows", None)
# pd.set_option("max_colwidth", None)
# pd.set_option("display.width", 1200)


def calc_cumlative_fpy(decaydataname, TALYS_FPY_FILE):
    """read calculated independent yield"""
    ind = read_fpy_data(TALYS_FPY_FILE)
    if sum(ind.values()) == 0:
        sys.exit()

    """ initial yield value """
    y1 = ind.copy()

    """ number of defalult iterations """
    iteration = 20

    """ convergence threshold """
    eps = 5.0e-3

    """ create full list of FPs """
    fplist = list(ind.keys())
    fp = []
    for t in range(iteration):
        add = []
        for f in fp:
            dd = DecayData(f, decaydataname)
            for m in range(dd.get_ndm()):
                add += [dd.get_next(int(m))]
        fp = fplist + add
    fp = sorted(set(fp))


    """ run decay chain calculations """
    y2 = {}
    for t in range(iteration):
        for i in fp:
            """initialize daughter nuclides (i)"""
            y2[i] = 0.00
            if y1.get(i) == 0.00:
                continue
            if y1.get(i) is None:
                y1[i] = 0.00
            for j in fp:
                """j is for decaying nuclide"""
                if i == j:
                    continue
                dd = DecayData(j, decaydataname)
                """ follow all decay modes """
                for m in range(dd.get_ndm()):
                    """count from 0"""
                    next = dd.get_next(int(m))
                    if next == i:
                        if y1.get(j) is not None:
                            y2[i] = y2[i] + (
                                float(y1[j]) * float(dd.get_branchingratio(int(m)))
                            )
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
                    d = d + abs(1.0 - (float(y2[k]) + float(ind[k])) / float(y1[k]))
            y1[k] = "{:.4E}".format(float(y2[k]) + float(ind[k]))
        print("# iteration: {0:3d}   convergence: {1:11.4e}".format(t, d))

        if d < eps:
            continue

        if t > iteration:
            continue

    """ resorting the dictionary """
    y = {}
    cfps = sorted(y1.keys())
    y = {key: y1[key] for key in cfps}
    df = pd.DataFrame.from_dict(y, orient="index")
    df.to_csv("cumulative.dat", sep=" ", header=False)

    """ output cmulative yiled  """
    print("#\n#\n#       Nuclide     cumulative     branchingR     DN yield")

    """ cumulative yeild and delayed neutrons output """
    delayed_n(y, decaydataname)

    return y


def delayed_n(y, decaydataname):
    totaldn = 0.00
    for i, v in y.items():
        rtyps = []
        dn = 0.00
        dd = DecayData(i, decaydataname)
        for m in range(dd.get_ndm()):
            # rtyp = float(dd.get_rtyp(int(m)))
            # if 1.5 <= rtyp < 1.6:
            #     dn = float(v) * float(dd.get_branchingratio(int(m)))
            #     totaldn += dn

            rtyps += [float(dd.get_rtyp(int(m)))]

        if any(x in rtyps for x in [1.5, 1.55, 1.555, 1.5555, 1.55555]):
            dn = float(v) * float(dd.get_branchingratio(int(m)))
            totaldn += dn
            print(
                "{0:>15s}{1:15.4E}{2:15.4E}{3:15.4E}".format(
                    i, float(v), float(dd.get_branchingratio(int(m))), float(dn)
                )
            )
        else:
            print(
                "{0:>15s}{1:15.4E}{2:15.4E}{3:15.4E}".format(
                    i, float(v), float(0.0), float(0.0)
                )
            )

    print("\n# total delayed neutron yield/fission: ", "{:.4E}".format(totaldn))
    return "{:.4E}".format(totaldn)


def calc_decay_heat(decaydataname, TALYS_FPY_FILE):
    """ 
    read calculated independent yield and return as dictionary format
    {'29-Cu-71-00': 1.9388e-07, '30-Zn-71-00': 4.8538e-09, '32-Ge-81-00': 0.001079, '32-Ge-81-01': 0.00032021, '32-Ge-82-00': 0.0012835, '33-As-83-00': 0.003104, '33-As-84-00': 0.0015447, '34-Se-84-00': 0.0083806, '34-Se-85-00': 0.013631, '34-Se-86-00': 0.010657, '35-Br-86-00': 0.0065523, '34-Se-87-00': 0.008291, '35-Br-87-00': 0.01003, '34-Se-88-00': 0.0034272, '35-Br-88-00': 0.014674, '36-Kr-88-00': 0.017015, '35-Br-89-00': 0.01236, '36-Kr-89-00': 0.033732, '35-Br-90-00': 0.0039933, '36-Kr-90-00': 0.041406, '37-Rb-90-00': 0.0046163, '37-Rb-90-01': 0.0033776, '35-Br-91-00': 0.001587, '36-Kr-91-00': 0.034204, '37-Rb-91-00': 0.018363, '36-Kr-92-00': 0.019615, '37-Rb-92-00': 0.031414, '38-Sr-92-00': 0.012332, '36-Kr-93-00': 0.0070431, '37-Rb-93-00': 0.025684, '38-Sr-93-00': 0.032474, '36-Kr-94-00': 0.0023559, '37-Rb-94-00': 0.014687, '38-Sr-94-00': 0.04691, '37-Rb-95-00': 0.0074683, '38-Sr-95-00': 0.050583, '39-Y-95-00': 0.012146, '37-Rb-96-00': 0.0020847, '38-Sr-96-00': 0.036099, '39-Y-96-00': 0.016311, '39-Y-96-01': 0.0047207, '38-Sr-97-00': 0.019665, '39-Y-97-00': 0.011232, '39-Y-97-01': 0.014795, '40-Zr-97-00': 0.016272, '38-Sr-98-00': 0.0087514, '39-Y-98-00': 0.018633, '39-Y-98-01': 0.0027843, '40-Zr-98-00': 0.028267, '38-Sr-99-00': 0.0021831, '39-Y-99-00': 0.014758, '40-Zr-99-00': 0.037899, '39-Y-100-00': 0.005942, '40-Zr-100-00': 0.03614, '41-Nb-100-00': 0.0080932, '41-Nb-100-01': 0.0021084, '39-Y-101-00': 0.0023083, '40-Zr-101-00': 0.021461, '41-Nb-101-00': 0.015964, '40-Zr-102-00': 0.013373, '41-Nb-102-00': 0.011644, '41-Nb-102-01': 0.0023383, '40-Zr-103-00': 0.0056203, '41-Nb-103-00': 0.012604, '42-Mo-103-00': 0.011888, '40-Zr-104-00': 0.0020551, '41-Nb-104-00': 0.0071167, '42-Mo-104-00': 0.013384, '41-Nb-105-00': 0.0037552, '42-Mo-105-00': 0.009866, '41-Nb-106-00': 0.0011699, '42-Mo-106-00': 0.0076699, '42-Mo-107-00': 0.0030437, '42-Mo-108-00': 0.0013666, '50-Sn-126-00': 0.0022319, '50-Sn-127-00': 0.0027619, '50-Sn-127-01': 0.0018785, '50-Sn-128-00': 0.0047009, '50-Sn-128-01': 0.0035334, '50-Sn-129-00': 0.0072467, '50-Sn-129-01': 0.0035136, '51-Sb-129-00': 0.0022, '51-Sb-129-01': 0.0014506, '50-Sn-130-00': 0.0092318, '50-Sn-130-01': 0.0046218, '51-Sb-130-00': 0.0048002, '51-Sb-130-01': 0.0037328, '50-Sn-131-00': 0.0074177, '50-Sn-131-01': 0.0020993, '51-Sb-131-00': 0.013262, '52-Te-131-00': 0.0012637, '52-Te-131-01': 0.0040943, '50-Sn-132-00': 0.0096906, '51-Sb-132-00': 0.013076, '51-Sb-132-01': 0.0028274, '52-Te-132-00': 0.016192, '50-Sn-133-00': 0.0020169, '51-Sb-133-00': 0.017276, '52-Te-133-00': 0.010206, '52-Te-133-01': 0.018717, '53-I-133-00': 0.0014796, '53-I-133-01': 0.00046681, '51-Sb-134-00': 0.0036703, '51-Sb-134-01': 0.0048538, '52-Te-134-00': 0.05067, '53-I-134-00': 0.0045969, '53-I-134-01': 0.0014839, '51-Sb-135-00': 0.0019872, '52-Te-135-00': 0.034324, '53-I-135-00': 0.025293, '52-Te-136-00': 0.019796, '53-I-136-00': 0.018041, '53-I-136-01': 0.002368, '54-Xe-136-00': 0.014075, '52-Te-137-00': 0.0069803, '53-I-137-00': 0.027949, '54-Xe-137-00': 0.027893, '52-Te-138-00': 0.0027032, '53-I-138-00': 0.017995, '54-Xe-138-00': 0.04768, '53-I-139-00': 0.0059809, '54-Xe-139-00': 0.051561, '55-Cs-139-00': 0.010262, '53-I-140-00': 0.0022984, '54-Xe-140-00': 0.043634, '55-Cs-140-00': 0.0229, '54-Xe-141-00': 0.017006, '55-Cs-141-00': 0.031625, '56-Ba-141-00': 0.013317, '54-Xe-142-00': 0.0074795, '55-Cs-142-00': 0.022606, '56-Ba-142-00': 0.031236, '54-Xe-143-00': 0.0015052, '55-Cs-143-00': 0.013981, '56-Ba-143-00': 0.041605, '55-Cs-144-00': 0.004271, '55-Cs-144-01': 0.00035424, '56-Ba-144-00': 0.036698, '57-La-144-00': 0.0068054, '55-Cs-145-00': 0.0012669, '56-Ba-145-00': 0.021492, '57-La-145-00': 0.013687, '56-Ba-146-00': 0.00964, '57-La-146-00': 0.010465, '57-La-146-01': 0.0021682, '58-Ce-146-00': 0.0061616, '56-Ba-147-00': 0.0028594, '57-La-147-00': 0.010136, '58-Ce-147-00': 0.011221, '57-La-148-00': 0.0040616, '58-Ce-148-00': 0.013185, '57-La-149-00': 0.001386, '58-Ce-149-00': 0.0086683, '58-Ce-150-00': 0.0051648, '58-Ce-151-00': 0.0014546, '59-Pr-151-00': 0.0024386, '60-Nd-153-00': 0.0012586}
    """
    ind = read_fpy_data(TALYS_FPY_FILE)
    # ind = {"33-As-88-00": 0.002}
    time = DECAY_HEAT_CALC_TIME
    coolingt_dep_b = [0.0] * len(time)
    coolingt_dep_g = [0.0] * len(time)
    coolingt_dep_a = [0.0] * len(time)
    coolingt_dep_dny = [0.0] * len(time)
    dd_dict_all = {}

    for i, y in ind.items():
        """
        loop over all FPs
        if the independent yield is 0, skip
        """
        # print("running calculation for nuclide:", i)

        pp = DecayData(i, decaydataname)
        if not hasattr(pp, "decayinfo"):
            print(i, " no decay data")
            continue
        if y == 0.0:
            continue

        tot_b = [0.0] * len(time)
        tot_g = [0.0] * len(time)
        tot_a = [0.0] * len(time)
        tot_dny = [0.0] * len(time)

        """
        call inner function which returns dictionary from the first daugthers
        [chain] and [branching ratio] are to reach each daugther
        [rtyp], [lambda], [e-bata] incorporate the parent nuclide
        """
        dd_dict = decaychain(i, decaydataname)
        dd_dict_all[i] = dd_dict

        for t in time:
            if t < 0.0:
                continue
            tnum = time.index(t)

            """ loop over number of chains from first daughters of parent nuclide:i """
            for k in dd_dict.keys():
                # print("time", t, "parent:", i, "chain:", dd_dict[k]['chain'])
                b = [0.0] * len(dd_dict)
                g = [0.0] * len(dd_dict)
                a = [0.0] * len(dd_dict)
                # dny = [0.0] * len(dd_dict)
                dny = 0.0

                """
                independent yield (ind[i] = y) x branching ratios to the daughter(s)
                fraction: initial fraction of the chain
                """
                branch_prod = math.prod(dd_dict[k]["branching"])
                fraction = (
                    y * branch_prod
                )  # Indepenent yield is normalized to 200%, fraction == N0 in bateman

                """
                solving bateman equation for the chain, k
                X returns in list with length of the chain including parent, 
                e.g. [1.1558e-16, 0.00028592, 0.02469, 5.5125e-06]
                """
                X = bateman_solver(dd_dict[k]["lmbds"], fraction, t)

                """
                get beta energy * bateman's solution Xi[t] at this timeperiod = t
                b, g, a : the list of the beta, gamman energy from the chain
                sum_b, sum_g , sum_a, sum_dny : the sum of the list b, g, a and delayed neutron yield
                coolingt_dep_b, coolingt_dep_g, coolingt_dep_dny: the sum of all nuclides in independent yield file
                """
                if len(X) != len(dd_dict[k]["en_betas"]):
                    break

                b = [
                    xi * float(enb) / 1e6 * lm
                    for xi, enb, lm in zip(
                        X, dd_dict[k]["en_betas"], dd_dict[k]["lmbds"]
                    )
                ]
                g = [
                    xi * float(eng) / 1e6 * lm
                    for xi, eng, lm in zip(
                        X, dd_dict[k]["en_gamms"], dd_dict[k]["lmbds"]
                    )
                ]
                a = [
                    xi * float(ena) / 1e6 * lm
                    for xi, ena, lm in zip(
                        X, dd_dict[k]["en_alphas"], dd_dict[k]["lmbds"]
                    )
                ]
                # dny = [xi * lm for xi, lm, rt in zip(X, dd_dict[k]['lmbds'], dd_dict[k]['rtyp']) if 1.5 <= rt < 1.6 ]
                for r in range(len(dd_dict[k]["rtyp"])):
                    rr = dd_dict[k]["rtyp"][r]
                    if rr == 1.5:
                        dny += X[r] * dd_dict[k]["lmbds"][r]
                    elif rr == 1.55:
                        dny += X[r] * dd_dict[k]["lmbds"][r] * 2
                    elif rr == 1.555:
                        dny += X[r] * dd_dict[k]["lmbds"][r] * 3
                    elif rr == 1.5555:
                        dny += X[r] * dd_dict[k]["lmbds"][r] * 4
                    else:
                        dny += 0.0

                # all contribution from first independent product at timeperiod = t
                tot_b[tnum] += sum(b)
                tot_g[tnum] += sum(g)
                tot_a[tnum] += sum(a)
                # tot_dny[tnum] += sum(dny)
                tot_dny[tnum] += dny

            coolingt_dep_b[tnum] += tot_b[tnum] * t
            coolingt_dep_g[tnum] += tot_g[tnum] * t
            coolingt_dep_a[tnum] += tot_a[tnum] * t
            coolingt_dep_dny[tnum] += tot_dny[tnum] * t

    """ for debug: output all decay chain used in the calculation """
    with open("dd_dict.json", "w") as f:
        json.dump(dd_dict_all, f, indent=2)

    df = pd.DataFrame()
    df["time"] = list(time)
    df["beta"] = list(coolingt_dep_b) / df["time"]
    df["gammma"] = list(coolingt_dep_g) / df["time"]
    df["dny"] = list(coolingt_dep_dny) / df["time"]
    df["beta*t"] = list(coolingt_dep_b)
    df["gamma*t"] = list(coolingt_dep_g)
    df["dny*t"] = list(coolingt_dep_dny)
    print(df)

    # compare with the calc result of U235(nth,f) by Oyak
    oyak = pd.read_csv(
        "sample/decayheat-2.53E-8-mev.dat", sep="\s+", header=0, comment="#"
    )
    oyak["time"] = oyak["time(s)"].astype(float)
    df["oyak_b"] = oyak["t*Pb(MeV)"]  # / oyak['time(s)']
    df["oyak_g"] = oyak["t*Pg(MeV)"]  # / oyak['time(s)']
    df["oyak_dny"] = oyak["t*d.n.act."]  # / oyak['time(s)']

    # plot of beta energy
    # df.plot('time', y= ['beta*t','oyak_b'], color = ['green','red'] ,xlabel="time", ylabel="t * En_beta [MeV]")
    df.plot("time", "beta*t", color="green")
    plt.xscale("log")
    # plt.show()

    # plot of gamma energy
    # df.plot('time', y= ['gamma*t','oyak_g'], color = ['green','red'] ,xlabel="time", ylabel="t * En_gamma [MeV]")
    df.plot("time", "gamma*t", color="orange")
    plt.xscale("log")
    # plt.show()

    # plot of alpha energy
    # df.plot('time', 'gamma*a', color = 'orange')
    # plt.xscale('log')
    # plt.show()

    # plot of delayed neutron yiedl
    # df.plot('time', y= ['dny*t','oyak_dny'], color = ['green','red'] ,xlabel="time", ylabel="t * delayed neutron yield")
    df.plot("time", "dny*t", color="green")
    plt.xscale("log")
    # plt.show()

    return df


if __name__ == "__main__":
    pass