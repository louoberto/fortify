# ========================================================================
# Function: paren_spacing
# ========================================================================
# Purpose:
# Handles formatting for objects around and inside parens ()
# ========================================================================
from inspect import currentframe
debug_me = 0

def paren_spacing(self, j, char, code_line, temp_line):
    if debug_me:
        self.debug(currentframe().f_lineno, char, code_line, j)
    if code_line.lower().startswith("if(") and j == 2:
        return temp_line + self.space + char

    if char == ")" and (j + 1 < len(code_line) and code_line[j + 1] not in [self.newline, self.space, '%', ')', ',',']', self.continuation_char]):
        # print(code_line, repr(code_line[j]),j)
        if (j + 2 >= len(code_line) or code_line[j + 1:j + 3] == '**'):
            # print(code_line, repr(code_line[j]),j)
            return temp_line + char
        elif code_line[j + 1] == "/" and code_line[j + 2] == ")":
            # print(code_line, repr(code_line[j]),j)
            return temp_line + char
        # print(code_line, repr(code_line[j]),j)
        return temp_line + char + (self.space if code_line[j + 1] not in [")", '.'] else "")
    else:
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        if code_line[j - 3:j] == '(/ ':
            if debug_me:
                self.debug(currentframe().f_lineno, char, code_line, j)
            return temp_line[:-1] + char
        else:
            # print(code_line[j-3:j])
            return temp_line + char
