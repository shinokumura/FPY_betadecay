""" cut off time of HL when cumulative yield is calculated"""
DEFAULT_LONG_LIVED = 1000.0 * 365 * 24 * 60 * 60  # 1000 years
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
TALYS_FPY_FILE = "sample/yieldZA1.00E-06.fis"
# TALYS_FPY_FILE = "sample/conv_fpy_endfb71.dat"
# TALYS_FPY_FILE = "sample/conv-fpy_U235_JENDL4.0.dat"

""" true if cumulative yield is calculated """
CUMLATIVE = False

""" true if decay data need to be converted into simple format """
CONVERT = False
DECAY_DATA_LIB_PATH_ENDF = "/Users/okumuras/Documents/nucleardata/ENDF/ENDFdecay/"
DECAY_DATA_LIB_PATH_JEFF = "/Users/okumuras/Documents/nucleardata/JEFF33-rdd/"
DECAY_DATA_LIB_PATH_JENDL = ("/Users/okumuras/Documents/nucleardata/JENDL/jendl-ddf-2015/")
DECAY_DATA_LIB_PATH = DECAY_DATA_LIB_PATH_ENDF

""" true if the time dependent decay heats and delayed neutron yield are calculated """
DECAYHEAT = True

""" simple format (Oyak format) of the decay data library file to be used in the calculation """
# DEFAULT_DECAY_FILE = "../DecayData/ENDFDD-BVII1.py.dat"
# DEFAULT_DECAY_FILE = "../DecayData/JEFF33DD.py.dat"
DEFAULT_DECAY_FILE = "../DecayData/JENDL2015DD.py.dat"
# DEFAULT_DECAY_FILE = "../Oyak/JENDLFPD2011.dat"
# DEFAULT_DECAY_FILE = "../Oyak/JENDLFPD2015.dat"
# DEFAULT_DECAY_FILE = "../Oyak/ENDFDD-BVII1.dat"

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
