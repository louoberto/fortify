# ========================================================================
# Function: paren_spacing
# ========================================================================
# Purpose:
# Handles formatting for objects around and inside parens ()
# ========================================================================
import re
from inspect import currentframe
debug_me = 0

def paren_spacing(self, j, char, code_line, temp_line):
    is_char = False
    if code_line.startswith('character '):
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        is_char = True
    if debug_me:
        self.debug(currentframe().f_lineno, char, code_line, j)
    if code_line.lower().startswith("if(") and j == 2:
        return temp_line + self.space + char

    if char == ")" and (j + 1 < len(code_line) and code_line[j + 1] not in [self.newline, self.space, '%', ')', ',',']', self.continuation_char]):
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        # print(code_line, repr(code_line[j]),j)
        if (j + 2 >= len(code_line) or code_line[j + 1:j + 3] == '**'):
            if debug_me:
                self.debug(currentframe().f_lineno, char, code_line, j)
            # print(code_line, repr(code_line[j]),j)
            return temp_line + char
        elif code_line[j + 1] == "/" and code_line[j + 2] == ")":
            if debug_me:
                self.debug(currentframe().f_lineno, char, code_line, j)
            # print(code_line, repr(code_line[j]),j)
            return temp_line + char
        # print(code_line, repr(code_line[j]),j)
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        return temp_line + char + (self.space if (code_line[j + 1] not in [")", '.'] and not is_char) else "")
    else:
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        if code_line[j - 3:j] == '(/ ':
            if debug_me:
                self.debug(currentframe().f_lineno, char, code_line, j)
            return temp_line[:-1] + char
        else:
            if debug_me:
                self.debug(currentframe().f_lineno, char, code_line, j)
            if temp_line[j-3:] == ' if':
                # if debug_me:
                # self.debug(currentframe().f_lineno, char, code_line, j)
                return temp_line + self.space + char
            else:
                if char == '(' and code_line[j-1] == 'f' and code_line[j-2] == 'i' and (j < 3 or not code_line[j-3].isalpha()):
                    if debug_me:
                        self.debug(currentframe().f_lineno, char, code_line, j)
                    return temp_line + self.space + char
                else:
                    return temp_line + char
