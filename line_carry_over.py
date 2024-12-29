# ========================================================================
# Function: miuns_spacing
# ========================================================================
# Purpose:
# Will format  I believe this handles = - 0.213 to = -0.213 for example
# ========================================================================
from no_format import no_format


def line_carry_over(self):
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
            ff_line = code_line[:self.ff_column_len]
            code_line = code_line[self.ff_column_len:]
        else:
            ff_line = ""

        quote_skip = False # Skip strings
        lineCont = False
        comloc = 0
        # The whole point of this is to look for a string
        for j, char in enumerate(code_line):
            # String check
            if char == "'" or char == '"':
                quote_skip = not quote_skip
                comloc = j
            if j > (self.last_col-len(ff_line)):
                lineCont = True
                break  # We know we have to bump over to the next, so no need to be in here anymore
        if lineCont:  # then we need to find a good place to stop this line...
            # Let's find the first, last space and call it there...
            if quote_skip:  # unless it was a comment that went overboard, then we need that to go over
                j = comloc
            else:
                j = self.last_col
                if self.free_form:
                    j -= 1
            if code_line[j] == " " or quote_skip:
                if self.free_form:
                    line1 = ff_line + code_line[:j] + "& " + cmnt_line
                    line2 = code_line[j:]
                else:
                    line1 = ff_line + code_line[:j] + cmnt_line
                    line2 = ff_line[-1] + "&" + code_line[j:]
            else:
                while code_line[j] != " ":
                    j = j - 1
                if self.free_form:
                    if not cmnt_line:
                        line1 = ff_line + code_line[:j] + "&\n"
                    else:
                        line1 = ff_line + code_line[:j] + "& " + cmnt_line
                    line2 = code_line[j:]
                else:
                    if not cmnt_line:
                        line1 = ff_line + code_line[:j] + "\n"
                    else:
                        line1 = ff_line + code_line[:j] + cmnt_line
                    line2 = ff_line[-1] + "&" + code_line[j:]
            new_file_lines.append(line1)
            new_file_lines.append(line2)
        else:
            new_file_lines.append(line)
    self.file_lines = new_file_lines
    return
