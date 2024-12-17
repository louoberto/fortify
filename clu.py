#!/usr/bin/env python3
#==============================================================================
# Purpose:
# Format Fortran code to a standard, while allowing user input for a variety
# of styles
#==============================================================================
import argparse
import os
from sort_vars import sortaVars
from processparens import processParens
from processnesting import processNesting
from processdatatypes import processDatatypes
from processcommentsandcasing import processCommentsAndCasing
from processIfs import processIfStatements
from processIfs import processIfs2
from processIfs import preprocessIfs3
from readFile import read_file
from convert_line_breaks import convert_line_breaks
from lineup_f90_line_continuations import lineup_f90_line_continuations
from find_defines import find_defines
from preprocessor_whitespace import preprocessor_whitespace
from process_preprocessor_directives import process_preprocessor_directives
from hangingSpaces import hangingSpaces
from globetrot import globetrot
from repeaters import repeaters
from format_params_saves import format_params_saves
from param_save_comma import param_save_comma
from print_file import print_file
from tabsToSpaces import tabsToSpaces
from processHangingEnds import processHangingEnds
from processColumns import processColumns
from processIncludes import processIncludes

# ----------------------------------------------
# Define global variables used across multiple functions
# ----------------------------------------------
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

class formatted_file:
    # Constructor to initialize object attributes
    def __init__(self, filetype, text):
        self.filetype = filetype
        self.text = text
    
    # Method to display information
    # def greet(self):


# ==========================================================
def processCommons(fileName, noSortAll=False):
    """
    Process each common file
    """
    lynes = read_file(fileName)
    print("Formatting: " + fileName)
    noSortName = False
    lynes = convert_line_breaks(lynes, f90)
    lynes, noSortName = processCommentsAndCasing(lynes, noSortName, False)
    lynes = processDatatypes(lynes)
    # lynes = processIfStatements(lynes)
    # lynes = processParens(lynes)
    # lynes = processIfs2(lynes)
    # lynes = processHangingEnds(lynes)
    # lynes = preprocessIfs3(lynes)
    # lynes = processNesting(lynes,f90)
    # lynes = processColumns(lynes,f90)
    # lynes = processNesting(lynes,f90)
    # lynes = processIncludes(lynes)
    # lynes = format_params_saves( lynes, common = True)
    # if not noSortAll:
    #     lynes = sortaVars( lynes, noSortName )
    # lynes = param_save_comma( lynes )
    # lynes = globetrot(lynes)
    # lynes = hangingSpaces(lynes)
    # lynes = process_preprocessor_directives(lynes)
    # lynes = processNesting(lynes,f90)
    # lynes = preprocessor_whitespace(lynes)
    # lynes = repeaters(lynes)
    # lynes = processColumns(lynes,f90)
    # lynes = processNesting(lynes,f90)
    # Block together all variables, look for subroutine to make the change
    # Continue to manage multiple declars on one line (dimensions, data statement blocks --> change to parameters )
    # Handle potential unneccesary &'s by combining those lines for if-statements at least

    print_file(lynes, fileName)

# ==========================================================
def processFile(fileName, f90=True):
    """
    Process each file
    """
    
    print("Formatting: " + fileName)
    noSortName = False
    lynes = convert_line_breaks(lynes, f90)
    lynes, noSortName = processCommentsAndCasing(lynes, noSortName, True, f90)
    lynes = tabsToSpaces(lynes)
    lynes = processDatatypes(lynes, f90)
    lynes = processIfStatements(lynes)
    lynes = processParens(lynes)
    lynes = processIfs2(lynes)
    lynes = processHangingEnds(lynes)
    lynes = preprocessIfs3(lynes)
    lynes = processNesting(lynes, f90)
    lynes = processColumns(lynes, f90)
    lynes = processNesting(lynes, f90)
    lynes = processIncludes(lynes)
    lynes = format_params_saves(lynes, common=True)
    lynes = sortaVars(lynes, noSortName, f90)
    # ---------------------------------------------------------------
    # Turning this off for now. Seems to cause an issue whereby it keeps adding in commas
    # ---------------------------------------------------------------
    # lynes = param_save_comma( lynes )
    # ================================================================
    lynes = globetrot(lynes)
    lynes = hangingSpaces(lynes)
    lynes = process_preprocessor_directives(lynes)
    lynes = processNesting(lynes, f90)
    lynes = preprocessor_whitespace(lynes)
    lynes = repeaters(lynes)
    lynes = processColumns(lynes, f90)
    lynes = processNesting(lynes, f90)
    lynes = lineup_f90_line_continuations(lynes, f90)
    if f90:
        if lynes[-1][-1] != "\n":
            lynes[-1] = lynes[-1] + "\n"
            print("Added newline at end of file")
    # Block together all variables, look for subroutine to make the change
    # Continue to manage multiple declars on one line (dimensions, data statement blocks --> change to parameters )
    # Handle potential unneccesary &'s by combining those lines for if-statements at least

    print_file(lynes, fileName)

# ===========================================================
# Main
# ===========================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "filename", action="store", nargs="+", help="Path(s) to input file(s)"
    )
    argz = parser.parse_args()
    fileList = argz.filename

    # Process each file one at a time
    for fortran_file in fileList:
        if ".f" == fortran_file[-2:]:
            processFile(fortran_file, f90=False)
        elif ".f90" == fortran_file[-4:]:
            processFile(fortran_file)
        elif ".inc" == fortran_file[-4:] or ".cmn" == fortran_file[-4:]:
            processCommons(fortran_file)
        else: 
            print("ERROR: File format not recognized")
