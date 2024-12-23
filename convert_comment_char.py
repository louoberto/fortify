# ========================================================================
# Function: convert_comment_char
# ========================================================================
# Purpose:
# Convert comment character from *, C, c to !
# In Fortran, only the first column can be *, C, or c. This changes it
# to be the modern !.
# ========================================================================
from no_format import no_format

def convert_comment_char(self):
    new_file_lines = []
    for line in self.file_lines:
        if no_format(line): # Skip line if we are not to format it
            pass
        else:
            # If the first character is a comment character, then the entire line is a comment
            # Force it to be ! from *, C, or c.
            if line[0] and line[0] in self.comments:
                line = "!" + line[1:]
        new_file_lines.append(line)
    self.file_lines = new_file_lines
    return
