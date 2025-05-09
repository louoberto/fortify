# ========================================================================
# Function: slash_spacing
# ========================================================================
# Purpose:
# Similar to relational_op_spacing except extra code is needed for slash
# spacing
# ========================================================================
from inspect import currentframe
debug_me = 0

def slash_spacing(self, j, char, code_line, temp_line, first_slash, i, slash_cont):
    if debug_me:
        self.debug(currentframe().f_lineno, char, code_line, j)
    # ====================================================================
    # Concerning single slash on a common type or data type
    # For example real foo /123/
    # ====================================================================
    # print(slash_cont, temp_line)
    if slash_cont or any(temp_line.lower().startswith(keyword) for keyword in self.common_types) or (any(temp_line.lower().startswith(keyword) for keyword in self.data_types) and ', parameter' not in temp_line):
        # print(slash_cont, temp_line)
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        if len(self.file_lines) > i + 1 and len(self.file_lines[i + 1]) > 5 and self.file_lines[i + 1][5] == self.continuation_char:
            slash_cont = True
        else:
            slash_cont = False
        if first_slash:
            # print(slash_cont, temp_line)
            first_slash = False
            if temp_line[-1] not in [self.space, '(']:
                # self.debug(currentframe().f_lineno, char, code_line, j)
                return temp_line + self.space + char, first_slash, slash_cont
        else:
            # print(slash_cont, temp_line)
            first_slash = True
            if len(code_line) > j + 1 and code_line[j + 1] not in [self.space,'\n',',',')']:
                # self.debug(currentframe().f_lineno, char, code_line, j)
                return temp_line + char + self.space, first_slash, slash_cont
        # print(slash_cont, temp_line)
        return temp_line + char, first_slash, slash_cont
    # ====================================================================
    # Other slash processing
    # ====================================================================
    elif len(code_line) > j + 1 and code_line[j + 1] != self.space: # ?/?
        if debug_me:
            self.debug(currentframe().f_lineno, char, code_line, j)
        if code_line[j - 1] != '=' and ')' not in [code_line[j - 1], code_line[j + 1]]: # ?/?
            if debug_me:
                self.debug(currentframe().f_lineno, char, code_line, j)
            if code_line[j + 1] == '/':
                if debug_me:
                    self.debug(currentframe().f_lineno, char, code_line, j)
                temp = temp_line + (self.space if code_line[j - 1] != self.space and j > 0 else self.empty) + char
            elif code_line[j - 1] in ['/', '.']:# and not code_line.startswith('namelist /') and temp_line != 'namelist ':
                if debug_me:
                    self.debug(currentframe().f_lineno, char, code_line, j)
                if temp_line[-1].isspace() and code_line[j - 1] == '/':
                    temp = temp_line[:-1] + char + self.space
                else:
                    temp = temp_line + char + self.space
            elif code_line[j - 1] in ['(', self.space] or code_line[j + 1] == self.newline:
                if debug_me:
                    self.debug(currentframe().f_lineno, char, code_line, j)
                if (code_line[j - 1] == self.space and not code_line[j - 2].isalnum()) or code_line[j - 1] == '(':
                    if debug_me:
                        self.debug(currentframe().f_lineno, char, code_line, j)
                    temp = temp_line + char
                else:
                    if debug_me:
                        self.debug(currentframe().f_lineno, char, code_line, j)
                    if code_line[j + 1] == self.newline:
                        if code_line[j - 1] == self.space:
                            temp = temp_line + char
                        else:
                            temp = temp_line + self.space + char
                    else:
                        if code_line[j - 1] == self.space:
                            if code_line[j + 1] in [',','=']:
                                temp = temp_line + char
                            else:
                                temp = temp_line + char + self.space
                        else:
                            temp = temp_line + self.space + char + self.space
            elif code_line[j + 1] == ',':
                temp = temp_line + self.space + char
            else:
                if debug_me:
                    self.debug(currentframe().f_lineno, char, code_line, j)
                if code_line[j - 1] not in [self.space,',']:
                    if debug_me:
                        self.debug(currentframe().f_lineno, char, code_line, j)
                    if code_line[j + 1] == '=':
                        temp = temp_line + self.space + char
                    else:
                        temp = temp_line + self.space + char + self.space
                else:
                    if debug_me:
                        self.debug(currentframe().f_lineno, char, code_line, j)
                    if code_line[j + 1] in [self.space,"'",]:
                        if debug_me:
                            self.debug(currentframe().f_lineno, char, code_line, j)
                        temp = temp_line + char
                    else:
                        # print(code_line, repr(code_line[j]),j)
                        temp = temp_line + char + self.space
        elif code_line[j + 1] == ')':
            if debug_me:
                self.debug(currentframe().f_lineno, char, code_line, j)
            if code_line[j - 2] == ')' and code_line[j - 1] == self.space:
                temp = temp_line[:-1] + char
            else:
                temp = temp_line + char
        else:
            # print(code_line, repr(code_line[j]),j)
            if code_line[j + 1] == '/':
                temp = temp_line + char
            else:
                temp = temp_line + char + self.space
    elif code_line[j - 1] != self.space:
        # print(code_line, repr(code_line[j]),j)
        if code_line[j - 1] in ['(',')','<','>','/','=']:
            temp = temp_line + char
        else:
            temp = temp_line + self.space + char
    else:
        # print(code_line, repr(code_line[j]),j)
        temp = temp_line + char
    return temp, first_slash, slash_cont
