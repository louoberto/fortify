# ========================================================================
# Function: star_spacing
# ========================================================================
# Purpose:
# Handles formatting * (asterisk) code
# ========================================================================
from inspect import currentframe
debug_me = 0

def star_spacing(self, j, char, code_line, temp_line):
    if debug_me:
        self.debug(currentframe().f_lineno, char, code_line, j)
    is_char = False
    if code_line.startswith('character '):
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        is_char = True
    if code_line[j - 1] != self.space and code_line[j + 1] != self.space: #?*?
        if code_line[j - 1].isalnum() and (code_line[j + 1].isalnum() or code_line[j + 1] == '('): #5*5
            for type in self.data_types:
                if (code_line.lower().startswith(type) and len(type) == j) or is_char:
                    temp = temp_line + char
                    break
                else:
                    if debug_me:
                        self.debug(currentframe().f_lineno, char, code_line, j)
                    temp = temp_line + self.space + char + self.space
        elif code_line[j - 1].isalnum() and not code_line[j + 1].isalnum(): #5*?
            if debug_me:
                self.debug(currentframe().f_lineno, char, code_line, j)
            temp = temp_line + self.space + char
        elif not code_line[j - 1].isalnum() and code_line[j + 1].isalnum(): #?*5
            if debug_me:
                self.debug(currentframe().f_lineno, char, code_line, j)
            if is_char:
                if debug_me:
                    self.debug(currentframe().f_lineno, char, code_line, j)
                temp = temp_line + char
            else:
                temp = temp_line + char + self.space
        elif code_line[j + 1] == '(':
            temp = temp_line + char + self.space
        else: #?*?
            temp = temp_line + char
    elif code_line[j - 1] == self.space and code_line[j + 1] != self.space: # ? *?
        if code_line[j + 1].isalnum() or code_line[j + 1] == '(': #? *5
            temp = temp_line + char + self.space
        else: #? *?
            temp = temp_line + char
    elif code_line[j - 1] != self.space and code_line[j + 1] == self.space: #?* ?
        if code_line[j - 1].isalnum(): #5* ?
            temp = temp_line + self.space + char
        else: #?* ?
            temp = temp_line + char
    else: # ? * ?
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        temp = temp_line + char

    return temp
