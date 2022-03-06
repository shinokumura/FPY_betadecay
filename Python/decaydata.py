import json
from collections import deque
import copy

from math import log

from elem import ztoelem
from utilities import *


"""
convert original ENDF fromatted Decay Data Libray to the simple format
"""


def convert_ddlibrary():
    import re
    from pathlib import Path
    from natsort import natsorted
    from config import DECAY_DATA_LIB_PATH
    from utilities import slices

    p = Path(DECAY_DATA_LIB_PATH).glob("*0*")
    p = [Path(pa) for pa in natsorted([str(pa) for pa in p])]
    print(" 2021, ENDFBVIII DD, Made by S. Okumura/IAEA")

    for DDFILE in p:
        with open(DDFILE) as ddl:
            lines = ddl.readlines()[1:]
        i = 0
        ln = 0

        """
        innner function to convert fortran-allowed scientific format into expornential expression
        """

        def conv_to_e(str):
            str = str.strip()
            if str.find("-", 2) > 1 and ("E-" not in str):
                return re.sub("([+-]{0,1}[0-9]+)(\-)", r"\1E-", str)
            elif str.find("+", 2) > 1 and ("E+" not in str):
                return re.sub("([+-]{0,1}[0-9]+)(\+)", r"\1E+", str)
            elif "E+" in str or "E-" in str:
                return float(str)
            else:
                return str

        nc2 = 6
        for line in lines:
            i += 1
            xx, mat, mf, mt = slices(line, 66, 4, 2, 3)
            if int(mf) == 8 and int(mt) == 457:
                if ln == 0:
                    ln = i
                if i == ln:
                    za, awr, lis, lis0, nst, nsp = slices(line, 11, 11, 11, 11, 11, 11)
                    z = int(float(conv_to_e(za)) / 1000.0)
                    a = int(float(conv_to_e(za)) % 1000.0)
                if i == ln + 1:
                    thlf, dthlf, xx, nc2 = slices(line, 11, 11, 22, 11)
                if i == ln + 2:
                    eb0, deb0, eg0, deg0, ea0, dea0 = slices(
                        line, 11, 11, 11, 11, 11, 11
                    )
                if int(nc2) == 34:
                    ln += 6
                if i == ln + 3:
                    spi, par, xx, xx, ndk6, ndk = slices(line, 11, 11, 11, 11, 11, 11)
                    if int(ndk) == 0:
                        continue

                    print(
                        "{:5d}{:5d}{:5d}{:15.7E}{:15.7E}{:15.7E}{:5d}{:5d}{:5d}".format(
                            int(z),
                            int(a),
                            int(lis0),
                            float(conv_to_e(thlf)),
                            float(conv_to_e(dthlf)),
                            float(conv_to_e(awr)),
                            int(ndk),
                            int(nsp),
                            int(mat),
                        )
                    )
                    print(
                        "{:15.7E}{:15.7E}{:15.7E}{:15.7E}{:15.7E}{:15.7E}".format(
                            float(conv_to_e(eb0)),
                            float(conv_to_e(deb0)),
                            float(conv_to_e(eg0)),
                            float(conv_to_e(deg0)),
                            float(conv_to_e(ea0)),
                            float(conv_to_e(dea0)),
                        )
                    )
                    for nd in range(int(ndk)):
                        rtyp, rfs, q, dq, br, dbr = slices(
                            lines[ln + 3 + nd], 11, 11, 11, 11, 11, 11
                        )
                        print(
                            "{:15.7E}{:15.7E}{:15.7E}{:15.7E}{:15.7E}{:15.7E}".format(
                                float(conv_to_e(rtyp)),
                                float(conv_to_e(rfs)),
                                float(conv_to_e(q)),
                                float(conv_to_e(dq)),
                                float(conv_to_e(br)),
                                float(conv_to_e(dbr)),
                            )
                        )
                else:
                    continue
    pass


"""
read simple format of decay data (same format as Oyak uses)
"""
def read_decay_data():
    from config import (
        DEFAULT_DECAY_FILE,
        SUPER_LONG_LIVED,
        DEFAULT_SIGNIFICUNT_NUMBER,
        DEFAULT_LONG_LIVED,
    )

    with open(DEFAULT_DECAY_FILE) as f:
        ln = 1
        lines = f.readlines()

    """ 
    dictionary containing all decay info 
    """
    decaydata = {}

    while lines:
        ELM = ""
        if ln >= len(lines):
            break

        decayinfo = []

        """ 
        read header of nuclide 
        100	read(12,*,end=1000)iz0,ia0,m0,T0,dT0,awr0,ndk0,nsp0,mat0
	    read(12,*)Eb0,dEb0,Eg0,dEg0,Ea0,dEa0
        """
        head = lines[ln]
        Z = head[0:5].strip()
        A = head[5:11].strip()
        ELM = ztoelem(int(Z))
        LIS = (
            head[10:16].strip().zfill(2)
        )  # ratio of the LIS state nuclide mass to that of neutron
        HL = head[17:31].strip()
        dHL = head[32:46].strip()
        NS = int(head[61:66].strip())  # number of decay mode

        nuclide = (
            str(Z) + "-" + ELM + "-" + str(A) + "-" + str(int(float(LIS))).zfill(2)
        )

        if HL == "0.0000000E+00":
            HL = SUPER_LONG_LIVED
            LAMBDA = signum_round(log(2) / float(HL), DEFAULT_SIGNIFICUNT_NUMBER)
        elif HL is not None:
            LAMBDA = signum_round(log(2) / float(HL), DEFAULT_SIGNIFICUNT_NUMBER)
        else:
            HL = SUPER_LONG_LIVED
            LAMBDA = signum_round(log(2) / float(HL), DEFAULT_SIGNIFICUNT_NUMBER)

        """ read energy """
        infon = lines[ln + 1]
        EB = infon[1:16].strip()
        dEB = infon[17:31].strip()
        EG = infon[32:46].strip()
        dEG = infon[47:61].strip()
        EA = infon[62:76].strip()
        dEA = infon[77:91].strip()

        """ read decay infor """
        decayinfo += lines[ln + 2 : ln + NS + 2]
        daughters = []
        DD = {}

        """ if the half life is longer than 1000 years, skip to read decay data """
        if float(HL) > DEFAULT_LONG_LIVED:
            EB, dEB, EG, dEG, EA, dEA = [0] * 6

        for decay in decayinfo:
            NUM = decayinfo.index(decay)
            RTYP = decay[
                1:16
            ].strip()  # 0 gamma, 1 beta, 2 ex, 3 IT, 4 alpha, 5 n, 6 SF, 7 proton, 10 unknown
            RFS = decay[17:30].strip()  # isomeric state flag for daughter nuclide
            Q = decay[31:46].strip()
            dQ = decay[47:61].strip()
            BR = decay[61:76].strip()
            dBR = decay[77:91].strip()

            daughterZ, daughterA = calc_daughter(float(RTYP), int(Z), int(A))
            daughterELM = ztoelem(int(daughterZ))

            if RFS == "0.0000000E+00":
                ISO = ""
            elif RFS == "1.0000000E+00":
                ISO = "M1"
            elif RFS == "2.0000000E+00":
                ISO = "M2"
            elif RFS == "3.0000000E+00":
                ISO = "M3"
            else:
                ISO = "UNKNOWN"

            # in case of spontanious fission, set product "FP"
            if float(RTYP) == 6.0:
                daughter = "FP"
            else:
                daughter = (
                    str(daughterZ)
                    + "-"
                    + daughterELM
                    + "-"
                    + str(daughterA)
                    + "-"
                    + str(int(float(RFS))).zfill(2)
                )

            daughters += [daughter]
            DD.update(
                {
                    NUM: {
                        "RTYP": RTYP,
                        "RFS": RFS,
                        "Q": Q,
                        "BR": BR,
                        "DAUGHTER": daughter,
                    }
                }
            )

        decaydata.update(
            {
                nuclide: {
                    "Z": Z,
                    "ELM": ELM,
                    "MASS": A,
                    "LIS": LIS,
                    "HL": HL,
                    "LAMBDA": LAMBDA,
                    "En_beta": EB,
                    "En_gamm": EG,
                    "En_alpha": EA,
                    "DecayInfo": DD,
                    "daughters": daughters,
                }
            }
        )

        ln = ln + 1 + NS + 1

    # print (json.dumps(decaydata, indent=2))

    with open("decaydata.json", "w") as f:
        json.dump(decaydata, f, indent=2)
    return decaydata


#  \u03B1 	α 	GREEK SMALL LETTER ALPHA
#  \u03B2 	β 	GREEK SMALL LETTER BETA
#  \u03B3 	γ 	GREEK SMALL LETTER GAMMA
#  \u03B4 	δ 	GREEK SMALL LETTER DELTA


def rtyp_to_mode(RTYP):
    if RTYP == 1.0:
        return '\u03B2' + '-'
    elif RTYP == 1.1:
        return ('double ' + '\u03B2' + '-')
    elif RTYP == 1.4:
        return '\u03B2' + '- +' + '\u03B1'
    elif RTYP == 1.5:
        return '\u03B2' + '-' + '+ n'
    elif RTYP == 1.55:
        return '\u03B2' + '-' + '+ 2n'
    elif RTYP == 1.555:
        return '\u03B2' + '-' + '+ 3n'
    elif RTYP == 1.5555:
        return '\u03B2' + '-' + '+ 4n'
    elif RTYP == 2.0:
        return '\u03B2' + '+'
    elif RTYP == 2.2:
        return '\u03B2' + '+'
    elif RTYP == 2.4:
        return '\u03B2' + '+ +' + '\u03B1'
    elif RTYP == 2.7:
        return '\u03B2' + '+ +' + 'p'
    elif RTYP == 2.77:
        return '\u03B2' + '+ +' + '2p'
    elif RTYP == 2.777:
        return '\u03B2' + '+ +' + '3p'
    elif RTYP == 3.0:
        return 'IT'
    elif RTYP == 3.4:
        return 'IT' + '+' + '\u03B1'
    elif RTYP == 4.0:  # alhpha
        return '\u03B1'
    elif RTYP == 5.0:
        return 'n'
    elif RTYP == 5.5:
        return '2n'
    elif RTYP == 5.55:
        return '3n'
    elif RTYP == 7.0:
        return 'p'
    elif RTYP == 7.7:
        return '2p'
    else:
        return ""

def calc_daughter(RTYP, Z, A):
    if RTYP == 1.0:
        return Z + 1, A
    elif RTYP == 1.1:
        return Z + 2, A
    elif RTYP == 1.4:
        return Z - 1, A - 4
    elif RTYP == 1.5:
        return Z + 1, A - 1
    elif RTYP == 1.55:
        return Z + 1, A - 2
    elif RTYP == 1.555:
        return Z + 1, A - 3
    elif RTYP == 1.5555:
        return Z + 1, A - 4
    elif RTYP == 2.0:
        return Z - 1, A
    elif RTYP == 2.2:
        return Z - 2, A
    elif RTYP == 2.4:
        return Z - 3, A - 4
    elif RTYP == 2.7:
        return Z - 2, A - 1
    elif RTYP == 2.77:
        return Z - 3, A - 2
    elif RTYP == 2.777:
        return Z - 4, A - 3
    elif RTYP == 3.0:
        return Z, A
    elif RTYP == 3.4:
        return Z - 2, A - 4
    elif RTYP == 4.0:  # alhpha
        return Z - 2, A - 4
    elif RTYP == 5.0:
        return Z, A - 1
    elif RTYP == 5.5:
        return Z, A - 2
    elif RTYP == 5.55:
        return Z, A - 3
    elif RTYP == 7.0:
        return Z - 1, A - 1
    elif RTYP == 7.7:
        return Z - 2, A - 2
    else:
        return Z, A



decaydata = read_decay_data()

from config import DEFAULT_SIGNIFICUNT_NUMBER, SUPER_LONG_LIVED
class DecayData:
    def __init__(self, nuclide=None, decaymode=None):

        self.nuclide = nuclide  # 40-Zr-99-00  without 0 fill
        self.decaymode = decaymode
        if decaydata.get(self.nuclide) is not None:
            self.decayinfo = decaydata[self.nuclide]["DecayInfo"]
            self.daughters = decaydata[self.nuclide]["daughters"]
            self.halflife = decaydata[self.nuclide]["HL"]
            self.lmbd = decaydata[self.nuclide]["LAMBDA"]
            self.ebeta = decaydata[self.nuclide]["En_beta"]
            self.egamm = decaydata[self.nuclide]["En_gamm"]
            self.ealp = decaydata[self.nuclide]["En_alpha"]
        else:
            self.daughters = []
            self.decayinfo = ""
            self.halflife = SUPER_LONG_LIVED
            # if self.halflife != None:
            self.lmbd = float(
                signum_round(log(2) / float(self.halflife), DEFAULT_SIGNIFICUNT_NUMBER)
                or log(2) / float(SUPER_LONG_LIVED)
            )
            # else:
            #     self.lmbd = None
            self.ebeta = 0.0
            self.egamm = 0.0
            self.ealp = 0.0

    def __repr__(self) -> str:
        info = "Nuclide: " + self.nuclide + ", decay info: " + self.decayinfo
        return info

    def get_ndm(self):  # number of decay mode
        if decaydata.get(self.nuclide) is not None:
            return len(decaydata[self.nuclide]["DecayInfo"])
        else:
            return 0

    def get_halflife(self):
        return self.halflife

    def get_halflife_formatted(self):
        year = (365 * 24 * 60 * 60)
        day = (24 * 60 * 60)
        hour = (24 * 60)
        minnute = (60)
        second = (60)

        if self.halflife == SUPER_LONG_LIVED:
            return "Long"

        if float(self.halflife) > year:
            return "{:2.1E} y".format(float(self.halflife) / year)

        elif float(self.halflife) > day:
            return "{:2.2f} d".format(float(self.halflife) / day)

        elif float(self.halflife) > hour:
            return "{:2.2f} h".format(float(self.halflife) / hour)

        elif float(self.halflife) > minnute:
            return "{:2.2f} m".format(float(self.halflife) / minnute)

        elif float(self.halflife) <= second:
            return "{:2.2f} sec".format(float(self.halflife) )

        else:
            return ""




    def get_lambda(self):
        return self.lmbd

    def get_daughters(self):  # specific mode
        """
        e.g. "39-Y-97-00": ["40-Zr-97-00","40-Zr-96-00"]
        """
        return self.daughters

    def get_ebeta(self):
        return self.ebeta

    def get_egamm(self):
        return self.egamm

    def get_ealpha(self):
        return self.ealp

    def get_decayinfo(self):
        return self.decayinfo

    def gen_diagram(self):
        fig = ""
        return fig

    def get_decaymodes(self):  # all decay modes
        modes = []
        # try:
        for n in range(self.get_ndm()):
            modes += [ decaydata[self.nuclide]["DecayInfo"][n]["RTYP"] ]
        # except:
        #     modes = []
        return modes

    def get_progonies(self):
        return progenies(self.nuclide)

    def get_decaymode(self, nd):  # specific mode
        return decaydata[self.nuclide]["DecayInfo"][nd]

    def get_rtyp(self, nd):
        return decaydata[self.nuclide]["DecayInfo"][nd]["RTYP"]

    def get_branchingratio(self, nd):
        return decaydata[self.nuclide]["DecayInfo"][nd]["BR"]

    def get_qvalue(self, nd):
        return decaydata[self.nuclide]["DecayInfo"][nd]["Q"]

    def get_next(self, nd):  # specific mode
        return decaydata[self.nuclide]["DecayInfo"][nd]["DAUGHTER"]


def gen_chains(chains, brs, rtyps, nuk, count=0):
    from config import MAX_NUMBER_IN_CHAIN

    """
    generate decay chains from the given(nuk) and first daugther nuclides
    """

    inside = chains[-1]
    inside_br = brs[-1]
    inside_rtyp = rtyps[-1]

    # loop counter
    count += 1

    dd = DecayData(nuk)
    dau = dd.get_daughters()
    ndm = dd.get_ndm()

    for d in dau:
        rtyp = float(dd.get_rtyp(dau.index(d)))
        br = float((dd.get_branchingratio(dau.index(d))))

        # spontaneous fission
        if d == nuk:
            break

        if dau.index(d) > 0:
            inside = copy.deepcopy(chains[-1][:count])
            inside.append(d)

            inside_br = copy.deepcopy(brs[-1][:count])
            inside_br.append(br)

            inside_rtyp = copy.deepcopy(rtyps[-1][:count])
            inside_rtyp.append(rtyp)

        if dau.index(d) == 0:
            inside.append(d)
            inside_br.append(br)
            inside_rtyp.append(rtyp)

        if inside not in chains:
            chains.append(inside)
            brs.append(inside_br)
            rtyps.append(inside_rtyp)

        chains, brs, rtyps = gen_chains(chains, brs, rtyps, d, count)

        inside = []
        inside_br = []
        inside_rtyp = []

        if count > MAX_NUMBER_IN_CHAIN:
            break

        if ndm == 0:
            break

    inside = []
    inside_br = []
    inside_rtyp = []

    return chains, brs, rtyps


def decaychain(nuclide):
    """
    use for the decay heats calculations
    """
    count = 0
    chains = []
    brs = []
    rtyps = []
    pp = DecayData(nuclide)

    # get first daughters from the independent product and loop over them to generate all possible decay chain as lists
    dau = pp.get_daughters()
    if dau is None:
        next
    else:
        dd_dict = {}
        for d in dau:
            rtyp = float(pp.get_rtyp(dau.index(d)))
            br = float(pp.get_branchingratio(dau.index(d)))
            """
            main process to call decay data for the 
            chain from the first daughter such as branching ratios, decay type
            """
            chains, brs, rtyps = gen_chains([[d]], [[br]], [[rtyp]], d)

            for j, chain in enumerate(chains):
                count += 1
                lmbds = []
                en_betas = []
                en_gamms = []
                en_alphas = []
                lmbds.append(pp.get_lambda())
                en_betas.append(pp.get_ebeta())
                en_gamms.append(pp.get_egamm())
                en_alphas.append(pp.get_ealpha())

                # append releasing energy from daughters
                for c in chain:
                    cc = DecayData(c)
                    en_beta = cc.get_ebeta()
                    en_gamm = cc.get_egamm()
                    en_alpha = cc.get_ealpha()
                    lmbd = cc.get_lambda()
                    if chain.index(c) + 1 >= len(chain):
                        cc_rtyp = 9999
                    else:
                        cc_rtyp = rtyps[j][chain.index(c) + 1]

                    lmbds.append(lmbd)
                    if 1.0 <= cc_rtyp <= 3.0 and cc_rtyp not in [3.4, 2.4, 1.4]:
                        # beta decay
                        en_betas.append(en_beta)
                        en_gamms.append(en_gamm)
                        en_alphas.append(0.0)
                    elif cc_rtyp == 4.0:
                        # alpha decay
                        en_betas.append(0.0)
                        en_gamms.append(en_gamm)
                        en_alphas.append(en_alpha)
                    elif cc_rtyp in [3.4, 2.4, 1.4]:
                        # alpha decay
                        en_betas.append(en_beta)
                        en_gamms.append(en_gamm)
                        en_alphas.append(en_alpha)
                    else:
                        en_betas.append(0.0)
                        en_gamms.append(en_gamm)
                        en_alphas.append(0.0)
                # this dictionary contains nuclide in chain and branching ratios for daughters only,
                # and lambda and decay energies contain parent (independent product)
                dd_dict[count] = {
                    "chain": chain,
                    "branching": brs[j],
                    "rtyp": rtyps[j],
                    "lmbds": lmbds,
                    "en_betas": en_betas,
                    "en_gamms": en_gamms,
                    "en_alphas": en_alphas,
                }
    return dd_dict


def progenies(nuclide):
    from config import MAX_NUMBER_IN_CHAIN

    """ first daughters """
    pp = DecayData(nuclide)
    dau = pp.get_daughters()
    count = 0

    chain1 = {}
    chain1[nuclide] = dau

    queue = deque(dau)  # ['38-Sr-100-00', '38-Sr-99-00', '38-Sr-98-00']
    chain2 = {}
    # store the unique decay products that is in the chain from the same parent
    """ first daughter(s) """
    while queue:
        # chain3 = {}  # store the complete chain from the first daughters
        dchain = []
        # print(queue[0])
        da = DecayData(queue[0])
        dchain = da.get_daughters()
        chain2[queue[0]] = dchain
        # chain3[queue[0]] = dchain

        """ first daughter's daugther's daughter's... """
        dqueue = deque(dchain)
        while dqueue:
            dchain2 = []
            dda = DecayData(dqueue[0])
            for p in range(dda.get_ndm()):
                dchain2 += [dda.get_next(int(p))]
                dqueue.append(dda.get_next(int(p)))

            if chain2.get(dqueue[0]) is None:
                chain2[dqueue[0]] = dchain2

            # chain3[dqueue[0]] = dchain2

            # fix position, dont move
            dqueue.popleft()

            """ break if chain length is more than config """
            count += 1
            if count > MAX_NUMBER_IN_CHAIN:
                dqueue = []

        # fix position, dont move
        queue.popleft()

        """ return dictionary with all progonies """
        progs_dict = {**chain1, **chain2}
    # print(" chain3: ", chain3)
    return progs_dict

