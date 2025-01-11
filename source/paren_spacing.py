# ========================================================================
# Function: paren_spacing
# ========================================================================
# Purpose:
# Handles formatting for objects around and inside parens ()
# ========================================================================
def paren_spacing(self, j, char, code_line, temp_line):
    if code_line.lower().startswith("if(") and j == 2:
        temp = temp_line + self.space + char
    elif char == ")" and (j + 1 < len(code_line) and code_line[j + 1] and code_line[j + 1] not in [self.newline, self.space, '%' ,')',',',self.continuation_char]):
        if (j + 2 < len(code_line) and code_line[j + 2] and code_line[j + 1:j + 3] not in ['**']):
            temp = temp_line + char + self.space
        else:
            temp = temp_line + char
    # elif code_line[j - 1] in ['+','-']:
    #     temp = temp_line + self.space + char
    else:
        temp = temp_line + char
    return temp
