# ========================================================================
# Function: minus_spacing
# ========================================================================
# Purpose:
# This handles this case: = - 0.213 to = -0.213
# ========================================================================
#(not self.free_form and ff_line[-1] == '&' and j == 0)
def minus_spacing(self, j, char, code_line, temp_line):
    if code_line[j-1] in ['-','+','/','*'] and code_line[j - 2] == self.space:
        temp = temp_line[:-1]
        # print(temp)
    else:
        # print(code_line)
        temp = temp_line[:-1] + char
    return temp
