# =============================================================================
# Function: format
# =============================================================================
# Purpose:
# The main formatting function. It runs all of the main formatting
# functions and stores them to be printed back in the driver.
# =============================================================================
from no_format import no_format


def format(self):
    new_file_lines = []
    slash_skip = False
    slash_cont = False
    line_num = 0
    pound_ifdef = False
    pound_else = False
    pound_endif = False
    self_skip_true = 0
    while line_num < len(self.file_lines):
        line = self.file_lines[line_num]
        # print(line)
        if not slash_cont:
            first_slash = True

        #======================================================================
        # Skip formatting if any of the following conditions are met
        #   1. If the line is blank (only a new line character)
        #   2. If a preprocessor directive is present or slash_skip is present
        #      slash_skip is a line continuation for directives
        #   3. Fixed format comment-only line
        #======================================================================
        if not line.strip(): # If blank line
            if line_num != len(self.file_lines):
                new_file_lines.append(self.newline)
            line_num += 1
            continue
        elif line.strip()[0] == '#' or slash_skip: # Preprocesser directive, leave line be
            new_file_lines.append(line)
            if line.strip()[-1] == '\\':
                slash_skip = True
            else:
                slash_skip = False
            if line.strip().startswith('#if'):
                pound_ifdef = True
                self.ifdefdent = self.indenter
                # print('ifd = ', self.ifdefdent, line)
            elif line.strip().startswith('#else') and pound_ifdef:
                pound_ifdef = False
                pound_else = True
                self.elsedent = self.ifdefdent
                # print(self.indenter)
                self.indenter = self.ifdefdent
                # print('ifdef = ', self.ifdefdent)
                # print('else = ', self.elsedent)
                # print(self.indenter)
            elif line.strip().startswith('#endif') and pound_ifdef or pound_else:
                pound_ifdef = False
                pound_else = False
                # print(self.indenter)
                # pound_endif = True
                # self.endifdent = self.indenter
                # print('end = ', self.endifdent, line)
            line_num += 1
            continue
        elif line[0] in ['*','C','c','!'] and not self.free_form: # Check for F77 comments
            # print(line)
            line = self.comment + line[1:] # Convert to what user wants
            while len(line) >= 2 and line[-2] == self.space: # Remove empty whitespace at the end of a comment-only line
                line = line[:-2] + line[-1:]
            new_file_lines.append(line) # Append and go back
            line_num += 1
            continue
        #======================================================================

        #======================================================================
        # This is for preserving the original comment character if the user
        # decides to do so on VSCode. It is put back at the end of the loop
        #======================================================================
        if not self.free_form:
            # print(line)
            old_comment = self.comment
            self.comment = '!'
        #======================================================================
        
        #======================================================================
        # Check for no format
        #======================================================================
        if no_format(self, line): # "No format" in the line
            new_file_lines.append(line)
            line_num += 1
            continue
        #======================================================================

        #======================================================================
        # Convert tab characters to spaces
        # This needs to be first to ensure proper character counting
        #======================================================================
        if self.tab in line:
            line = line.replace(self.tab, self.space * self.tab_len)
        #======================================================================
        
        #======================================================================
        # Standardize the line continuation character to & for fixed format
        #======================================================================
        if not self.free_form and len(line) >= 6 and line[5] != self.space and line[5] != self.continuation_char:
            line = line[:5] + self.continuation_char + line[6:]
        #======================================================================

        #======================================================================
        # Break up line into 3 parts: ff_line, code_line, cmnt_line
        #======================================================================
        ff_line, code_line, cmnt_line, should_cont = self.line_breakup(self, line)
        if not should_cont:
            new_file_lines.append(line)
            line_num += 1
            continue
        #======================================================================

        #======================================================================
        # Remove empty whitespace at the end of a comment-only line
        #======================================================================
        if not code_line:
            code_line = ff_line + code_line + cmnt_line
            while(len(code_line) > 1 and code_line[-2] == self.space):
                code_line = code_line[:-2] + code_line[-1:]
            if self.comment_behavior in [self.as_is, self.first_col]:
                new_file_lines.append(code_line)
                line_num += 1
                continue
        #======================================================================

        #======================================================================
        # Start of character processing for loop
        #======================================================================
        temp = self.empty
        single_quote_skip = False  # Skip strings
        double_quote_skip = False  # Skip strings
        comment_skip = False  # Skip comment
        for j, char in enumerate(code_line):
            # String check
            if char == "'" and not double_quote_skip:
                single_quote_skip = not single_quote_skip
            if char == '"' and not single_quote_skip:
                double_quote_skip = not double_quote_skip
            if not single_quote_skip and not double_quote_skip and char == self.comment:
                comment_skip = True
            if not single_quote_skip and not double_quote_skip and not comment_skip:
                if self.lowercasing: # User defined; default is true
                    char = char.lower() # Lowercase all working code; no global CAPS at this time
                if char == self.space:
                    temp = self.remove_extra_space(self, j, char, code_line, temp)
                elif char == ".":
                    temp = self.period_spacing(self, j, char, code_line, temp)
                elif char == self.semicolon:
                    temp = self.semicolon_spacing(self, j, char, code_line, temp, line_num, cmnt_line, ff_line)
                    # print(temp)
                    break
                elif char == ",":
                    temp = self.comma_spacing(self, j, char, code_line, temp)
                elif char == ":":
                    temp = self.colon_spacing(self, j, char, code_line, temp)
                elif char in ["(", ")", "[","]"]:
                    temp = self.paren_spacing(self, j, char, code_line, temp)
                elif char in ["/"]:
                    temp, first_slash, slash_cont = self.slash_spacing(self, j, char, code_line, temp, first_slash, line_num, slash_cont)
                elif char in ["<", ">", "="]:
                    temp = self.relational_op_spacing(self, j, char, code_line, temp)
                elif len(code_line) > j + 1 and char == "*" and "*" not in [code_line[j - 1], code_line[j + 1]] and code_line[j - 4 : j] not in self.data_types:
                    # print(code_line)
                    temp = self.star_spacing(self, j, char, code_line, temp)
                elif char in ["+", "-"]:
                    temp = self.plus_spacing(self, j, char, code_line, temp)
                else:
                    temp += char
            else:
                temp += char
            #==================================================================
            # End of character processing for loop
            #==================================================================

        #======================================================================
        # Structured indenting/nesting
        #======================================================================
        # print(repr(temp), self.indenter)
        temp, self_skip_true = self.structured_indent(self, temp, line_num, ff_line, self_skip_true)
        #======================================================================
        self.lines.append(temp)
        self.code_line = temp # Save the current line for knowledge on the next line

        #======================================================================
        # We skip this if in the middle of a string. Otherwise we need to see 
        # if the formatter pushed the line past the last usable column
        #======================================================================
        if not comment_skip:
            temp1, temp2 = self.line_carry_over(self, ff_line, temp, cmnt_line)
            temp = temp1 + temp2
        #======================================================================

        #======================================================================
        # Always make sure the line ends in a newline character
        #======================================================================
        if (temp[-1] != self.newline) and (line_num < len(self.file_lines) - 1):
            # print(line_num, len(self.file_lines))
            temp += self.newline
        #======================================================================

        #======================================================================
        # Change the F77 comment back to whatever it was to begin with
        #======================================================================
        if not self.free_form:
            self.comment = old_comment
        #======================================================================

        new_file_lines.append(temp)
        line_num += 1
        #======================================================================
        # End of while loop
        #======================================================================

    self.file_lines = new_file_lines
    return
