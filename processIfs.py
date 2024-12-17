from donotformat import doNotFormatCheck
spacing = 6  # First 6 cols go unused in most cases
spaceamp = 5
indent = 3  # default indentation
lastcol = 131  # Last usable column in Fortran

# ===========================================================
def processIfStatements(lynes):
    """
    Prints a line or not, depending on how we process an if statement
    """
    new_lynes = []
    # ==================================================
    # Process each line of the file one at a time. If raw == given, store those lines.
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
def processIfs2(lynes):
    new_lynes = []
    iftypes = [".and.", ".not."]
    iftypes2 = [".eq.", ".ge.", ".gt.", ".le.", ".lt.", ".ne.", ".or."]
    # ===========================================================
    # Process each line of the file one at a time. If raw == given, store those lines.
    for lyne in lynes:
        skip = False
        skipPass = 0
        temp = ""
        for jtr, char in enumerate(lyne):
            if skipPass == 0:
                if char == "!":
                    skip = True
                if skip:
                    temp += char
                else:
                    if char == "." and any(lyne[jtr : jtr + 5] in x for x in iftypes):
                        try:
                            if lyne[jtr + 5]:
                                if lyne[jtr - 1] != " " and lyne[jtr + 5] != " ":
                                    temp += " " + lyne[jtr : jtr + 5] + " "
                                elif lyne[jtr - 1] != " " and lyne[jtr + 5] == " ":
                                    temp += " " + lyne[jtr : jtr + 5]
                                elif lyne[jtr - 1] == " " and lyne[jtr + 5] != " ":
                                    temp += lyne[jtr : jtr + 5]
                                else:
                                    temp += lyne[jtr : jtr + 5]
                                skipPass = 4
                        except IndexError:
                            if lyne[jtr - 1] != " ":
                                temp += " " + lyne[jtr:]
                            else:
                                temp += lyne[jtr:]
                            skipPass = 4
                            skip = True
                    elif char == "." and any(
                        lyne[jtr : jtr + 4] in x for x in iftypes2
                    ):
                        try:
                            if lyne[jtr + 4]:
                                if (
                                    lyne[jtr - 1] != " "
                                    and lyne[jtr + 4] != " "
                                    and lyne[jtr + 4] != "."
                                ):
                                    temp += " " + lyne[jtr : jtr + 4] + " "
                                elif lyne[jtr - 1] != " " and lyne[jtr + 4] == " ":
                                    temp += " " + lyne[jtr : jtr + 4]
                                elif lyne[jtr - 1] == " " and lyne[jtr + 4] != " ":
                                    temp += lyne[jtr : jtr + 4] + " "
                                else:
                                    temp += lyne[jtr : jtr + 4]
                                skipPass = 3
                        except IndexError:
                            if lyne[jtr - 1] != " ":
                                temp += " " + lyne[jtr:]
                            else:
                                temp += lyne[jtr:]
                            skipPass = 3
                    else:
                        temp += char
            else:
                skipPass = skipPass - 1
        lyne = temp
        new_lynes.append(lyne)
    return new_lynes


# ===========================================================
def preprocessIfs3(lynes):
    new_lynes = []
    # =======================================================
    # Process each line of the file one at a time. If raw == given, store those lines.
    skipLynes = 0
    for itr, lyne in enumerate(lynes):
        if skipLynes == 0:
            [lyne, skip, skipLynes] = processIfs3(lyne, lynes, itr)
            if not skip:
                new_lynes.append(lyne)
            else:
                for guy in lyne:
                    new_lynes.append(guy + "\n")
        else:
            skipLynes = skipLynes + 1
    return new_lynes

# ===========================================================
def processIfs(lyne, lynes, lnum):
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
                                    lynes[lnum + ltr].strip()
                                    and lynes[lnum + ltr].strip()[0] == "&"
                                ):
                                    skipLynes = skipLynes + 1
                                    temp.append(
                                        " " * spaceamp
                                        + "&"
                                        + " " * indent
                                        + lynes[lnum + ltr].strip()[1:].strip()
                                    )
                                    ltr = ltr + 1
                            elif lyne[itr + 1 :].strip()[-1] == "," or (
                                "write" in lyne[itr + 1 :]
                                and "&" in lynes[lnum + 1].strip()
                            ):
                                ltr = 1
                                while "&" in lynes[lnum + ltr].strip():
                                    skipLynes = skipLynes + 1
                                    temp.append(
                                        " " * spaceamp
                                        + "&"
                                        + " " * indent
                                        + lynes[lnum + ltr].strip()[1:].strip()
                                    )
                                    ltr = ltr + 1
                            temp.append(" " * spacing + "endif")
                            lyne = temp
        else:
            lyne = lyne + cmt
    return [lyne, skip, skipLynes]

# ===========================================================
def processIfs3(lyne, lynes, lnum):
    cmt = ""
    skipLynes = 0
    skip = False
    if lyne[0].isnumeric():
        if "if (" in lyne[1:]:
            # ===================================================
            if lyne.find("!") > 0:
                cmt = lyne[lyne.find("!") :]
                lyne = lyne[0 : lyne.find("!")]
            if "then" not in lyne.replace(" ", "")[-5:]:
                # lyne=' '*spacing + lyne.strip()
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
                                    " " * spacing
                                    + " " * indent
                                    + lyne[itr + 1 :].strip()
                                )
                                if temp2.strip():
                                    temp.append(
                                        " " * spacing
                                        + " " * indent
                                        + lyne[itr + 1 :].strip()
                                    )
                                if not lyne[itr + 1 :].strip():
                                    ltr = 1
                                    while lynes[lnum + ltr].strip()[0] == "&":
                                        skipLynes = skipLynes + 1
                                        temp.append(
                                            " " * spaceamp
                                            + "&"
                                            + " " * indent
                                            + lynes[lnum + ltr].strip()[1:].strip()
                                        )
                                        ltr = ltr + 1
                                elif lyne[itr + 1 :].strip()[-1] == ",":
                                    ltr = 1
                                    while lynes[lnum + ltr].strip()[0] == "&":
                                        skipLynes = skipLynes + 1
                                        temp.append(
                                            " " * spaceamp
                                            + "&"
                                            + " " * indent
                                            + lynes[lnum + ltr].strip()[1:].strip()
                                        )
                                        ltr = ltr + 1
                                temp.append(" " * spacing + "endif")
                                lyne = temp
            else:
                lyne = lyne + cmt
    return [lyne, skip, skipLynes]

