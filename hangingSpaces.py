

# ===========================================================
def hangingSpaces(lynes):
    """
    Removes white space from the end of lines
    """
    new_lynes = []
    # =======================================================
    for itr, lyne in enumerate(lynes):
        lenLyne = len(lyne)
        if lenLyne > 1:
            jtr = -2
            while lyne[jtr] == " ":
                jtr = jtr - 1
                if abs(jtr) == lenLyne:
                    break
            if "implicit NONE" in lyne:
                lyne = lyne.replace(
                    "implicit NONE", "implicit none"
                )  # This was happening for some reason
            if "record / " in lyne:
                rloc = lyne.find("record / ") + len("record / ")
                tempLyne = lyne[rloc:]
                endrloc = tempLyne.find("/")
                sname = tempLyne[
                    :endrloc
                ].lower()  # This was uppercasing for some reason.
                lyne = lyne[:rloc] + sname + tempLyne[endrloc:]
            lynes[itr] = lyne[: jtr + 1] + lyne[-1]
        new_lynes.append(lynes[itr])
    return new_lynes
