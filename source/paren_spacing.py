# ========================================================================
# Function: paren_spacing
# ========================================================================
# Purpose:
# Handles formatting for objects around and inside parens ()
# ========================================================================
def paren_spacing(self, j, char, code_line, temp_line):
    if code_line.lower().startswith("if(") and j == 2:
        return temp_line + self.space + char

    if char == ")" and (j + 1 < len(code_line) and code_line[j + 1] not in [self.newline, self.space, '%', ')', ',', self.continuation_char]):
        if (j + 2 >= len(code_line) or code_line[j + 1:j + 3] == '**'):
            return temp_line + char
        return temp_line + char + (self.space if code_line[j + 1] != ")" else "")

    return temp_line + char
