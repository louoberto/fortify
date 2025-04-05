# ========================================================================
# Function: semicolon_spacing
# ========================================================================
# Purpose:
# Finds semicolons in the code and adds a new line after it.
# ========================================================================
def semicolon_spacing(self, line, i):
    while self.semicolon in line:
        index = line.index(self.semicolon)
        # Add before part if not empty
        if index > 0:
            self.file_lines[i+1:i+1]= (line[:index + 1])
        # Update line to the remaining part
        line = line[index + 1:]

    return line


# if word == "apple":
#         # Insert new words directly after current word
#         words[i+1:i+1] = ["cherry", "date"]