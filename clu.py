#!/usr/bin/env python3
# ==============================================================================
# Purpose:
# Format Fortran code to a standard, while allowing user input for a variety
# of styles
# ==============================================================================
import argparse
from fortify import fortify

spacing = 6  # First 6 cols go unused in most cases
spaceamp = 5
tab = 3
lastcol = 131  # Last usable column in Fortran
continuation_char = '&'
data_types = ["integer", "real", "complex", "character", "logical"] # Variable declartion types, referenced in multiple functions
comments = ['*', 'c', 'C', '!']
functions = ["subroutine", "function","program" ]  # Types of Fortran code blocks, used to identify the start and ending of function sections

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
        myfile = fortify(continuation_char, spacing, tab, spaceamp, lastcol, data_types, comments, functions)
        myfile.read_file(myfile, fortran_file)
        myfile.convert_line_breaks(myfile)
        myfile.lowercasing(myfile)
        myfile.convert_comment_char(myfile)
        myfile.tab_to_spaces(myfile)

