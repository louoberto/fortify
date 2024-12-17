from donotformat import doNotFormatCheck

# ==========================================================
def convert_line_breaks(lynes, f90):
    """
    If we have line breaks, make sure we are using & as the character
    """
    new_lynes = []
    weopen = False
    for lyne in lynes:
        comment_found = False
        if lyne.strip():  # Is there anything in this line to worry about?
            if not f90:
                if lyne[0].strip():  # Is there anything in the first column?
                    if not lyne[0].strip().isdigit():
                        comment_found = (
                            True  # First column != a number, so it's a comment
                        )

                    # If we have a symbol in the 6th column and it isn't a line comment, make sure its a &
                    if len(lyne) >= 6 and not comment_found:
                        if lyne[5].strip():
                            lyne = lyne[:5] + "&" + lyne[6:]
        new_lynes.append(lyne)
    return new_lynes
