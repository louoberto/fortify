# ========================================================================
# Function: colon_spacing
# ========================================================================
# Purpose:
# 
# ========================================================================
from inspect import currentframe
import re
debug_me = 0

def colon_spacing(self, j, char, code_line, temp_line):
    if debug_me:
        self.debug(currentframe().f_lineno, char, code_line, j)
    if re.search(r"^[a-z0-9_]+:*" + re.escape('do ') + r"\b", code_line.lower()):
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        return temp_line + char + self.space 
    else:
        # print(code_line, repr(code_line[j]),j)
        return temp_line + char
