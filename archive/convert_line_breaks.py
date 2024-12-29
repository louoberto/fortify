# ========================================================================
# Function: convert_line_breaks
# ========================================================================
# Purpose:
# If a fixed format file is given, this will force the line continuation
# character to be the continuation_char (default is &).
# ========================================================================
def convert_line_breaks(self):
    new_file_lines = []
    if not self.free_form:  # Make sure we are fixed form
        for line in self.file_lines:
            if line.strip():  # Make sure the line has something
                # Make sure the first column is not a comment character,
                # thus the entire line is not a comment and check to
                # make sure the line is longer than 6 characters for good measure
                if line.strip()[0] != "!" and len(line) >= 6 and line[5] != " ":
                    line = line[:5] + self.continuation_char + line[6:]
            new_file_lines.append(line)
        self.file_lines = new_file_lines
    return
