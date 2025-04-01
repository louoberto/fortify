# ========================================================================
# Function: format
# ========================================================================
# Purpose:
# The main formatting function. It runs all of the main formatting
# functions and stores them to be printed back in the driver.
# ========================================================================
from no_format import no_format


def format(self):
    indenter = 0
    skip = False
    first_case = False
    select_indent = False
    new_file_lines = []
    do_list = []
    do_count = 0
    for i, line in enumerate(self.file_lines):
        # print(line)
        first_slash = True
        # print(line[0])
        # Skip formatting if any of the following conditions are met
        if not line.strip(): # If blank line
            if i != len(self.file_lines):
                new_file_lines.append(self.newline)
            continue
        elif line.strip()[0] == '#': # Preprocesser directive, leave line be
            new_file_lines.append(line)
            continue
        elif line[0] in ['*','C','c','!'] and not self.free_form: # Check for F77 comments
            # print(line)
            line = self.comment + line[1:] # Convert to what user wants
            while(line[-2] == self.space): # Remove empty whitespace at the end of a comment-only line
                line = line[:-2] + line[-1:]
            new_file_lines.append(line) # Append and go back
            continue
        elif not self.free_form: # We've dealt with column 0 comments, so change this to '!'
            # print(line)
            old_comment = self.comment
            self.comment = '!'
        
        if no_format(self, line): # "No format" in the line
            new_file_lines.append(line)
            continue

        # Convert tab characters to spaces
        # This needs to be first to ensure proper character counting
        if self.tab in line:
            line = line.replace(self.tab, self.space * self.tab_len)
        
        # Standardize the line continuation character to & for fixed format
        if not self.free_form and len(line) >= 6 and (line[5] != self.space and line[5] != self.continuation_char):
            line = line[:5] + self.continuation_char + line[6:]

        # Break up line into 3 parts: ff_line, code_line, cmnt_line
        cmt_index = line.find(self.comment)
        if cmt_index > 0:
            if not self.free_form:
                code_line = line[self.ff_column_len:cmt_index].lstrip()
                ff_line = line[:self.ff_column_len]
            else:
                code_line = line[:cmt_index].lstrip()
                ff_line = self.empty
            add_space = len(code_line) - len(code_line.rstrip()) # Keep original spacing
            cmnt_line = self.space * add_space + line[cmt_index:]
            code_line = code_line.rstrip()
        elif cmt_index == 0:
            while(line[-2] == self.space):
                line = line[:-2] + line[-1:]
            if self.comment_behavior in [self.as_is, self.first_col]:
                new_file_lines.append(line)
                continue
            else:
                cmnt_line = line
                code_line = self.empty
                ff_line = self.empty
        else:
            if not self.free_form:
                code_line = line[self.ff_column_len:].lstrip()
                ff_line = line[:self.ff_column_len]
            else:
                code_line = line.lstrip()
                ff_line = self.empty
            cmnt_line = self.empty

        # Remove empty whitespace at the end of a comment-only line
        if not code_line:
            code_line = ff_line + code_line + cmnt_line
            while(len(code_line) > 1 and code_line[-2] == self.space):
                code_line = code_line[:-2] + code_line[-1:]
            if self.comment_behavior in [self.as_is, self.first_col]:
                new_file_lines.append(code_line)
                continue

        temp = self.empty
        single_quote_skip = False  # Skip strings
        double_quote_skip = False  # Skip strings
        comment_skip = False  # Skip comment
        # print(code_line)

        for j, char in enumerate(code_line):
            # String check
            if char == "'" and not double_quote_skip:
                single_quote_skip = not single_quote_skip
            if char == '"' and not single_quote_skip:
                double_quote_skip = not double_quote_skip
            if char == self.comment:
                comment_skip = True
            if not single_quote_skip and not double_quote_skip and not comment_skip:
                if self.lowercasing: # User defined; default is true
                    char = char.lower() # Lowercase all working code; no global CAPS at this time
                if char == self.space:
                    temp = self.remove_extra_space(self, j, char, code_line, temp)
                elif char == ".":
                    temp = self.period_spacing(self, j, char, code_line, temp)
                elif char == ",":
                    temp = self.comma_spacing(self, j, char, code_line, temp)
                elif char == ":":
                    temp = self.colon_spacing(self, j, char, code_line, temp)
                elif char in ["(", ")", "[","]"]:
                    temp = self.paren_spacing(self, j, char, code_line, temp)
                elif char in ["/"]:
                    temp, first_slash = self.slash_spacing(self, j, char, code_line, temp, first_slash)
                elif char in ["<", ">", "="]:
                    temp = self.relational_op_spacing(self, j, char, code_line, temp)
                elif char == "*" and "*" not in [code_line[j - 1], code_line[j + 1]] and code_line[j - 4 : j] not in self.data_types:
                    temp = self.star_spacing(self, j, char, code_line, temp)
                elif char in ["+", "-"]:
                    temp = self.plus_spacing(self, j, char, code_line, temp)
                else:
                    temp += char
            else:
                temp += char

        temp, indenter, skip, first_case, select_indent = self.structured_indent(self, temp, indenter, skip, first_case,i, ff_line, do_list, do_count, select_indent)
        if not comment_skip: # User defined; default is true
            temp1, temp2 = self.line_carry_over(self, ff_line, temp, cmnt_line)
            temp = temp1 + temp2
        new_file_lines.append(temp)
        if not self.free_form: # Change the F77 comment back to whatever it was to begin with
            self.comment = old_comment
    self.file_lines = new_file_lines
    return
