from donotformat import doNotFormatCheck
# ===========================================================
def format_params_saves(lynes, common=False):
    """
    Finds all parameter variables, formats them to be as follows:
    type, parameter :: var = value
    If there are parameter declarations between preprocessor #if statements,
    those are left alone
    """
    # Open file, grab lines in the file
    new_lynes = []
    functions = [
    "subroutine",
    "function",
    "program",
    ]  # Types of Fortran code blocks, used to identify the start and ending of function sections
    # Variable declartion types, referenced in multiple functions
    data_types = ["integer", "real", "complex", "character", "logical"]
    param_str = "parameter"
    save_str = "save"

    parameter_dicts = []
    parameter_dict = {}  # Dictionary

    param_comments_dicts = []  # List of dictionaries
    param_comments_dict = {}  # Dictionary

    save_lists = []
    save_list = []  # list

    preprocessor_directive = False
    num_functions = 0
    first_common = False

    for lyne in lynes:
        this_line = lyne.lstrip()
        # Block parameters up separately for multiple functions in a given .f file
        for func in functions:
            if func in this_line[: len(func)] or (common and not first_common):
                num_functions += 1
                first_common = True
                parameter_dicts.append(
                    parameter_dict
                )  # Store the dictionary we've built so far
                parameter_dict = {}

                param_comments_dicts.append(param_comments_dict)
                param_comments_dict = {}

                save_lists.append(save_list)  # Store the dictionary we've built so far
                save_list = []
                break
        if this_line != "!":  # Make sure we aren't starting with a line comment

            # Dont' process stuff in between preprocessor directives
            if "#if" in this_line[0:3]:
                preprocessor_directive = True
            elif "#end" in this_line[0:4]:
                preprocessor_directive = False
            # Is this line a parameter?
            elif (
                param_str in this_line[: len(param_str)] and not preprocessor_directive
            ):
                # Grab string between ( and =, that's our variable name
                paren_start = this_line.find("(")
                equal_start = this_line.find("=")
                cmt_index = this_line.find("!")
                paren_end = [
                    par for par, x in enumerate(this_line[:cmt_index]) if x == ")"
                ]  # Grab last element
                if paren_start > -1 and equal_start > -1 and paren_end:

                    # Grab string between = and ), that's our value
                    variable = this_line[paren_start + 1 : equal_start]
                    variable = variable.strip()
                    value = this_line[equal_start + 1 : paren_end[-1]]
                    value = value.strip()

                    if variable and value:  # Add that to a dictionary
                        parameter_dict[variable] = value

                        if "!" in this_line[paren_end[-1] :]:
                            param_comments_dict[variable] = this_line[cmt_index:]

            # Is this line a save variable?
            elif save_str in this_line[: len(save_str)] and not preprocessor_directive:
                variable = this_line.split()[1]
                # Check if we have a list of saved vars
                if variable[-1] == ",":
                    save_list.append(variable[:-1])  # Save this one (without the comma)
                    # Check for more save vars
                    if len(this_line.split()) > 2:
                        for var in this_line.split()[2:]:
                            if var[0] != "!":  # Check for line comments
                                if var[-1] == ",":  # Trim commas for lists
                                    var = var[:-1]
                                save_list.append(var)
                            else:
                                break  # We found the line comment, stop processing

                    else:
                        save_list.append(variable)

    parameter_dicts.append(
        parameter_dict
    )  # Store the dictionary for the last function we find
    param_comments_dicts.append(param_comments_dict)
    save_lists.append(save_list)
    num_functions = 0  # Reset this for the next time we loop around
    first_common = False

    # Now that we have a list of parameters, loop back through, find when we declare that variable, add it
    for lyne in lynes:
        skip_this_line = False
        line_to_print = lyne

        if not doNotFormatCheck(lyne):
            this_line = lyne.lstrip()

            # Block parameters up separately for multiple functions in a given .f file
            for func in functions:
                if func in this_line[: len(func)] or (common and not first_common):
                    num_functions += 1
                    first_common = True
                    break
            if this_line != "!":  # Make sure we aren't starting with a line comment
                # Don't process stuff in between preprocessor directives
                if "#if" in this_line[0:3]:
                    preprocessor_directive = True
                elif "#end" in this_line[0:4]:
                    preprocessor_directive = False
                elif not preprocessor_directive:
                    for dtype in data_types:
                        # Find code, get rid of comment
                        comment_indx = this_line.find("!")
                        line_sans_comment = this_line[:comment_indx]
                        line_sans_comment.strip()

                        # If this line just declares a parameter/save, don't print it. Gonna bring this info in later
                        if (
                            param_str in this_line[: len(param_str)]
                            or save_str in this_line[: len(save_str)]
                        ):
                            if (
                                this_line.split()[0] in save_str
                                or this_line[: len(param_str)] in param_str
                            ):  # Make sure we are looking for "save", not "save_var_name"
                                skip_this_line = True

                        # Is this line a variable that isn't already a parameter or a save variable?
                        elif dtype in this_line[: len(dtype)]:

                            line_split = this_line.split()
                            declare = line_split[0]
                            variable = this_line[len(declare) : comment_indx].strip()

                            # Is this already a save/parameter?
                            if (
                                save_str not in variable[: len(save_str)]
                                and param_str not in variable[: len(param_str)]
                            ):
                                for parm in parameter_dicts[num_functions]:
                                    if parm:  # Delas with empty values
                                        if (
                                            parm in variable
                                        ):  # Looping this way allows var( n )
                                            line_to_print = (
                                                spacing * " "
                                                + declare
                                                + ", "
                                                + param_str
                                                + " :: "
                                                + variable
                                                + " = "
                                                + parameter_dicts[num_functions][parm]
                                                + this_line[comment_indx:]
                                            )

                                            if (
                                                parm
                                                in param_comments_dicts[num_functions]
                                            ):
                                                line_to_print += param_comments_dicts[
                                                    num_functions
                                                ][parm]
                                            del parameter_dicts[num_functions][parm]
                                            break

                                for indx, sav in enumerate(save_lists[num_functions]):
                                    if sav:  # Deals with empty values
                                        if sav in variable[: len(sav)]:
                                            if len(variable) == len(sav):
                                                line_to_print = (
                                                    spacing * " "
                                                    + declare
                                                    + ", "
                                                    + save_str
                                                    + " :: "
                                                    + variable
                                                    + this_line[comment_indx:]
                                                )
                                                del save_lists[num_functions][indx]
                                                break  # We have found the right variable type. Stop wasting time with further for loop iterations
                                            elif len(variable) > len(sav):
                                                if variable[len(sav)] == "(":
                                                    line_to_print = (
                                                        spacing * " "
                                                        + declare
                                                        + ", "
                                                        + save_str
                                                        + " :: "
                                                        + variable
                                                        + this_line[comment_indx:]
                                                    )
                                                    del save_lists[num_functions][indx]
                                                    break  # We have found the right variable type. Stop wasting time with further for loop iterations
                            break

        # Now that we've done everything to this line, print it
        if not skip_this_line:
            new_lynes.append(line_to_print)

    return new_lynes
