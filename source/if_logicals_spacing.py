# ========================================================================
# Function: if_logicals_spacing
# ========================================================================
# Purpose:
# Adds spaces between logical expressions: x.gt.y to x .gt. y
# ========================================================================
def if_logicals_spacing(self, j, char, code_line, temp_line):
    if code_line[j - 4 : j + 1].lower() in self.iftypes:
        i = 5
    elif code_line[j - 3 : j + 1].lower() in self.iftypes2:
        i = 4
    elif code_line[j - 1].isnumeric() and not code_line[j + 1].isnumeric() and code_line[j + 1] != ')' and code_line[j + 1] != self.newline:
        if code_line[j:j+4].lower() not in self.iftypes2 and code_line[j:j+5].lower() not in self.iftypes and code_line[j+1] != self.space:
            temp = temp_line + char + self.space
        else:
            temp = temp_line + char
        return temp
    else:
        temp = temp_line + char
        return temp

    if code_line[j - i] != self.space and code_line[j + 1] != self.space: #?.gt.?
        if temp_line[-i] != self.space:
            temp = temp_line[:i-1] + self.space + temp_line[i-1:] + char + self.space
        else:
            temp = temp_line[:i-1] + temp_line[i-1:] + char + self.space
    elif code_line[j - i] not in [self.space, self.newline] and code_line[j + 1] == self.space:
        temp = temp_line[:i-1] + self.space + temp_line[i-1:] + char
    elif code_line[j - i] == self.space and code_line[j + 1] not in [self.space,self.continuation_char]:
        temp = temp_line + char + self.space
    else:
        temp = temp_line + char

    return temp
