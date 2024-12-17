# ===========================================================
def processHangingEnds(lynes):
    """
    Change 'end if', 'end do', and 'go to' to one word 'endif', 'enddo', 'goto'
    """
    new_lynes = []
    # =======================================================
    # Process each line of the file one at a time. if raw == given, store those lines.
    for lyne in lynes:
        if "end if" in lyne:
            locend = lyne.find("end if")
            lyne = lyne[:locend] + lyne[locend : locend + 3] + lyne[locend + 4 :]
        if "end do" in lyne:
            locend = lyne.find("end do")
            lyne = lyne[:locend] + lyne[locend : locend + 3] + lyne[locend + 4 :]
        if "go to" in lyne:
            locend = lyne.find("go to")
            lyne = lyne[:locend] + "goto" + lyne[locend + 5 :]
        new_lynes.append(lyne)
    return new_lynes
