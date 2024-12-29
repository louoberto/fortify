# ========================================================================
# Function: if_logicals_spacing
# ========================================================================
# Purpose:
# Adds spaces between logical expressions: x.gt.y => x .gt. y
# ========================================================================
from no_format import no_format
def if_logicals_spacing(self):

    new_file_lines = []
    skip = False
    skip_pass = 0
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
            ff_line = code_line[:self.ff_column_len-1]
            code_line = code_line[self.ff_column_len-1 :]
        else:
            ff_line = ""

        temp = ""
        single_quote_skip = False  # Skip strings
        double_quote_skip = False  # Skip strings
        for j, char in enumerate(code_line):
            if skip_pass == 0:
                if char == "!":
                    skip = True
                if skip:
                    temp += char
                else:
                    if char == "." and any(code_line[j : j + 5] in x for x in self.iftypes):
                        # try:
                        if code_line[j + 5]:
                            if code_line[j - 1] != self.space and code_line[j + 5] != self.space:
                                temp += self.space + code_line[j : j + 5] + self.space
                            elif code_line[j - 1] != self.space and code_line[j + 5] == self.space:
                                temp += self.space + code_line[j : j + 5]
                            elif code_line[j - 1] == self.space and code_line[j + 5] != self.space:
                                temp += code_line[j : j + 5]
                            else:
                                temp += code_line[j : j + 5]
                            skip_pass = 4
                        # except IndexError:
                        #     if code_line[j - 1] != self.space:
                        #         temp += self.space + code_line[j:]
                        #     else:
                        #         temp += code_line[j:]
                        #     skip_pass = 4
                        #     skip = True
                    elif char == "." and any(code_line[j : j + 4] in x for x in self.iftypes2):
                        # try:
                        if code_line[j + 4]:
                            if code_line[j - 1] != self.space and code_line[j + 4] != self.space and code_line[j + 4] != ".":
                                temp += self.space + code_line[j : j + 4] + self.space
                            elif code_line[j - 1] != self.space and code_line[j + 4] == self.space:
                                temp += self.space + code_line[j : j + 4]
                            elif code_line[j - 1] == self.space and code_line[j + 4] != self.space:
                                temp += code_line[j : j + 4] + self.space
                            else:
                                temp += code_line[j : j + 4]
                            skip_pass = 3
                        # except IndexError:
                        #     if code_line[j - 1] != self.space:
                        #         temp += self.space + code_line[j:]
                        #     else:
                        #         temp += code_line[j:]
                        #     skip_pass = 3
                    else:
                        temp += char
            else:
                skip_pass = skip_pass - 1
        line = temp

        new_file_lines.append(ff_line + temp + cmnt_line)
    self.file_lines = new_file_lines
    return
