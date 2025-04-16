"""
beta decay calculation from the independent FPY data
"""
import os
import argparse
import pathlib

from fpy_betadecay.config import DECAY_DATA_LIBS

from fpy_betadecay.scripts.decay_data import convert_ddlibrary, DecayData
from fpy_betadecay.scripts.decay_observables import calc_decay_heat, calc_cumlative_fpy

import logging
logging.basicConfig(filename="process.log", level=logging.ERROR, filemode="w")


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def cli():
    parser = argparse.ArgumentParser(
        prog="Beta Decay Calculator from Fission Product Yield Data File",
        add_help=False,
    )

    parser.add_argument(
        "-conv",
        "--convert",

        choices=[k for k in DECAY_DATA_LIBS.keys()],
        help="Convert ENDF-6 format Decay Data into JSON.",
    )

    parser.add_argument(
        "-calc",
        "--calculate",
        type=pathlib.Path,
        help="File path to the TALYS Independent FPY file to calculate decay heat and cumulative yield",
    )

    parser.add_argument(
        "-dd",
        "--decaydata",
        choices=[k for k in DECAY_DATA_LIBS.keys()],
        help="Name of decay data used in the beta-decay calculations.",
    )

    args = parser.parse_args()

    # print(args)

    if args.convert:
        convert_ddlibrary(args.convert)

    if args.calculate:
        """init decay data"""
        DecayData.load_decay_data(args.decaydata)

        """run calculations"""
        calc_decay_heat(args.decaydata, args.calculate)
        calc_cumlative_fpy(args.decaydata, args.calculate)


if __name__ == "__main__":
    cli()

    # if CHAIN_PLOT:
    #     from decay_chain import *
    #     nuclide = "82-Pb-211-00"
    #     diagram(nuclide)
