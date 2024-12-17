# ===========================================================
def processColumns(lynes, f90):
    """
    Processes multiple varaibles declared on a single line (i think)
    """
    lastcol = 131  # Last usable column in Fortran
    new_lynes = []
    for lyne in lynes:
        skip = False
        lineCont = False
        # Now we process multiple variables declared on a single line, as well as
        # handling variables that didn't space properly
        commenter = False
        comloc = 0
        for jtr, char in enumerate(lyne.rstrip()):
            if char == "!":
                skip = True
            elif char == " ":
                ktr = jtr + 1
                while lyne[ktr] == " ":  # Keep looking until we find a non-space value
                    ktr = ktr + 1
                if lyne[ktr] == "!":  # Then we have a comment after ktr spaces.
                    skip = True
            if not skip:
                if char == '"' or char == "'":
                    commenter = True
                    comloc = jtr
                elif char == '"' or char == "'":  # I'm not sure this makes sense....
                    commenter = False
                if jtr > lastcol and not f90:
                    lineCont = True
                    skip = True  # We know we have to bump over to the next, so no need to be in here anymore
        if lineCont:  # then we need to find a good place to stop this line...
            # Let's find the first, last space and call it there...
            if (
                commenter
            ):  # unless it was a comment that went overboard, then send that to the next dye-mension!
                jtr = comloc
            else:
                jtr = lastcol
            if lyne[jtr] == " " or commenter:
                lyne1 = lyne[:jtr] + "\n"
                lyne2 = "& " + lyne[jtr:]
                new_lynes.append(lyne1)
                new_lynes.append(lyne2)
            else:
                while lyne[jtr] != " ":
                    jtr = jtr - 1
                    lyne1 = lyne[:jtr] + "\n"
                    lyne2 = "& " + lyne[jtr:]
                new_lynes.append(lyne1)
                new_lynes.append(lyne2)
        else:
            new_lynes.append(lyne)
    return new_lynes
