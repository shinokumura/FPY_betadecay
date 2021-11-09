# read TALYS fission yield file

from config import TALYS_FPY_FILE
from elem import ztoelem


def slices(s, *args):
    position = 0
    for length in args:
        yield s[position:position + length]
        position += length

def read_fpy_data():
    with open (TALYS_FPY_FILE) as f:
        lines = f.readlines()[5:]
        # lines = f.readlines()
    ind = {}

    for line in lines:
        z, a, iso, fpy = slices(line, 5, 5, 3, 15)
        elem = ztoelem(int(z.strip()))
        if int(iso.strip()) > 0:
            product = str(z.strip()) + "-" + elem + "-" + str(a.strip()) + "-" + str(iso.strip()).zfill(2)
        else:
            product = str(z.strip()) + "-" + elem + "-" + str(a.strip()) + "-00"
        
        ind[product] = float(fpy)

    # for k, v in ind.items():
    #     ind[k] = float(v)
    # print(ind)
    return ind


class FY():
    def __init__(self, ff=None, decaymode=None, y1=None):
        self.ff = ff  # nuclide
        self.y1 = y1

    def get_ffy(self):
        return self.y1

    def add_yield(self, addy):
        return addy
