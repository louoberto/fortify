#!/usr/bin/env python3
# ==============================================================================
# Function: driver
# Purpose:
# This is the entry point from the command line. It creates the object and calls
# all the class object functions.
# ==============================================================================
import argparse
from fortify import fortify


if __name__ == "__main__":
    # Arg parsing command line
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("filename", action="store", nargs="+", help="Path(s) to input file(s)")

    argz = parser.parse_args()
    fortran_files = argz.filename # Set of args supplied to us.
    for fortran_file in fortran_files:
        myfile = fortify()
        myfile.read_file(myfile, fortran_file)
        if myfile.free_form:
            myfile.last_col = 10000  # Last usable column in Fortran, as per the standard
        else:
            myfile.last_col = 72  # Last usable column in Fortran, as per the standard
        myfile.format(myfile)
        myfile.print_file(myfile, fortran_file)
