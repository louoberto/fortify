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
    new_file_lines = []
    for line in self.file_lines:
        # Skip formatting if any of the following conditions are met
        if not line.strip(): # If blank line
            new_file_lines.append(line)
            continue
        elif no_format(line): # Do no format in the line
            new_file_lines.append(line)
            continue
        elif line.strip()[0] == '#': # Preprocesser directive, leave line be
            new_file_lines.append(line)
            continue
        elif line[0] in ['*','C','c']: # Convert old-style comment chars to !
            line = "!" + line[1:]
            new_file_lines.append(line)
            continue

        cmt_index = line.find("!")
        if cmt_index == 0:
            new_file_lines.append(line)
            continue
        if "\t" in line: # Convert tab characters to spaces
            line = line.replace("\t", self.space * self.tab)
        if not self.free_form: # Standardize the line continuation character to & for fixed format
            if len(line) > 4 and (line[5] != self.space and line[5] != self.continuation_char):
                line = line[:5] + self.continuation_char + line[6:]
        if cmt_index > 0:
            if not self.free_form:
                code_line = line[self.ff_column_len:cmt_index].lstrip()
            else:
                code_line = line[:cmt_index].lstrip()
            add_space = len(code_line) - len(code_line.rstrip()) # Keep original spacing
            cmnt_line = self.space * add_space + line[cmt_index:]
        else:
            if not self.free_form:
                code_line = line[self.ff_column_len:].lstrip()
            else:
                code_line = line.lstrip()
            cmnt_line = ""

        ff_line = "" # Fixed format columns
        if not self.free_form:
            ff_line = line[:self.ff_column_len]
        if code_line:
            code_line = code_line.replace(self.space*2, '')
        else:
            new_file_lines.append(ff_line + code_line + cmnt_line)
            continue

        temp = ""
        single_quote_skip = False  # Skip strings
        double_quote_skip = False  # Skip strings
        for j, char in enumerate(code_line):
            # String check
            if char == "'":
                single_quote_skip = not single_quote_skip
            if char == '"':
                double_quote_skip = not double_quote_skip
            if not single_quote_skip and not double_quote_skip:
                char = char.lower() # Lowercase all working code; no global CAPS at this time
                if char == ".":
                    temp = self.if_logicals_spacing(self, j, char, code_line, temp)
                # elif char in [")", self.space]:
                #     temp = self.paren_spacing(self, j, char, code_line, temp)
                elif char in ["<", ">", "/", "="]:
                    temp = self.relational_op_spacing(self, j, char, code_line, temp)
                elif char == "*" and code_line[j - 1] != "*" and code_line[j + 1] != "*" and not code_line[j - 4 : j] in self.data_types:
                    temp = self.star_spacing(self, j, char, code_line, temp)
                elif char in ["+", "-"]:
                    temp = self.plus_spacing(self, j, char, code_line, temp)
                elif char in [",", ":"]:
                    temp = self.comma_colon_spacing(self, j, char, code_line, temp)
                else:
                    temp += char
            else:
                temp += char
        
        if "/ /" in temp:
            temp = temp.replace("/ /", "//") # Taking this into account
        if "= =" in temp:
            temp = temp.replace("= =", "==") # Taking this into account
        
        temp, indenter, skip, first_case = self.structured_indent(self, temp, indenter, skip, first_case)
        temp1, temp2 = self.line_carry_over(self, ff_line, temp, cmnt_line)
        temp = temp1 + temp2
        new_file_lines.append(temp)
    self.file_lines = new_file_lines
    return
