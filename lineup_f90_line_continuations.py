from donotformat import doNotFormatCheck

def lineup_f90_line_continuations(lynes, f90):
    new_lynes = []
    weopen = False
    for lyne in lynes:
        if f90 and lyne.strip():
            if "&" == lyne[-2] and "!" != lyne.strip()[0]:
                if lyne.count("(") > lyne.count(")"):
                    starting_col = lyne.find("(") + 2
                    weopen = True
                elif weopen and lyne.count("(") <= lyne.count(")"):
                    lyne = " " * starting_col + lyne.lstrip()
            elif weopen and lyne.count("(") <= lyne.count(")"):
                lyne = " " * starting_col + lyne.lstrip()
                weopen = False
        new_lynes.append(lyne)
    return new_lynes
