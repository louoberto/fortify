# ========================================================================
# Function: comma_spacing
# ========================================================================
# Purpose:
# Should handle cases :: and , related formatting
# ========================================================================
def comma_spacing(self, j, char, code_line, temp_line):
    if code_line[j - 1] == self.space: # Comma case 1
        temp = temp_line[:-1] + char
    elif code_line[j + 1] != self.space: # Comma case 2
        temp = temp_line + char + self.space
    else:
        temp = temp_line + char
    return temp
