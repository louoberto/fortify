# ========================================================================
# Function: paren_spacing
# ========================================================================
# Purpose:
# Handles formatting for objects around and inside parens ()
# ========================================================================
from inspect import currentframe
debug_me = 0

def paren_spacing(self, j, char, code_line, temp_line):
    # print(repr(code_line))
    is_char = False
    if code_line.lower().startswith('character'):
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
        if not is_char:
            if debug_me:
                self.debug(currentframe().f_lineno, char, code_line, j)
            if code_line[j + 1] not in [")", ".",'/']:
                if debug_me:
                    self.debug(currentframe().f_lineno, char, code_line, j)
                return temp_line + char + self.space
            else:
                # print(code_line, repr(code_line[j]),j)
                if debug_me:
                    self.debug(currentframe().f_lineno, char, code_line, j)
                if code_line[j + 1] == '/':
                    # print(repr(code_line))
                    if j + 2 == len(code_line) or code_line[j + 2] == '\n':
                        # print(repr(code_line))
                        return temp_line + char
                    elif len(code_line) > j + 2 and code_line[j + 2] != self.space:
                        # print(repr(code_line))
                        return temp_line + char + self.space
                    else:
                        # print(repr(code_line))
                        return temp_line + char
                else:
                    if debug_me:
                        self.debug(currentframe().f_lineno, char, code_line, j)
                    if code_line[j + 1] not in ['.']:
                        return temp_line + char + self.space
                    else:
                        # print(code_line, repr(code_line[j]),j)
                        if code_line[j+1:j + 5].lower() not in self.iftypes2 and code_line[j+1:j + 6].lower() not in self.iftypes:
                            # print(code_line[j+1:j + 5].lower(), repr(code_line[j]),j)
                            return temp_line + char
                        else:
                            return temp_line + char + self.space
        else:
            # print(temp_line)
            return temp_line + char + (self.space if (code_line[j + 1] not in [')', '.','*']) else "")
    else:
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        if code_line[j - 3:j] == '(/ ':
            if debug_me:
                self.debug(currentframe().f_lineno, char, code_line, j)
            return temp_line[:-1] + char
        else:
            # if debug_me:
            #     self.debug(currentframe().f_lineno, char, code_line, j)
            if temp_line[j-3:] == ' if':
                if debug_me:
                    self.debug(currentframe().f_lineno, char, code_line, j)
                return temp_line + self.space + char
            else:
                if debug_me:
                    self.debug(currentframe().f_lineno, char, code_line, j)
                if char == '(' and code_line[j-1] == 'f' and code_line[j-2] == 'i' and (j < 3 or not code_line[j-3].isalpha()):
                    if debug_me:
                        self.debug(currentframe().f_lineno, char, code_line, j)
                    return temp_line + self.space + char
                else:
                    if debug_me:
                        self.debug(currentframe().f_lineno, char, code_line, j)
                    return temp_line + char
