# ========================================================================
# Function: comma_spacing
# ========================================================================
# Purpose:
# Should handle cases , related formatting
# ========================================================================
def comma_spacing(self, j, char, code_line, temp_line):
    if code_line[j - 1] == self.space: # Comma case 1
        temp = temp_line[:-1] + char
    elif len(code_line) > j + 1 and code_line[j + 1] not in [self.space, self.continuation_char, self.newline]: # Comma case 2
        temp = temp_line + char + self.space
    else:
        temp = temp_line + char
    return temp
