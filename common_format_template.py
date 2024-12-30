# ========================================================================
# Function: comma_colon_spacing
# ========================================================================
# Purpose:
# Will format 
# ========================================================================
from no_format import no_format


def common_format_template(self):
    new_file_lines = []
    for line in self.file_lines:
        # Skip blank lines
        if not line.strip():
            new_file_lines.append(line)
            continue
        elif "\t" in line:
            line = line.replace("\t", self.space * self.tab)

        # Skip formatting if any of the following conditions are met
        #   1. If there is a comment in the first column
        #   2. FORMAT statement is in the line.
        #   3. There is a "do not fortify" in the line.
        #   4. Preprocessor directive
        cmt_index = line.find("!")
        if cmt_index == 0 or "format" in line[:cmt_index] or no_format(line) or "#" in line.strip()[0]:
            new_file_lines.append(line)
            continue
        elif cmt_index > 0:
            code_line = line[:cmt_index].lstrip()
            cmnt_line = line[cmt_index:]
        else:
            code_line = line.lstrip()
            cmnt_line = ""

        if not self.free_form:
            ff_line = code_line[: self.ff_column_len]
            code_line = code_line[self.ff_column_len :]
        else:
            ff_line = ""

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
                if char == self.space and code_line[j - 1] == self.space: # Remove double spaces
                    continue
                else:
                    char = char.lower() # Lowercase all working code; no global CAPS at this time

                if char == ".":
                    temp = self.if_logicals_spacing(self, j, char, code_line, temp)
                elif char in [")", self.space]:
                    temp = self.paren_spacing(self, j, char, code_line, temp)
                elif char in ["<", ">", "/", "="]:
                    temp = self.relational_op_spacing(self, j, char, code_line, temp)
                elif char == "*" and code_line[j - 1] != "*" and code_line[j + 1] != "*" and not any(code_line[j - 4 : j] in x for x in self.data_types):
                    temp = self.star_spacing(self, j, char, code_line, temp)
                elif char in ["+", "-"]:
                    temp = self.plus_spacing(self, j, char, code_line, temp)
                    temp = self.minus_spacing(self, j, char, code_line, temp)
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
        new_file_lines.append(ff_line + temp + cmnt_line)
    self.file_lines = new_file_lines
    return
