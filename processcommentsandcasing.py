from donotformat import doNotFormatCheck

def processCommentsAndCasing(lynes, noSortName, lowerCase, f90):
    """
    Cleans up code comments, makes sure all comments use ! instead of C. Makes code lowercase.
    """
    new_lynes = []
    stringer = False
    spacing = 6  # First 6 cols go unused in most cases
    # ===========================================================
    # Process each line of the file one at a time. If raw == given, store those lines.
    for lyne in lynes:
        # =======================
        # Convert starting comment lines to !
        if "C" in lyne[0].strip() and not f90:
            lyne = lyne[0 : lyne.find("C")] + "!" + lyne[lyne.find("C") + 1 :]
            lyne = " " * spacing + lyne
        elif "c" in lyne[0].strip() and not f90:
            lyne = lyne[0 : lyne.find("c")] + "!" + lyne[lyne.find("c") + 1 :]
            lyne = " " * spacing + lyne
        elif "*" in lyne[0].strip() and not f90:
            lyne = lyne[0 : lyne.find("*")] + "!" + lyne[lyne.find("*") + 1 :]
            lyne = " " * spacing + lyne
        elif "#" in lyne[0].strip():
            lyne = lyne.rstrip() + "\n"  # Don't change precompiler directives
        else:
            # ================================
            # Once comment characters are converted to !, make sure everything == tabbed over and made lowercase.
            cmt = lyne.find("!")
            if cmt != 0:  # A comment exists somewhere in the lyne
                temp = ""
                double_quote_count = 0
                single_quote_count = 0
                commenter = False
                for char in lyne:
                    # find start and end of character in code, " or '
                    if char == "'" and double_quote_count % 2 == 0:
                        # stringer = not stringer
                        single_quote_count += 1
                    elif char == '"' and single_quote_count % 2 == 0:
                        # stringer = not stringer
                        double_quote_count += 1

                    if (
                        single_quote_count % 2 == 0
                        and double_quote_count % 2 == 0
                        or doNotFormatCheck(lyne)
                    ):  # We are stll in string mode, don't change anything
                        if char == "!":  # we are in comment land, don't format
                            commenter = True
                        if lowerCase and not commenter:
                            temp = temp + char.lower()
                        else:
                            temp = temp + char
                    else:
                        temp = temp + char

                if "do not sort" in lyne:
                    noSortName = True
                lyne = temp
            else:  # the entire lyne == a comment
                if not f90:
                    lyne = " " * spacing + lyne

        # ^^^^^^^^^^^^^^Formatted the file up to comments and lowercasing ^^^^^^^^
        new_lynes.append(lyne)
    return new_lynes, noSortName
