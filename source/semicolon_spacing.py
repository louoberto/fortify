# ========================================================================
# Function: semicolon_spacing
# ========================================================================
# Purpose:
# Finds semicolons in the code and adds a new line after it.
# ========================================================================
def semicolon_spacing(self, j, char, code_line, temp_line, i, cmnt_line, ff_line):
    if j > 0 and code_line[j+1:].strip():
        self.file_lines[i+1:i+1] = [ff_line + code_line[j + 1:]]
    if cmnt_line:
        return temp_line + char
    else:
        return temp_line + char + '\n'