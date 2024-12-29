# ===========================================================
def processIncludes(lynes):
    """
    Alphabetizes each block of include statements
    """
    new_lynes = []

    include_list = []
    start_includes = False

    for lyne in lynes:
        if lyne.lstrip() != "!" and lyne.lstrip()[:7] == "include":
            start_includes = True

            temp = lyne.lstrip()
            temp = temp[temp.find(" ") :].lstrip()
            include_list.append(temp)

        elif start_includes and lyne.lstrip() and lyne.lstrip()[:7] != "include":
            # Stopped finding 'include' statements
            start_includes = False

            # Print all found includes to the file
            include_list = sorted(include_list)
            for incl in include_list:
                new_lynes.append(" " * spacing + "include " + incl)

            include_list = []

            # Print the line we just found
            new_lynes.append("\n")
            new_lynes.append(lyne)

        else:
            new_lynes.append(lyne)

    return new_lynes
