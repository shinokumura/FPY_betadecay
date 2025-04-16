from pathlib import Path

""" cut off time of HL when cumulative yield is calculated"""
DEFAULT_LONG_LIVED = 1000.0 * 365 * 24 * 60 * 60  # 1,000 years

""" used for the nuclides whose HL are not known """
SUPER_LONG_LIVED = 1.0e50

""" max number of nuclides in one chain """
MAX_NUMBER_IN_CHAIN = 100
MAX_NUMBER_IN_DIAGRAM = 20

""" cut off of yield """
SMALLEST_YIELD_CONSIDERED = 1.0e-50

""" signigicunt number """
DEFAULT_SIGNIFICUNT_NUMBER = 5

""" TALYS FPY data """
TALYS_FPY_FILE = "Sample_FPY_Files/pu239_yieldZA1.00E-06.fis.gef"
# TALYS_FPY_FILE = "sample/conv_fpy_endfb71.dat"
# TALYS_FPY_FILE = "sample/conv-fpy_U235_JENDL4.0.dat"

DEFAULT_DECAYDATA = "ENDF8.1"

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DECAY_DATA_LIBS = {
    "ENDF7.1": {
        "ENDF-6": "/Users/okumuras/Documents/nucleardata/ENDF/ENDFdecay/",
        "SimpleENDF": f"{BASE_DIR}/DecayData/SimpleENDF/ENDFDD-BVII1.py.dat",
        "JSON": f"{BASE_DIR}/DecayData/JSON/ENDFDD-BVII1.json",
    },
    "ENDF8.1": {
        "ENDF-6": "/Users/okumuras/Documents/nucleardata/ENDF/decay-version.VIII.1/",
        "SimpleENDF": f"{BASE_DIR}/DecayData/SimpleENDF/ENDFDD-B8.1.py.dat",
        "JSON": f"{BASE_DIR}/DecayData/JSON/ENDFDD-B8.1.json",
    },
    "JENDL2015": {
        "ENDF-6": "/Users/okumuras/Documents/nucleardata/JENDL/jendl-ddf-2015/",
        "SimpleENDF": f"{BASE_DIR}/DecayData/SimpleENDF/JENDL2015DD.py.dat",
        "JSON": f"{BASE_DIR}/DecayData/JSON/JENDL2015DD.json",
    },
    "JEFF3.3": {
        "ENDF-6": "/Users/okumuras/Documents/nucleardata/JEFF33-rdd/",
        "SimpleENDF": f"{BASE_DIR}/DecayData/SimpleENDF/JEFF33DD.py.dat",
        "JSON": f"{BASE_DIR}/DecayData/JSON/JEFF33DD.json",
    },
    "JENDL5.0": {
        "ENDF-6": "/Users/okumuras/Documents/nucleardata/JENDL/jendl5-dec_upd3/",
        "SimpleENDF": f"{BASE_DIR}/DecayData/SimpleENDF/JENDL5.0.py.dat",
        "JSON": f"{BASE_DIR}/DecayData/JSON/JENDL5.0.json",
    },
}


""" time(s) for time dependent calculations """
DECAY_HEAT_CALC_TIME = [
    4.00e-01,
    6.00e-01,
    1.00e00,
    2.00e00,
    4.00e00,
    6.00e00,
    1.00e01,
    2.00e01,
    4.00e01,
    6.00e01,
    1.00e02,
    2.00e02,
    4.00e02,
    6.00e02,
    1.00e03,
    2.00e03,
    4.00e03,
    6.00e03,
    1.00e04,
    2.00e04,
    4.00e04,
]
