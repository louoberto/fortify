# ========================================================================
# Function: comma_spacing
# ========================================================================
# Purpose:
# Should handle cases , related formatting
# ========================================================================
from inspect import currentframe
debug_me = 0

def comma_spacing(self, j, char, code_line, temp_line):
    if code_line[j - 1] == self.space: # Comma case 1
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        temp_line = temp_line[:-1]
    if len(code_line) > j + 1 and code_line[j + 1] not in [self.space, self.continuation_char, self.newline]: # Comma case 2
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        temp = temp_line + char + self.space
    elif not self.free_form and len(code_line) > j + 1 and code_line[j + 1] not in [self.space, self.newline]:
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        temp = temp_line + char + self.space
    else:
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        temp = temp_line + char
    return temp
