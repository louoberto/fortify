# ========================================================================
# Function: tab_to_spaces
# ========================================================================
# Purpose:
# Convert tab characters to spaces
# ========================================================================
def tab_to_spaces(self):
    new_file_lines = []
    for line in self.file_lines:
        if "\t" in line:
            new_file_lines.append(line.replace("\t", " " * self.tab))
        else:
            new_file_lines.append(line)
    self.file_lines = new_file_lines
    return
