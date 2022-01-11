# read TALYS fission yield file

from config import TALYS_FPY_FILE
from elem import ztoelem
from utilities import slices

"""
read TALYS FPY file: yieldZAxxxE-xx.fis file
"""


def read_fpy_data():
    with open(TALYS_FPY_FILE) as f:
        lines = f.readlines()
    ind = {}

    for line in lines:
        if not line.startswith("#"):
            z, a, iso, fpy = slices(line, 5, 5, 3, 15)
            elem = ztoelem(int(z.strip()))
            if int(iso.strip()) > 0:
                product = (
                    str(z.strip())
                    + "-"
                    + elem
                    + "-"
                    + str(a.strip())
                    + "-"
                    + str(iso.strip()).zfill(2)
                )
            else:
                product = str(z.strip()) + "-" + elem + "-" + str(a.strip()) + "-00"
            ind[product] = float(fpy)
    return ind


""" 
convert beoh format FPY data into talys format 
"""


def convert_beof_fpy_data():
    with open("tmpFPY.txt") as f:
        lines = f.readlines()[3:]
    ind = {}

    for line in lines:
        _, z, h, a, _, iso, fpy, cum = slices(line, 7, 3, 1, 3, 3, 3, 12, 14)
        elem = ztoelem(int(z.strip()))
        if int(iso.strip()) > 0:
            product = (
                str(int(z)).strip()
                + "-"
                + elem
                + "-"
                + str(int(a)).strip()
                + "-"
                + str(iso.strip()).zfill(2)
            )
        else:
            product = (
                str(int(z)).strip() + "-" + elem + "-" + str(int(a)).strip() + "-00"
            )

        ind[product] = "{:.4E}".format(float(fpy))

        print("{:5d}{:5d}{:3d}{:15.4e}".format(int(z), int(a), int(iso), float(fpy)))
    return ind


"""
convert FPY data library by DeCE code and convert again into TALYS format
"""


def convert_fpy_lib_data():
    # run
    with open("sample/JENDL_U235.dat") as f:
        lines = f.readlines()
    ind = {}

    for line in lines:
        if not line.startswith("#"):
            z, a, iso, fpy, dfpy = slices(line, 7, 7, 14, 14, 14)
            elem = ztoelem(int(z.strip()))
            if int(float(iso.strip())) > 0:
                product = (
                    str(int(z)).strip()
                    + "-"
                    + elem
                    + "-"
                    + str(int(a)).strip()
                    + "-"
                    + str(iso.strip()).zfill(2)
                )
            else:
                product = (
                    str(int(z)).strip() + "-" + elem + "-" + str(int(a)).strip() + "-00"
                )

            ind[product] = "{:.4E}".format(float(fpy))

            print(
                "{:5d}{:5d}{:3d}{:15.4e}".format(
                    int(z), int(a), int(float(iso.strip())), float(fpy)
                )
            )
    return ind


class FY:
    def __init__(self, ff=None, decaymode=None, y1=None):
        self.ff = ff  # nuclide
        self.y1 = y1

    def get_ffy(self):
        return self.y1

    def add_yield(self, addy):
        return addy


if __name__ == "__main__":
    convert_fpy_lib_data()
