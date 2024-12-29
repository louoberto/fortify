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
