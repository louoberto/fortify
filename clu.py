#!/usr/bin/env python3
# ==============================================================================
# Function: driver
# Purpose:
# Format Fortran code to a standard
# ==============================================================================
import argparse
from fortify import fortify

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

    # File editing order
    #   1. Read file, store lines
    #   2. Start by removing any unnecessary whitespace
    #   3. Convert the comment character from F77 *,C,c to !
    #   4. Convert line break characters to be &
    #   5. Lowercase all normal code, except strings
    for fortran_file in fortran_files:
        myfile = fortify()
        myfile.read_file(myfile, fortran_file)
        myfile.convert_comment_char(myfile)
        myfile.common_format_template(myfile)
        myfile.structured_indent(myfile)
        # myfile.line_carry_over(myfile)
        # myfile.lineup_f90_line_continuations(myfile)


        myfile.print_file(myfile, fortran_file)

