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
            if code_line[j + 1] == ")":
                # print(code_line)
                temp = temp_line + char
            else:
                temp = temp_line + char + self.space
        else:
            temp = temp_line + char
    else:
        temp = temp_line + char
    # print(repr(char), repr(code_line))
    # print(len(temp))
    # print(code_line)
    if char == ')' and len(temp) > 1:
        while len(temp) > 1 and temp[-2].isspace():
            temp = temp[:-2] + temp[-1]
    # if char == '(':
    #     print(repr(temp))
    # print(temp)
    return temp
