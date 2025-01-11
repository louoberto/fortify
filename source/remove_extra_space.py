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
        if code_line[j - 1] == "(": # Remove blank space after paren
            # print(repr(temp_line))
            temp = temp_line
        else:
            if code_line[j + 1] == ")":
                temp = temp_line
            else:
                temp = temp_line + char

    return temp