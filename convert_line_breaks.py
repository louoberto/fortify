# ========================================================================
# Function: convert_line_breaks
# ========================================================================
# Purpose:
# If a fixed format file is given, this will force the line continuation
# character to be an ampersand. It is most common and in free form
# it must be an ampersand.
# ========================================================================
comments = ['*', 'c', 'C', '!']
def convert_line_breaks(self):
    """
    If we have line breaks, force using & as the character
    """
    new_file_lines = []
    if not self.free_form:  # Make sure we are fixed form
        for line in self.file_lines:
            if line.strip():  # Make sure the line has something
                # Make sure the first column is not a comment character, 
                # thus the entire line is not a comment and check to 
                # make sure the line is longer than 6 characters for good measure
                if line.strip()[0] not in comments and len(line) >= 6 and line[5] != ' ':
                    line = line[:5] + "&" + line[6:] 
        new_file_lines.append(line)
    self.file_lines = new_file_lines
    return self
