# ========================================================================
# Function: plus_spacing
# ========================================================================
# Purpose:
# Will format
# ========================================================================
def plus_spacing(self, j, char, code_line, temp_line):
    if code_line[j + 1] != self.space and code_line[j - 1] != self.space:  # ?+?
        if code_line[j - 1] == "e" or code_line[j - 1] == "d":  # d+?
            if code_line[j - 2].isnumeric() and code_line[j + 1].isnumeric():  # 5d+5
                temp = temp_line + char
            else:  # ?d+?
                temp = temp_line + self.space + char + self.space
        else:  # ?+?
            if code_line[j - 2] == "=":  # =+?
                temp = temp_line + self.space + char
            else:  # ?+?
                temp = temp_line + self.space + char + self.space
    elif code_line[j - 1] == self.space and code_line[j + 1] != self.space:  # ? +?
        temp = temp_line + char + self.space
    elif code_line[j - 1] != self.space and code_line[j + 1] == self.space:  # ?+ ?
        temp = temp_line + self.space + char
    else:  # ? + ?
        temp = temp_line + char

    return temp
