# ========================================================================
# Function: miuns_spacing
# ========================================================================
# Purpose:
# Will format  I believe this handles = - 0.213 to = -0.213 for example
# ========================================================================
def minus_spacing(j, char, ff_line, code_line, temp):
    if (ff_line and ff_line[-1] == "&" and j == 0) or (
        code_line[j - 3] in ["=", "-", "+", "/", "*"]
        and code_line[j - 2] == ' '
        and code_line[j - 1] in ["+", "-"]
    ):
        pass
    return char
