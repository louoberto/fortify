import numpy as np
# ===========================================================
def process_preprocessor_directives(lynes):
    """
    Lines containing a # preprocessor directive should not be reformatted,
    except for removing trailing whitespaces
    """

    # Open the file again, read in the lines of data
    new_lynes = []

    hash_includes = "#include"
    include_names = []

    # Loop trough the file, find all the #include statements and process them
    for lyne in lynes:
        if len(lyne.lstrip()) > 0:
            # Is this a preprocessor directive?
            if lyne.lstrip()[0] == "#":

                if hash_include in lyne.strip()[: len(hash_include)]:

                    # Grab name of file
                    include_names.append(lyne.split()[1][1:-1])

    # Now that we have found all the #include statements, open them up and find the #declare vars
    declared_vars = np.array([])
    if include_names:
        for inc in include_names:
            print("Looking for: " + inc)
            include_file = glob.glob(
                os.path.join(source_dir, "**", inc), recursive=True
            )

            # Grab list of variables to define
            if include_file:
                declared_vars = np.append(declared_vars, find_defines(include_file[0]))

    declared_vars = declared_vars.flatten()
    if np.size(declared_vars) > 0:
        declared_lowercase = np.char.lower(declared_vars)

    # Now that we have found all the variables we care about, print the updated file
    for lyne in lynes:

        line_to_print = lyne
        if len(line_to_print.lstrip()) > 0:

            if (
                line_to_print.lstrip()[0] == "#"
            ):  # We have found a preprocessor directive
                line_to_print = line_to_print.lstrip()

            elif np.size(declared_vars) > 0:

                # Remove commas at the end of the words for better matching
                splt = line_to_print.split()
                splt_no_comma = line_to_print.split()
                comma_indices = []
                oparen_indices = []
                for indx, word in enumerate(splt):
                    if word[-1] == ",":
                        splt_no_comma[indx] = word[:-1]
                        comma_indices.append(indx)
                    elif word[-1] == "(":
                        splt_no_comma[indx] = word[:-1]
                        oparen_indices.append(indx)

                if set(declared_lowercase) & set(splt_no_comma):
                    # Something on this line == a #declare variable, find it and change it
                    string_open = False
                    num_apostrophe = 0
                    for indx, word in enumerate(splt_no_comma):
                        if "!" in word:
                            break  # Don't change line comments
                        # Don't change strings
                        if "'" in word:
                            num_apostrophe += word.count("'")
                            if num_apostrophe % 2:
                                string_open = True
                            else:
                                string_open = False

                        elif not string_open and word in declared_lowercase:
                            jdx = [
                                i for i, s in enumerate(declared_lowercase) if word == s
                            ]
                            splt[indx] = declared_vars[jdx[-1]]
                            if indx in comma_indices:
                                splt[indx] = splt[indx] + ","
                            elif indx in oparen_indices:
                                splt[indx] = splt[indx] + "("

                    line_to_print = (
                        " " * (len(line_to_print) - len(line_to_print.lstrip()))
                        + " ".join(splt)
                        + "\n"
                    )
        new_lynes.append(line_to_print)
    return new_lynes
