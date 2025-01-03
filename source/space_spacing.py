# ========================================================================
# Function: paren_spacing
# ========================================================================
# Purpose:
# Handles formatting for objects around and inside parens ()
# ========================================================================
def space_spacing(self, j, char, code_line, temp_line):
    if code_line[j - 1] == "(" or (j + 1 < len(code_line) and code_line[j + 1] == ")"):
        temp = temp_line # skip this because we want parens to line up with args
    else:
        temp = temp_line + char
    return temp
