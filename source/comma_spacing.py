# ========================================================================
# Function: comma_spacing
# ========================================================================
# Purpose:
# Should handle cases :: and , related formatting
# ========================================================================
def comma_spacing(self, j, char, code_line, temp_line):
    if code_line[j - 1] == self.space: # Comma case 1
        # print(repr(code_line.strip()))
        temp = temp_line[:-1] + char
    elif len(code_line) > j + 1 and code_line[j + 1] not in [self.space, self.continuation_char]: # Comma case 2
        temp = temp_line + char + self.space
    else:
        # print(repr(code_line.strip()))
        #print(code_line)
        temp = temp_line + char
    return temp
