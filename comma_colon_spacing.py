# ========================================================================
# Function: comma_colon_spacing
# ========================================================================
# Purpose:
# Will format 
# ========================================================================
from no_format import no_format


def comma_colon_spacing(self):
    new_file_lines = []
    for line in self.file_lines:
        # Skip blank lines
        if not line.strip():
            new_file_lines.append(line)
            continue

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
            code_line = line[:cmt_index]
            cmnt_line = line[cmt_index:]
        else:
            code_line = line
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
                if char == "," and code_line[j + 1] != self.space: # Comma case 1
                    temp += temp + char + self.space
                elif char == "," and code_line[j - 1] == self.space: # Comma case 2
                    temp = temp[:-1] + char
                elif char == ":" and code_line[j + 1] != ":" and code_line[j - 1] != ":": # Colon case 1
                    if code_line[j + 1] != self.space and code_line[j - 1] != self.space:  # a=b
                        temp += self.space + char + self.space
                    elif code_line[j + 1] != self.space and code_line[j - 1] == self.space:  # maybe a =b
                        temp += char + self.space
                    elif code_line[j + 1] == self.space and code_line[j - 1] != self.space:  # could be a= b
                        temp += self.space + char
                    else:  # could be a = b
                        temp += char
                elif char == ":" and code_line[j + 1] == ":" and code_line[j - 1] != ":": # Colon case 2
                    if code_line[j - 1] != self.space:  # a=b
                        temp += self.space + char
                    else:  # could be a = b
                        temp += char
                elif char == ":" and code_line[j + 1] != ":" and code_line[j - 1] == ":": # Colon case 3
                    if code_line[j + 1] != self.space:  # a=b
                        temp += char + self.space
                    else:  # could be a = b
                        temp += char
                else:
                    temp += char
            else:
                temp += char

        new_file_lines.append(ff_line + temp + cmnt_line)
    self.file_lines = new_file_lines
    return
