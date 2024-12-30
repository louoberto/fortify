# ========================================================================
# Function: if_logicals_spacing
# ========================================================================
# Purpose:
# Adds spaces between logical expressions: x.gt.y to x .gt. y
# ========================================================================
def if_logicals_spacing(self, j, char, code_line, temp_line):
    if code_line[j - 4 : j + 1].lower() in self.iftypes:
        if code_line[j - 5] != self.space and code_line[j + 1] != self.space:
            temp = temp_line[:-4] + self.space + temp_line[-4:] + char + self.space
        elif code_line[j - 5] != self.space and code_line[j + 1] == self.space:
            temp = temp_line[:-4] + self.space + temp_line[-4:] + char
        elif code_line[j - 5] == self.space and code_line[j + 1] != self.space:
            temp = temp_line + char + self.space
        else:
            temp = temp_line + char
    elif code_line[j - 3 : j + 1].lower() in self.iftypes2:
        if code_line[j - 4] != self.space and code_line[j + 1] != self.space:
            temp = temp_line[:-3] + self.space + temp_line[-3:] + char + self.space
        elif code_line[j - 4] != self.space and code_line[j + 1] == self.space:
            temp = temp_line[:-3] + self.space + temp_line[-3:] + char
        elif code_line[j - 4] == self.space and code_line[j + 1] != self.space:
            temp = temp_line + char + self.space
        else:
            temp = temp_line + char
    else:
        temp = temp_line + char
    return temp
