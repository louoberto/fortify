# ========================================================================
# Function: structured_indent
# ========================================================================
# Purpose:
# Will format  I believe this handles = - 0.213 to = -0.213 for example
# ========================================================================
from no_format import no_format


def lineup_f90_line_continuations(self):
    new_file_lines = []
    weopen = False
    for line in self.file_lines:
        if self.free_form and line.strip():
            if "&" == line[-2] and "!" != line.strip()[0]:
                if line.count("(") > line.count(")"):
                    starting_col = line.find("(") + 2
                    weopen = True
                elif weopen and line.count("(") <= line.count(")"):
                    line = " " * starting_col + line.lstrip()
            elif weopen and line.count("(") <= line.count(")"):
                line = " " * starting_col + line.lstrip()
                weopen = False
        new_file_lines.append(line)
    return
