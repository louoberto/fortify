import glob
import numpy as np
# ===========================================================
def globetrot(lynes):
    """
    Sort through all include .cmn/.inc files, make all global variables capitalized
    """
    new_lynes = []
    noWrite = False
    includeList = []

    # ToDo: need to sort between multiple functions, only caps globals for that function
    for lyne in lynes:
        if lyne.lstrip() != "!":  # Check that this != just a line comment
            if lyne.lstrip()[:7] == "include":
                splt = lyne.split()
                inc = splt[1]
                includeList.append(inc)

    includeList = sorted(includeList)
    includeList = np.unique(includeList)
    # Process includes again, by getting just the names
    for itr, inclu in enumerate(includeList):
        includeList[itr] = inclu[1:]
        includeList[itr] = includeList[itr][: includeList[itr].find("'")]

    cmnVarList = []
    structname = ""
    strux = []
    struxNames = []
    rekords = []
    struxAppeared = False
    recordname = ""
    ktr = 0
    # =====================================================================
    # Scan the include list and store the variables
    for itr, inclu in enumerate(includeList):
        cmnVarList.append("new_inclu_" + inclu)
        # line skip 1 Can use this to skip certains things, for instance
        # line skip 2
        # line skip 3
        print("Looking for: ", inclu)
        # Make sure the file can be open, and, if so, store the lines
        cFile = glob.glob(os.path.join(autogen_path, "**", inclu), recursive=True)

        if cFile:
            cFile = cFile[0]
            try:
                with open(cFile, "r") as inCmn:  # Inhale the whole file
                    cLynes = inCmn.readlines()
            except:
                try:
                    with open(inclu, "r") as inCmn:  # Inhale the whole file
                        cLynes = inCmn.readlines()
                except:
                    noWrite = True
                    print("Could not open/read: ", cFile)
                    continue
            for jtr, lyne in enumerate(cLynes):

                lyne_strip = lyne.lstrip()
                cmt_index = lyne_strip.find("!")

                if "record / " in lyne_strip[: len("record / ")]:
                    temp = lyne.lstrip()[len("record /") :]
                    structname = temp[: temp.find("/")].strip()
                    recordname = temp[temp.find("/") + 1 :].strip()
                    rekords.append(structname + "." + recordname)
                elif "structure /" in lyne_strip[: len("structure /")]:
                    temp = lyne_strip[len("structure /") :]
                    structname = temp[: temp.find("/")].strip()
                    cmnVarList.append(structname)
                    struxNames.append(structname)
                    struxAppeared = True
                elif "end structure" in lyne_strip[: len("end structure")]:
                    struxAppeared = False
                    ktr = ktr + 1
                dummy = lyne.lstrip()

                var_list = False
                starloc = lyne_strip[:cmt_index].find("*")
                if lyne_strip[:starloc] in data_types:

                    # Check if we have a parameter
                    splt = lyne_strip[:cmt_index].split()
                    if "::" in lyne_strip[:cmt_index]:
                        for indx, word in enumerate(splt):
                            # Assumes Clu styling, with "type, parameter :: var"
                            if "::" == word and len(splt) > indx + 2:
                                variable = splt[indx + 1]
                                if (
                                    variable[-1] == "," or variable[-1] == "("
                                ):  # Trim stuff at the end
                                    variable = variable[:-1]
                                cmnVarList.append(variable)  # Save this variable
                                if (
                                    struxAppeared
                                ):  # Then check later if a record of it == here
                                    strux.append(structname + "." + variable)
                                break
                    else:
                        variable = splt[1]
                        rparen = 0
                        lparen = 0
                        if (
                            variable[-1] == "," or variable[-1] == "("
                        ):  # Trim stuff at the end
                            if variable[-1] == ",":
                                var_list = True
                            lparen += variable.count("(")
                            rparen += variable.count(")")
                            variable = variable[:-1]
                        cmnVarList.append(variable)  # Save this variable
                        if struxAppeared:  # Then check later if a record of it == here
                            strux.append(structname + "." + variable)

                        if (
                            var_list and len(splt) > 2
                        ):  # If we have more variables, grab them
                            for variable in splt[2:]:
                                lparen += variable.count("(")
                                rparen += variable.count(")")
                                if lparen == rparen and ")" not in variable:
                                    if variable[-1] == ",":  # Trim stuff at the end
                                        variable = variable[:-1]
                                    cmnVarList.append(variable)  # Save this variable
                                    if (
                                        struxAppeared
                                    ):  # Then check later if a record of it == here
                                        strux.append(structname + "." + variable)
        else:
            print("Cannot find include file: ", incl)
    if rekords:
        for itr, var in enumerate(cmnVarList):
            for jtr, rekord in enumerate(rekords):
                sn = rekord[: rekord.find(".")]  # Struct name
                rekname = rekord[rekord.find(".") + 1 :]  # record name
                for ktr, struckie in enumerate(strux):
                    sn2 = struckie[: struckie.find(".")]  # Struct name
                    struxvar = struckie[struckie.find(".") + 1 :]  # var name
                    if (
                        sn == sn2 and var == struxvar
                    ):  # Struct names and var names match. so change to have period
                        cmnVarList[itr] = rekname + "." + var

    # ===============================================================
    noCmns = True
    checkCmn = []
    for itr, var in enumerate(cmnVarList):
        if "new_inclu_" in var:  # and itr>0: # and 'new_inclu' not in cmnVarList[-1]
            next = True
            cmnFil = var[10:]
            firstFlag = True
        else:
            next = False
        if next:  # reset this flag
            noCmns = True
        varLen = len(var)
        for jtr, lyne in enumerate(lynes):
            if lyne.lstrip() != "!":
                isComment = False
                isQuote = False
                dummy = ""
                skipLen = 0
                for ktr, char in enumerate(lyne):
                    if char == "!":
                        isComment = True
                    if char == "'" and not isComment:
                        if isQuote:
                            isQuote = False
                        else:
                            isQuote = True
                    if not isComment and not isQuote:
                        if (
                            var.lower() == lyne[ktr : ktr + varLen].lower()
                            and not lyne[ktr + varLen].isnumeric()
                            and not lyne[ktr + varLen].isalpha()
                            and not lyne[ktr - 1].isalpha()
                            and lyne[ktr + varLen] != "_"
                            and lyne[ktr - 1] != "."
                            and lyne[ktr - 1] != "_"
                            and lyne[ktr + varLen] != "."
                        ):
                            skipLen = varLen
                            if var == structname or "." in var:
                                dummy = (
                                    dummy + var.lower()
                                )  # Keep struct names lowercased
                            else:
                                dummy = dummy + var.upper()
                            noCmns = False
                        else:
                            if skipLen > 1:
                                skipLen = skipLen - 1
                            else:
                                dummy = dummy + char
                    else:
                        dummy = dummy + char
                lynes[jtr] = dummy
        if not noCmns and firstFlag:
            firstFlag = False
            checkCmn.append(cmnFil)
    for itr, inclu in enumerate(includeList):
        if inclu not in checkCmn:
            print("Might be able to remove: " + inclu)
    if not noWrite:
        # Print to the file
        for lyne in lynes:
            new_lynes.append(lyne)
    return new_lynes
