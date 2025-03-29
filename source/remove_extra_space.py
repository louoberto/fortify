# ========================================================================
# Function: remove_extra_space
# ========================================================================
# Purpose:
# Removes double spacing in a code line.
# ========================================================================
def remove_extra_space(self, j, char, code_line, temp_line):
    if (len(code_line) > j + 1) and (code_line[j + 1] in [self.newline, self.space] or \
       code_line[j + 1] == ")" or code_line[j + 1] == "]") or \
       code_line[j - 1] == "(" or code_line[j - 1] == "[" or\
       (temp_line and temp_line[-1] == "(") or (temp_line and temp_line[-1] == "["):
        temp = temp_line
    else:
        temp = temp_line + char

    return temp