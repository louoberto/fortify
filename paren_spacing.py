# ========================================================================
# Function: paren_spacing
# ========================================================================
# Purpose:
# Will format 
# ========================================================================
def paren_spacing(self, j, char, code_line, temp_line):
    if char == self.space:
        if code_line[j - 1] == "(" or j + 1 < len(code_line) and code_line[j + 1] == ")":
            temp = temp_line # skip this because we want parens to line up with args
        else:
            temp = temp_line + char
    elif char == ")" and j + 1 < len(code_line) and code_line[j + 1] and code_line[j + 1] not in ("\n", self.space, "%"):
        temp = temp_line + char + self.space
    else:
        temp = temp_line + char
    return temp
