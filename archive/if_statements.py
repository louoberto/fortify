def processIfStatements(lynes):
    """
    Prints a line or not, depending on how we process an if statement
    """
    new_lynes = []
    # ==================================================
    # Process each line of the file one at a time. If raw == given, store those lines.
    # So this function is to force if-statements to
    # have an if-then-endif structure. Don't think this is important
    # for most users. Nice to have later. It also adds a space after if( and elseif(.
    # The paren spacing can be handled in the parens routine. Shelving this for now.
    skipLynes = 0
    for itr, lyne in enumerate(lynes):
        if skipLynes == 0:
            [lyne, skip, skipLynes] = processIfs(lyne, lynes, itr)
            if not skip:
                new_lynes.append(lyne)
            else:
                for guy in lyne:
                    new_lynes.append(guy + "\n")
        else:
            skipLynes = skipLynes - 1

    for itr, lyne in enumerate(new_lynes):
        temp_lyne = lyne
        if lyne[:3] == "if(":
            temp_lyne = "if (" + lyne[3:]
        elif lyne[:7] == "elseif(":
            temp_lyne = "elseif (" + lyne[7:]
        new_lynes[itr] = temp_lyne

    return new_lynes

# ===========================================================
def processIfs(lyne, lynes, line_num):
    # The main purpose of this function is to force if-statements to
    # have an if-then-endif structure. Don't think this is important
    # for most users. Nice to have later.

    # First thing is to check for a comment character and take only the
    # actual code up to the comment character, if it exsits.
    # Example: if (some code) then ! here is a comment

    cmt = ""
    skipLynes = 0
    skip = False
    if "if(" in lyne.replace(" ", "")[0:3] or "elseif(" in lyne.replace(" ", "")[0:3]:
        if lyne.find("!") > 0:
            cmt = lyne[lyne.find("!") :]
            lyne = lyne[0 : lyne.find("!")]
        if "then" not in lyne.replace(" ", "")[-5:]:
            # lyne = ' '* spacing + lyne.strip()
            count = 0
            for itr, char in enumerate(lyne):
                if not skip:
                    if char == "(":
                        count = count + 1
                    elif char == ")":
                        count = count - 1
                        if count == 0:
                            skip = True
                            temp = [
                                [
                                    " " * spacing
                                    + lyne[0 : itr + 1].strip()
                                    + " then"
                                    + " " * indent
                                    + cmt
                                ][0].rstrip()
                            ]
                            temp2 = (
                                " " * spacing + " " * indent + lyne[itr + 1 :].strip()
                            )
                            if temp2.strip():
                                temp.append(
                                    " " * spacing
                                    + " " * indent
                                    + lyne[itr + 1 :].strip()
                                )
                            if not lyne[itr + 1 :].strip():
                                ltr = 1
                                while (
                                    lynes[line_num + ltr].strip()
                                    and lynes[line_num + ltr].strip()[0] == "&"
                                ):
                                    skipLynes = skipLynes + 1
                                    temp.append(
                                        " " * spaceamp
                                        + "&"
                                        + " " * indent
                                        + lynes[line_num + ltr].strip()[1:].strip()
                                    )
                                    ltr = ltr + 1
                            elif lyne[itr + 1 :].strip()[-1] == "," or (
                                "write" in lyne[itr + 1 :]
                                and "&" in lynes[line_num + 1].strip()
                            ):
                                ltr = 1
                                while "&" in lynes[line_num + ltr].strip():
                                    skipLynes = skipLynes + 1
                                    temp.append(
                                        " " * spaceamp
                                        + "&"
                                        + " " * indent
                                        + lynes[line_num + ltr].strip()[1:].strip()
                                    )
                                    ltr = ltr + 1
                            temp.append(" " * spacing + "endif")
                            lyne = temp
        else:
            lyne = lyne + cmt
    return [lyne, skip, skipLynes]