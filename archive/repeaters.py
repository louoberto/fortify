# ===========================================================
def repeaters(lynes):
    new_lynes = []
    format_open = False
    lparen = 0
    rparen = 0

    # Loop through lines, re-print them if they don't repeat
    for itr, lyne in enumerate(lynes):

        # Comment
        new_lynes.append(
            lyne
        )  # State by assuming we'll keep this ine, then remove it if needed

        # Checks we need to make on every line
        if (
            lparen == rparen
        ):  # If all parens are closed, then we're done with the format statement
            format_open = False
            lparen = 0
            rparen = 0
        if len(lyne.split()) > 1:
            if "format" in lyne.split()[1]:
                format_open = True
        if format_open:
            cmt_index = lyne.find("!")
            for char in lyne[:cmt_index]:  # count parens, skipping line comments
                if char == "(":
                    lparen += 1
                elif char == ")":
                    rparen += 1

        # Check if we want to remove this line
        if itr > 0:
            if lyne == lynes[itr - 1]:  # Do we have a repeated line?
                remove_line = (
                    True  # Assume we'll remove this line, but look for exceptions
                )
                if lyne.lstrip():  # Make sure we're not looking at a blank line

                    if lyne.lstrip()[0] == "!":
                        remove_line = False
                    elif format_open:
                        remove_line = False
                    elif (
                        "write" in lyne.lstrip()[: len("write")]
                    ):  # We don't want to delete write statements
                        remove_line = False

                if remove_line:
                    new_lynes.pop()  # Remove the last line
    return new_lynes
