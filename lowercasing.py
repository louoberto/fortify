# ========================================================================
# Function: lowercasing
# ========================================================================
# Purpose:
# Lowercase all code in the file, except for comments and strings
# Fortran compilers are case insensitive, and modern languages are
# typically lowercased. So, the code looks modern in this way
# ========================================================================
from no_format import no_format

def lowercasing(self):
    new_file_lines = []
    for line in self.file_lines:
        if no_format(line): # Skip line if we are not to format it
            pass
        else:
            # If the first character is a comment character, then the entire line is a comment
            if line[0] and (line[0].strip() in self.comments or line[0].strip() in "#"):
                pass
            else: # The first character was not a comment and it's not a pre-processor line
                cmt = line.find("!")
                if cmt != 0:  # A comment exists somewhere in the line
                    # We need to check for strings like "example1!" and 'example2!'
                    # Anything in a string needs to remain unformatted
                    temp = ""
                    double_quote_count = 0
                    single_quote_count = 0
                    commenter = False
                    for char in line:
                        if char == "'" and double_quote_count % 2 == 0: # then we have ex: 'example'
                            single_quote_count += 1
                        elif char == '"' and single_quote_count % 2 == 0: # then we have ex: "example"
                            double_quote_count += 1
                        if (
                            single_quote_count % 2 == 0
                            and double_quote_count % 2 == 0
                        ):  # There are no strings currently happenings
                            if char == "!":  # The rest of the line is a comment
                                commenter = True
                            if not commenter:
                                temp = temp + char.lower()
                            else:
                                temp = temp + char
                        else: # We are in the middle of a string
                            temp = temp + char
                    line = temp
                else:  # the entire line is a comment
                    pass
        new_file_lines.append(line)
    self.file_lines = new_file_lines
    return
