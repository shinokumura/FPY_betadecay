# read TALYS fission yield file


from fpy_betadecay.scripts.elem import ztoelem
from fpy_betadecay.scripts.utilities import slices

"""
read TALYS FPY file: yieldZAxxxE-xx.fis file
"""
def read_fpy_data(TALYS_FPY_FILE):
    if not TALYS_FPY_FILE:
        from config import TALYS_FPY_FILE
        
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


def convert_beoh_fpy_data():
    # Convert beoh output to TALYS FPY format
    with open("FPY.txt") as f:
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


def convert_fpy_lib_data(filename):
    # Convert Sameple_FPY_files/JENDL4.0_U235.dat (DeCE output) to TALYS FPY format
    with open(filename) as f:
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


if __name__ == "__main__":
    convert_fpy_lib_data()
