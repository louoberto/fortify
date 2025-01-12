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
    parser.add_argument("--last_column_free_form", type=int, default=None, help="Line carry over: Last usable column in Fortran free form.")
    parser.add_argument("--last_column_fixed_form", type=int, default=None, help="Line carry over: Last usable column in Fortran fixed form.")
    parser.add_argument("--line_carry_over", type=bool, default=None, help="Line carry over formatting; when formatting runs past column limit")
    parser.add_argument("--lowercasing", type=bool, default=None, help="Lowercasing all code. If false, leaves case as is.")
    parser.add_argument("--comment_character", type=str, default=None, help="Fortran comment character")
    parser.add_argument("--continuation_character", type=str, default=None, help="Fortran fixed format continuation character")
    parser.add_argument("--comment_lines", type=str, default=None, help="How to treat comment-only lines")
    parser.add_argument("--tab_length", type=int, default=None, help="Fortran default tab length")


    args = parser.parse_args()
    fortran_files = args.filename  # Set of args supplied to us.

    last_column_free_form = args.last_column_free_form if args.last_column_free_form is not None else 10000
    last_column_fixed_form = args.last_column_fixed_form if args.last_column_fixed_form is not None else 72
    lowercasing = args.lowercasing if args.lowercasing is not None else True
    line_carry_over = args.line_carry_over if args.line_carry_over is not None else True
    comment_character = args.comment_character if args.comment_character is not None else '!'
    continuation_character = args.continuation_character if args.continuation_character is not None else '&'
    comment_lines = args.comment_lines if args.comment_lines is not None else 'first_column'
    tab_length = args.tab_length if args.tab_length is not None else 3


    for fortran_file in fortran_files:
        myfile = fortify()
        myfile.read_file(myfile, fortran_file)
        myfile.lowercasing = lowercasing
        myfile.do_carry_over = line_carry_over
        myfile.comment_behavior = comment_lines
        myfile.tab_length = tab_length
        if myfile.free_form:
            myfile.last_col = last_column_free_form
        else:
            myfile.last_col = last_column_fixed_form
            myfile.comment = comment_character
            myfile.continuation_char = continuation_character

        myfile.format(myfile)
        myfile.print_file(myfile, fortran_file)