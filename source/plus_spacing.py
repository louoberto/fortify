# ========================================================================
# Function: plus_spacing
# ========================================================================
# Purpose:
# Handles formatting for + and -
# ========================================================================
def plus_spacing(self, j, char, code_line, temp_line):
    if len(code_line) > j + 1 and self.space not in [code_line[j - 1], code_line[j + 1]]:  # ?+?
        if code_line[j - 1] in ['D','d','E','e']:  # d+?
            if code_line[j - 2].isnumeric() and code_line[j + 1].isnumeric():  # 5d+5
                temp = temp_line + char
            else:  # ?d+?
                temp = temp_line + self.space + char + self.space
        else:  # ?+?
            if j == 0:
                temp = temp_line + char
            elif code_line[j - 1] == "=":  # =+?
                temp = temp_line + char #self.space + char
            else:  # ?+?
                if code_line[j - 1] not in ['(',')','.','/',',']:
                    temp = temp_line + self.space + char
                    if (code_line[j + 1].isalnum() and code_line[j - 1].isalnum()) or code_line[j + 1] in ['(']:
                        temp += self.space
                elif code_line[j - 1] in ['(',')'] and temp_line[-1] != self.space:
                    temp = temp_line + char
                elif code_line[j - 1] in ['.'] and (code_line[j - 4 : j].lower() in self.iftypes2 or code_line[j - 5 : j].lower() in self.iftypes):
                    temp = temp_line + char
                elif code_line[j - 1] in ['/',',']:
                    temp = temp_line + char
                else:
                    
                    temp = temp_line + char + self.space
    elif len(code_line) > j + 1 and code_line[j - 1] == self.space and code_line[j + 1] != self.space:  # ? +?
        if code_line[j - 2] in ['=', ','] and (code_line[j + 1].isalnum() or code_line[j + 1] == '('):
            temp = temp_line + char
        else:
            if code_line[j - 1] == self.space and (code_line[j + 1].isalnum() or code_line[j + 1] == self.newline):
                temp = temp_line + char
            else:
                temp = temp_line + char + self.space
    elif len(code_line) > j + 1 and code_line[j - 1] != self.space and code_line[j + 1] == self.space:  # ?+ ?
        if j == 0:
            temp = temp_line + char
        else:
            temp = temp_line + self.space + char
    else:  # ? + ?
        temp = temp_line + char
    
    return temp
