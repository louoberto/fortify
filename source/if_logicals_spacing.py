# ========================================================================
# Function: if_logicals_spacing
# ========================================================================
# Purpose:
# Adds spaces between logical expressions: x.gt.y to x .gt. y
# ========================================================================
def if_logicals_spacing(self, j, char, code_line, temp_line):
    if code_line[j - 4 : j + 1].lower() in self.iftypes:
        if code_line[j - 5] != self.space and code_line[j + 1] != self.space:
            if temp_line[-5] != self.space:
                temp = temp_line[:-4] + self.space + temp_line[-4:] + char + self.space
            else:
                temp = temp_line[:-4] + temp_line[-4:] + char + self.space
        elif code_line[j - 5] != self.space and code_line[j + 1] == self.space:
            temp = temp_line[:-4] + self.space + temp_line[-4:] + char
        elif code_line[j - 5] == self.space and code_line[j + 1] != self.space:
            temp = temp_line + char + self.space
        else:
            temp = temp_line + char
    elif code_line[j - 3 : j + 1].lower() in self.iftypes2:
        if code_line[j - 4] != self.space and code_line[j + 1] != self.space: #?.gt.?
            if temp_line[-4] != self.space:# and code_line[-2] != self.continuation_char:
                temp = temp_line[:-3] + self.space + temp_line[-3:] + char + self.space
            else:
                temp = temp_line[:-3] + temp_line[-3:] + char + self.space
        elif code_line[j - 4] not in [self.space, '\n'] and code_line[j + 1] == self.space:
            # print(repr(code_line))
            # print(temp_line[:-3] + self.space + temp_line[-3:] + char)
            temp = temp_line[:-3] + self.space + temp_line[-3:] + char
        elif code_line[j - 4] == self.space and code_line[j + 1] not in [self.space,self.continuation_char]:
            temp = temp_line + char + self.space
        else:
            temp = temp_line + char
    elif code_line[j - 1].isnumeric() and not code_line[j + 1].isnumeric() and code_line[j + 1] != ')' and code_line[j + 1] != '\n':
        if code_line[j:j+4].lower() not in self.iftypes2 and code_line[j:j+5].lower() not in self.iftypes and code_line[j+1] != self.space:
            temp = temp_line + char + self.space
        else:
            temp = temp_line + char
    else:
        temp = temp_line + char
    return temp
