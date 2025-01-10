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
    if code_line[j + 1] == "=": # ?==, ?+=, ?-=, ?/=
        if code_line[j - 1] != self.space: # ?==, ?+=, ?-=, ?/=
            temp = temp_line + self.space + char
        else: # ? ==, ? +=, ? -=, ? /=
            temp = temp_line + char
    elif code_line[j + 1] != self.space: # ?=?, ?+?, ?-?, ?/?
        if code_line[j - 1] != '=' and ')' not in [code_line[j - 1], code_line[j + 1]]: # ?=?, ?+?, ?-?, ?/?
            if char == '/':
                if code_line[j + 1] == '/':
                    temp = temp_line + (self.space if code_line[j - 1] != self.space else self.empty) + char
                elif code_line[j - 1] in ['/', '.']:
                    temp = temp_line + char + self.space
                elif code_line[j - 1] in ['(', self.space] or code_line[j + 1] == self.newline:
                    temp = temp_line + char
                elif code_line[j + 1] == ',':
                    temp = temp_line + self.space + char
                else:
                    temp = temp_line + self.space + char + self.space
            else:
                if code_line[j - 1] != self.space:
                    temp = temp_line + self.space + char + self.space
                else:
                    temp = temp_line + char + self.space
        elif code_line[j + 1] == ')':
            temp = temp_line + char
        else:
            temp = temp_line + char + self.space
    elif code_line[j - 1] != self.space:
        if code_line[j - 1] in ['(',')','<','>','/']:
            temp = temp_line + char
        else:
            temp = temp_line + self.space + char
    else:
        temp = temp_line + char
    return temp
