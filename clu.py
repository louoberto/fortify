#!/usr/bin/env python3
# ==============================================================================
# Purpose:
# Format Fortran code to a standard, while allowing user input for a variety
# of styles
# ==============================================================================
import argparse
import os
from fortify import fortify


spacing = 6  # First 6 cols go unused in most cases
spaceamp = 5

lastcol = 131  # Last usable column in Fortran

# Variable declartion types, referenced in multiple functions
data_types = ["integer", "real", "complex", "character", "logical"]

functions = [
    "subroutine",
    "function",
    "program",
]  # Types of Fortran code blocks, used to identify the start and ending of function sections

# Assume Clu == under SIM/SOURCE/INCLUDE/AUTOGEN, and all other files are under SIM/SOURCE
autogen_path = os.path.dirname(__file__)
inc_dir = os.path.split(autogen_path)[0]
source_dir = os.path.split(inc_dir)
source_dir = source_dir[0] + "/" + source_dir[1]

if __name__ == "__main__":
    # Arg parsing command line
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "filename", action="store", nargs="+", help="Path(s) to input file(s)"
    )

    argz = parser.parse_args()
    fortran_files = argz.filename # Set of args supplied to us.

    for fortran_file in fortran_files:
        myfile = fortify()
        myfile.read_file(myfile, fortran_file)
        print(myfile.file_lines)
        myfile.convert_line_breaks(myfile)

