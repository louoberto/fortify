# ========================================================================
# Function: plus_spacing
# ========================================================================
# Purpose:
# Will format
# ========================================================================
from no_format import no_format


def plus_spacing(self, j, char, code_line, temp):
    if char in ["+", "-"]:
        if code_line[j + 1] != self.space and code_line[j - 1] != self.space:  # ?+?
            if code_line[j - 1] == "e" or code_line[j - 1] == "d":  # d+?
                if code_line[j - 2].isnumeric() and code_line[j + 1].isnumeric():  # 5d+5
                    temp += char
                else:  # ?d+?
                    temp += self.space + char + self.space
            else:  # ?+?
                if code_line[j - 2] == "=":  # =+?
                    temp += self.space + char
                else:  # ?+?
                    temp += self.space + char + self.space
        elif code_line[j - 1] == self.space and code_line[j + 1] != self.space:  # ? +?
            temp += char + self.space
        elif code_line[j - 1] != self.space and code_line[j + 1] == self.space:  # ?+ ?
            temp += self.space + char
        else:  # ? + ?
            temp += char
    else:
        temp += char
    return temp
