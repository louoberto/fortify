# ========================================================================
# Function: relational_op_spacing
# ========================================================================
# Purpose:
# Ensures that there is a space before and after rel_ops
# E.g. x<=4 turns into x <= 4
#
# General algorithm is as follows. For each line we check:
# 1. Is there a comment? If so, is it in column 0? If not, take only the line
#    up to the comment.
# 2. Then check if code contains <, <=, >, >=, /=, ==, //
# 3. If so, check if there is a space already between rel_ops. If not,
#    add space to either side of the line.
# ========================================================================
def relational_op_spacing(self, j, char, code_line, temp_line):
    if len(code_line) > j + 1 and code_line[j + 1] == "=": # ?==, ?+=, ?-=, ?/=
        if code_line[j - 1] != self.space: # ?==, ?+=, ?-=, ?/=
            temp = temp_line + self.space + char
        else: # ? ==, ? +=, ? -=, ? /=
            temp = temp_line + char
    elif len(code_line) > j + 1 and code_line[j + 1] != self.space: # ?=?, ?+?, ?-?, ?/?
        # print(code_line, repr(code_line[j]),j)
        if code_line[j - 1] != '=' and ')' not in [code_line[j - 1], code_line[j + 1]]: # ?=?, ?+?, ?-?, ?/?
            if char == '/':
                # print(code_line, repr(code_line[j]),j)
                if code_line[j + 1] == '/':
                    # print(code_line, repr(code_line[j]),j)
                    temp = temp_line + (self.space if code_line[j - 1] != self.space and j > 0 else self.empty) + char
                elif code_line[j - 1] in ['/', '.']:# and not code_line.startswith('namelist /') and temp_line != 'namelist ':
                    # print(code_line, repr(code_line[j]),j)
                    if temp_line[-1].isspace() and code_line[j - 1] == '/':
                        temp = temp_line[:-1] + char + self.space
                    else:
                        temp = temp_line + char + self.space
                elif code_line[j - 1] in ['(', self.space] or code_line[j + 1] == self.newline:
                    if (code_line[j - 1] == self.space and not code_line[j - 2].isalnum()) or code_line[j - 1] == '(':
                        temp = temp_line + char
                    else:
                        if code_line[j + 1] == self.newline:
                            if code_line[j - 1] == self.space:
                                temp = temp_line + char
                            else:
                                temp = temp_line + self.space + char
                        else:
                            if code_line[j - 1] == self.space:
                                if code_line[j + 1] == ',':
                                    temp = temp_line + char
                                else:
                                    temp = temp_line + char + self.space
                            else:
                                temp = temp_line + self.space + char + self.space
                elif code_line[j + 1] == ',':
                    temp = temp_line + self.space + char
                else:
                    # print(code_line, repr(code_line[j]),j)
                    if code_line[j - 1] != self.space:
                        temp = temp_line + self.space + char + self.space
                    else:
                        temp = temp_line + char + self.space
            else:
                # print(code_line, repr(code_line[j]),j)
                if code_line[j - 1] != self.space:
                    temp = temp_line + self.space + char + self.space
                else:
                    if code_line[j + 1] != self.newline:
                        temp = temp_line + char + self.space
                    else:
                        temp = temp_line + char
        elif code_line[j + 1] == ')':
            temp = temp_line + char
        else:
            # print(code_line, repr(code_line[j]),j)
            if char == '/' and code_line[j + 1] == '/':
                temp = temp_line + char
            else:
                temp = temp_line + char + self.space
    elif code_line[j - 1] != self.space:
        if code_line[j - 1] in ['(',')','<','>','/','=']:
            temp = temp_line + char
        else:
            temp = temp_line + self.space + char
    else:
        temp = temp_line + char
    return temp
