# ========================================================================
# Function: if_logicals_spacing
# ========================================================================
# Purpose:
# Adds spaces between logical expressions: x.gt.y => x .gt. y
# This promotes code readability and is common place in other language
# formatters (clang, black, etc).
#
# TODO: Probably need to update for a line carrying over
# ========================================================================
def if_logicals_spacing(self):
    # This puts a space between keywords statements.
    new_file_lines = []
    iftypes = [".and.", ".not."]  # These are 3 letter
    iftypes2 = [  # These are 2 letter
        ".eq.",
        ".ge.",
        ".gt.",
        ".le.",
        ".lt.",
        ".ne.",
        ".or.",
    ]
    # ===========================================================
    # Process each line of the file one at a time. If raw == given, store those lines.
    for line in self.file_lines:
        skip = False
        skip_pass = 0
        temp = ""
        for j, char in enumerate(line):
            if skip_pass == 0:
                if char == "!":
                    skip = True
                if skip:
                    temp += char
                else:
                    if char == "." and any(line[j : j + 5] in x for x in iftypes):
                        try:
                            if line[j + 5]:
                                if line[j - 1] != " " and line[j + 5] != " ":
                                    temp += " " + line[j : j + 5] + " "
                                elif line[j - 1] != " " and line[j + 5] == " ":
                                    temp += " " + line[j : j + 5]
                                elif line[j - 1] == " " and line[j + 5] != " ":
                                    temp += line[j : j + 5]
                                else:
                                    temp += line[j : j + 5]
                                skip_pass = 4
                        except IndexError:
                            if line[j - 1] != " ":
                                temp += " " + line[j:]
                            else:
                                temp += line[j:]
                            skip_pass = 4
                            skip = True
                    elif char == "." and any(line[j : j + 4] in x for x in iftypes2):
                        try:
                            if line[j + 4]:
                                if (
                                    line[j - 1] != " "
                                    and line[j + 4] != " "
                                    and line[j + 4] != "."
                                ):
                                    temp += " " + line[j : j + 4] + " "
                                elif line[j - 1] != " " and line[j + 4] == " ":
                                    temp += " " + line[j : j + 4]
                                elif line[j - 1] == " " and line[j + 4] != " ":
                                    temp += line[j : j + 4] + " "
                                else:
                                    temp += line[j : j + 4]
                                skip_pass = 3
                        except IndexError:
                            if line[j - 1] != " ":
                                temp += " " + line[j:]
                            else:
                                temp += line[j:]
                            skip_pass = 3
                    else:
                        temp += char
            else:
                skip_pass = skip_pass - 1
        line = temp
        new_file_lines.append(line)
    self.file_lines = new_file_lines
    return
