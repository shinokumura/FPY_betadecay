import copy

from scripts.decay_data import DecayData
from config import MAX_NUMBER_IN_CHAIN

def gen_chains(decaydataname, chains, brs, rtyps, nuk, depth=0):
    """
    generate decay chains from the given(nuk) and first daugther nuclides
    """

    inside = chains[-1]
    inside_br = brs[-1]
    inside_rtyp = rtyps[-1]

    depth += 1

    dd = DecayData(nuk, decaydataname)
    daughters = dd.get_daughters()
    ndm = dd.get_ndm()

    for idx, daughter in enumerate(daughters):
        rtyp = float(dd.get_rtyp(idx))
        br = float((dd.get_branchingratio(idx)))

        # spontaneous fission
        if daughter == nuk:
            break

        if idx > 0:
            inside = copy.deepcopy(chains[-1][:depth])
            inside.append(daughter)

            inside_br = copy.deepcopy(brs[-1][:depth])
            inside_br.append(br)

            inside_rtyp = copy.deepcopy(rtyps[-1][:depth])
            inside_rtyp.append(rtyp)

        if idx == 0:
            inside.append(daughter)
            inside_br.append(br)
            inside_rtyp.append(rtyp)

        if inside not in chains:
            chains.append(inside)
            brs.append(inside_br)
            rtyps.append(inside_rtyp)

        chains, brs, rtyps = gen_chains(decaydataname, chains, brs, rtyps, daughter, depth)

        inside = []
        inside_br = []
        inside_rtyp = []

        if depth > MAX_NUMBER_IN_CHAIN:
            break

        if ndm == 0:
            break

    inside = []
    inside_br = []
    inside_rtyp = []

    return chains, brs, rtyps



def decaychain(nuclide, decaydataname):
    """
    use for the decay heats calculations
    """
    depth = 0
    chains = []
    brs = []
    rtyps = []
    pp = DecayData(nuclide, decaydataname)

    # get first daughters from the independent product and loop over them to generate all possible decay chain as lists
    daughters = pp.get_daughters()
    if daughters is None:
        return {}
    
    dd_dict = {}

    for idx, daughter in enumerate(daughters):
        rtyp = float(pp.get_rtyp(idx))
        br = float(pp.get_branchingratio(idx))
        """
        main process to call decay data for the 
        chain from the first daughter such as branching ratios, decay type
        """
        chains, brs, rtyps = gen_chains(decaydataname, [[daughter]], [[br]], [[rtyp]], daughter)

        for j, chain in enumerate(chains):
            depth += 1
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
                cc = DecayData(c, decaydataname)
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
            dd_dict[depth] = {
                "chain": chain,
                "branching": brs[j],
                "rtyp": rtyps[j],
                "lmbds": lmbds,
                "en_betas": en_betas,
                "en_gamms": en_gamms,
                "en_alphas": en_alphas,
            }
    return dd_dict



if __name__ == "__main__":
    # nuclide = "37-Rb-93-00"
    # nuclide = "55-Cs-141-00"
    # nuclide = "86-Rn-222-00"
    # nuclide = "92-U-235-00"
    # nuclide = "91-Pa-231-00"
    nuclide = "37-Rb-93-00"
    decaychain(nuclide, "ENDF8.1")
