# ========================================================================
# Function: period_spacing
# ========================================================================
# Purpose:
# Adds spaces between logical expressions: x.gt.y to x .gt. y
# ========================================================================
from inspect import currentframe
debug_me = 0

def period_spacing(self, j, char, code_line, temp_line):
    # print(repr(code_line))
    if code_line[j - 4:j + 1].lower() in self.iftypes:
        i = 5
    elif code_line[j - 3:j + 1].lower() in self.iftypes2:
        i = 4
    elif code_line[j - 1].isnumeric() and len(code_line) > j + 1 and not code_line[j + 1].isnumeric() and code_line[j + 1] not in [')', self.newline, 'D', 'd', 'E', 'e','_']:
        # print(repr(code_line))
        if code_line[j:j + 4].lower() not in self.iftypes2 and code_line[j:j + 5].lower() not in self.iftypes and code_line[j + 1] != self.space:
            if code_line[j+1:j + 3] == '/)':
                # print(repr(code_line[j+1:j + 3]))
                temp = temp_line + char
            else:
                temp = temp_line + char + self.space
        else:
            temp = temp_line + char
        return temp
    else:
        # print(repr(code_line))
        # if code_line[j-1] == ')':
        #     print(repr(code_line[:j]), repr(temp_line))
        temp = temp_line + char
        return temp

    if code_line[j - i] != self.space and code_line[j + 1] != self.space: #?.gt.?
        if len(temp_line) >= i and temp_line[-i] not in [self.space, '(']:
            temp = temp_line[:1 - i] + self.space + temp_line[1 - i:] + char + self.space
        else:
            temp = temp_line[:1 - i] + temp_line[1 - i:] + char + self.space
    elif code_line[j - i] not in [self.space, self.newline, '(',')'] and code_line[j + 1] == self.space:
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        temp = temp_line[:1 - i] + self.space + temp_line[1 - i:] + char
    elif code_line[j - i] == self.space and len(code_line) > j + 1 and code_line[j + 1] not in [self.space, self.continuation_char]:
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        temp = temp_line + char + self.space
    else:
        temp = temp_line + char

    return temp
