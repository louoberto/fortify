# ========================================================================
# Function: plus_spacing
# ========================================================================
# Purpose:
# Handles formatting for + and -
# ========================================================================
def plus_spacing(self, j, char, code_line, temp_line):
    if code_line[j + 1] != self.space and code_line[j - 1] != self.space:  # ?+?
        if code_line[j - 1] in ['D','d','E','e']:  # d+?
            if code_line[j - 2].isnumeric() and code_line[j + 1].isnumeric():  # 5d+5
                temp = temp_line + char
            else:  # ?d+?
                temp = temp_line + self.space + char + self.space
        else:  # ?+?
            if j == 0:
                temp = temp_line + char
            elif code_line[j - 1] == "=":  # =+?
                temp = temp_line + self.space + char
            else:  # ?+?
                temp = temp_line + self.space + char + self.space
    elif code_line[j - 1] == self.space and code_line[j + 1] != self.space:  # ? +?
        if code_line[j - 2] in ['=', ','] and code_line[j + 1].isnumeric(): # 
            # print(code_line)
            temp = temp_line + char
        else:
            # print(code_line[j - 2], code_line[j + 1], temp_line)
            temp = temp_line + char + self.space
    elif code_line[j - 1] != self.space and code_line[j + 1] == self.space:  # ?+ ?
        temp = temp_line + self.space + char
        # print(temp, code_line[:j+10])
    elif j == 0:
        print(code_line)
    else:  # ? + ?
        temp = temp_line + char
    
    return temp
