spacing = 6  # First 6 cols go unused in most cases
spaceamp = 5
indent = 3  # default indentation
lastcol = 131  # Last usable column in Fortran

# Variable declartion types, referenced in multiple functions
data_types = ["integer", "real", "complex", "character", "logical"]
# ===========================================================
def param_save_comma(lynes):
    """
    If we declare a variable as a 'parameter' or 'save' variable, ensure
    there == a comma between modifiers
    """
    new_lynes = []
    # Loop through all lines, clean up variable declarations
    for line in lynes:
        line_to_print = line
        this_line = line.strip()

        if this_line != "!":  # don't worry about line comment lines

            for dtype in data_types:
                if dtype in this_line[: len(dtype)]:

                    # This == a variable declaration, find which index we have "::"
                    line_split = this_line.split()
                    colns = []
                    for indx, splt in enumerate(line_split):
                        if "::" == splt:
                            colns = indx
                            break
                        elif "!" in splt:
                            break
                    if colns:
                        leftParens = 0
                        rightParens = 0

                        # If this declaration has "::", make sure there are commas after the modifiers
                        for indx, splt in enumerate(line_split[: colns - 1]):

                            for char in splt:
                                if char == "(":
                                    leftParens = leftParens + 1
                                elif char == ")":
                                    rightParens = rightParens + 1
                            openToClose = (
                                leftParens - rightParens
                            )  # ...Assuming there's not

                            if line_split[0][-1] != "," and openToClose == 0:
                                line_split[indx] = line_split[indx] + ","
                        line_to_print = spacing * " " + " ".join(line_split)

                        # Make sure we have a line ending here
                        if line_to_print[-1] != "\n":
                            line_to_print = line_to_print + "\n"
                    break

        new_lynes.append(line_to_print)
    return new_lynes
