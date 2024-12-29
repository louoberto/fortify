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
from no_format import no_format

def remove_extra_spaces(self):
    new_file_lines = []
    for line in self.file_lines:
        # Skip blank lines
        if not line.strip():
            new_file_lines.append(line)
            continue

        # Skip formatting if any of the following conditions are met
        #   1. If there is a comment in the first column
        #   2. FORMAT statement is in the line. Should make this more robust...
        #   3. There is a "do not fortify" in the line.
        #   4. Preprocessor directive
        cmt_index = line.find("!")
        if cmt_index == 0 or "format" in line[:cmt_index] or no_format(line) or "#" in line.strip()[0]:
            new_file_lines.append(line)
            continue
        if cmt_index > 0:
            code_line = line[:cmt_index]
            cmnt_line = line[cmt_index:]
        else:
            code_line = line
            cmnt_line = ""
        
        if not self.free_form:
            ff_line = code_line[:self.ff_column_len]
            code_line = code_line[self.ff_column_len:]
        else:
            ff_line = ""
        
        while ("  " in code_line):
            code_line = code_line.replace("  ", " ")
        
        new_file_lines.append(ff_line + code_line + cmnt_line[:-1])
    self.file_lines = new_file_lines
    return


            
