# ========================================================================
# Function: cvt_cmt_tab_ctn
# ========================================================================
# Purpose:
# Convert comment character from *, C, c to !
# In Fortran, only the first column can be *, C, or c. This changes it
# to be the modern !.
#
# Also if a fixed format file is given, this will force the line continuation
# character to be the continuation_char (default is &).
# ========================================================================
from no_format import no_format

def convert_comment_char(self):
    new_file_lines = []
    for line in self.file_lines:
        if line and not no_format(line): # Skip line if we are not to format it
            if line[0] in ['*','C','c']:
                line = "!" + line[1:]
            if "\t" in line:
                line = line.replace("\t", self.space * self.tab)

            if not self.free_form:
                if len(line) > 4 and (line[5] != self.space and line[5] != self.continuation_char):
                    line = line[:5] + self.continuation_char + line[6:]
        
        new_file_lines.append(line)
    self.file_lines = new_file_lines
    return
