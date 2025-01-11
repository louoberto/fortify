# ========================================================================
# Function: remove_extra_space
# ========================================================================
# Purpose:
# Removes double spacing in a code line.
# ========================================================================
def remove_extra_space(self, j, char, code_line, temp_line):
    if code_line[j + 1] in [self.newline, self.space]:
        temp = temp_line
    else:
        # print(repr(temp_line), repr(code_line[j - 1]), repr(code_line[j + 1]))
        if code_line[j - 1] == "(": # Remove blank space after paren
            # print(repr(temp_line))
            temp = temp_line
        else:
            if code_line[j + 1] == ")":
                temp = temp_line
            elif code_line[j - 1] == "(":
                temp = temp_line
                # print(repr(temp))
            elif temp_line[-1] == "(":
                temp = temp_line
            else:
                temp = temp_line + char
                # print(repr(temp))

    return temp