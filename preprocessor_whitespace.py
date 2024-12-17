# ===========================================================
def preprocessor_whitespace(lynes):
    """
    Ensures that all preprocessor directives, #, start in the 0th column
    """
    # Open the file again, read in the lines of data
    new_lynes = []

    for lyne in lynes:
        line_to_print = lyne
        if line_to_print.lstrip():
            if line_to_print.lstrip()[0] == "#":
                line_to_print = line_to_print.lstrip()

        new_lynes.append(line_to_print)
    return new_lynes
