from math import exp

from fpy_betadecay.config import SMALLEST_YIELD_CONSIDERED, DEFAULT_SIGNIFICUNT_NUMBER
from fpy_betadecay.scripts.utilities import signum_round


def singledecay(lmbd, N0, t=20):
    return N0 * exp(-lmbd * t)


def bateman_solver(lmbds, Y0=1.0, t=20):
    """
    inputs
    lmbds: lambdas of all nuclides in the chain
    Y0: initial fraction
    t: time period in sec
    """
    n = len(lmbds)
    X = [None] * n
    lmbd_product = 1.0
    for i in range(n):
        if i > 0:
            lmbd_product *= lmbds[i - 1]
        xi = 0.0
        for k in range(i + 1):
            if lmbds[k] == None:
                continue
            denominator = 1.0
            for l in range(i + 1):
                if lmbds[l] == None:
                    continue
                if l == k:
                    continue
                if lmbds[l] == lmbds[k]:
                    lmbds[k] *= 0.0001

                denominator *= lmbds[l] - lmbds[k]

            xi += lmbd_product / denominator * exp(-lmbds[k] * t) * Y0

        if xi < 0.00 or xi < SMALLEST_YIELD_CONSIDERED:
            xi = SMALLEST_YIELD_CONSIDERED

        X[i] = signum_round(xi, DEFAULT_SIGNIFICUNT_NUMBER)

    if abs(1 - Y0 / sum(X)) > 1.0:
        print(
            "  initial fraction",
            Y0,
            "is not conserved-->",
            signum_round(sum(X), 5),
            "deviation:",
            signum_round(abs(1 - Y0 / sum(X)), 5),
        )
        pass
    else:
        # print(Y0, " initial independent yield conserved-->", signum_round(sum(X),5))
        pass

    return X


if __name__ == "__main__":
    bateman_solver([6.3200003e-01, 1.0, 0.88499999, 0.99996299])
