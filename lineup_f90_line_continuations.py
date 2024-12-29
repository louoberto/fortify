# ========================================================================
# Function: lineup_f90_line_continuations
# ========================================================================
# Purpose:
# This function lines up the continuation_char for free form. It does this
# by finding the farthest out ampersand, and lining up all others to it.
# ========================================================================
from no_format import no_format


def lineup_f90_line_continuations(self):
    new_file_lines = []
    open_paren = False
    for line in self.file_lines:
        if not no_format(line):
            if self.free_form and line.strip():
                if self.continuation_char == line[-2] and self.comment_char != line.strip()[0]:
                    if line.count("(") > line.count(")"):
                        starting_col = line.find("(") + 2
                        open_paren = True
                    elif open_paren and line.count("(") <= line.count(")"):
                        line = self.space * starting_col + line.lstrip()
                elif open_paren and line.count("(") <= line.count(")"):
                    line = self.space * starting_col + line.lstrip()
                    open_paren = False
            new_file_lines.append(line)
    return
