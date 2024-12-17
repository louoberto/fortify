# ===========================================================
def tabsToSpaces(lynes):
    """
    Converts tab characters to spaces
    """
    new_lynes = []
    indent = 3  # default indentation
    include_list = []
    start_includes = False

    for lyne in lynes:
        if "\t" in lyne:
            # lyne.replace('\t', ' '*indent)
            new_lynes.append(lyne.replace("\t", " " * indent))
        else:
            new_lynes.append(lyne)

    return new_lynes