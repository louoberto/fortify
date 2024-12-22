from read_file import read_file
from convert_line_breaks import convert_line_breaks
from processcommentsandcasing import processCommentsAndCasing
# from sort_vars import sortaVars
# from processparens import processParens
# from processnesting import processNesting
# from processdatatypes import processDatatypes
# from processIfs import processIfStatements
# from processIfs import processIfs2
# from processIfs import preprocessIfs3
# from lineup_f90_line_continuations import lineup_f90_line_continuations
# from find_defines import find_defines
# from preprocessor_whitespace import preprocessor_whitespace
# from process_preprocessor_directives import process_preprocessor_directives
# from hangingSpaces import hangingSpaces
# from globetrot import globetrot
# from repeaters import repeaters
# from format_params_saves import format_params_saves
# from param_save_comma import param_save_comma
# from print_file import print_file
# from tabsToSpaces import tabsToSpaces
# from processHangingEnds import processHangingEnds
# from processColumns import processColumns
# from processIncludes import processIncludes



class fortify:
    # Constructor to initialize object attributes
    def __init__(self):
        self.read_file = read_file
        self.convert_line_breaks = convert_line_breaks
        self.processCommentsAndCasing = processCommentsAndCasing

        #     lynes, noSortName = processCommentsAndCasing(lynes, noSortName, True, f90)
#     lynes = tabsToSpaces(lynes)
#     lynes = processDatatypes(lynes, f90)
#     lynes = processIfStatements(lynes)
#     lynes = processParens(lynes)
#     lynes = processIfs2(lynes)
#     lynes = processHangingEnds(lynes)
#     lynes = preprocessIfs3(lynes)
#     lynes = processNesting(lynes, f90)
#     lynes = processColumns(lynes, f90)
#     lynes = processNesting(lynes, f90)
#     lynes = processIncludes(lynes)
#     lynes = format_params_saves(lynes, common=True)
#     lynes = sortaVars(lynes, noSortName, f90)
#     # ---------------------------------------------------------------
#     # Turning this off for now. Seems to cause an issue whereby it keeps adding in commas
#     # ---------------------------------------------------------------
#     # lynes = param_save_comma( lynes )
#     # ================================================================
#     lynes = globetrot(lynes)
#     lynes = hangingSpaces(lynes)
#     lynes = process_preprocessor_directives(lynes)
#     lynes = processNesting(lynes, f90)
#     lynes = preprocessor_whitespace(lynes)
#     lynes = repeaters(lynes)
#     lynes = processColumns(lynes, f90)
#     lynes = processNesting(lynes, f90)
#     lynes = lineup_f90_line_continuations(lynes, f90)
#     if f90:
#         if lynes[-1][-1] != "\n":
#             lynes[-1] = lynes[-1] + "\n"
#             print("Added newline at end of file")
#     # Block together all variables, look for subroutine to make the change
#     # Continue to manage multiple declars on one line (dimensions, data statement blocks --> change to parameters )
#     # Handle potential unneccesary &'s by combining those lines for if-statements at least

#     print_file(lynes, fileName)