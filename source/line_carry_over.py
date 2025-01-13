# ========================================================================
# Function: line_carry_over
# ========================================================================
# Purpose:
# The purpose of this is to carry over lines that might have been
# formatted past the last usable column
# ========================================================================
def line_carry_over(self, ff_line, temp_line, cmnt_line):
    single_quote_skip = False  # Skip strings
    double_quote_skip = False  # Skip strings
    line_cont = False
    com_loc = 0
    # The whole point of this is to look for a string and cutoff
    for i, char in enumerate(temp_line):
        if not single_quote_skip and not double_quote_skip:
            com_loc = i
        # String check
        if i > self.last_col - len(ff_line) - 1:
            line_cont = True
            # print(repr(temp_line[j]), j+6 - len(ff_line) - 1, self.last_col - len(ff_line) - 1, single_quote_skip, repr(temp_line))
            break  # We know we have to bump over to the next, so no need to be in here anymore
        if i + 1 < len(temp_line) and temp_line[i+1] != self.newline:
            if char == "'" and not double_quote_skip:
                single_quote_skip = not single_quote_skip
            if char == '"' and not single_quote_skip:
                double_quote_skip = not double_quote_skip
    if line_cont:  # then we need to find a good place to stop this line
        print(com_loc, ff_line +temp_line)
        if com_loc:
            j = com_loc
        else:
            j = self.last_col - len(ff_line) - 1
            # Look for the first space, and call it there
            if temp_line[j] != self.space:
                while temp_line[j] != self.space:
                    j -= 1
                j += 1 #Add one back


        if self.free_form:
            if temp_line[j + 1] == self.continuation_char:
                line1 = temp_line[:j] + self.continuation_char
                if cmnt_line:
                    line1 += self.space + cmnt_line
                line2 = self.empty
            else:
                line1 = temp_line[:j] + self.continuation_char
                if cmnt_line:
                    line1 += self.space + cmnt_line
                else:
                    line1 += self.newline
                indent = len(line1) - len(line1.lstrip())
                line2 = self.space * indent + temp_line[j:].rstrip() + self.newline
        else:
            indent = len(temp_line[:j]) - len(temp_line[:j].lstrip())
            if single_quote_skip or double_quote_skip:
                quote2 = '// '
                line1 = ff_line + temp_line[:j] + cmnt_line
                quote_skip = False
                if single_quote_skip:
                    quote = "'"
                    for j, char in enumerate(temp_line[:j]):
                        if char == "'":
                            quote_skip = not quote_skip
                else:
                    quote = '"'
                    for j, char in enumerate(temp_line[:j]):
                        if char == '"':
                            quote_skip = not quote_skip
                if quote_skip:
                    line1 = ff_line + temp_line[:j] + quote + cmnt_line
                    line2 = self.space * 5 + self.continuation_char + self.space * indent + quote2 + quote + temp_line[j:]
                else:
                    line1 = ff_line + temp_line[:j].rstrip() + cmnt_line
                    # if 
                    line2 = self.space * 5 + self.continuation_char + self.space * indent + temp_line[j:].lstrip()
            else:
                # print(ff_line + temp_line[:j])
                line1 = ff_line + temp_line[:j].rstrip() + cmnt_line
                line2 = self.space * 5 + self.continuation_char + self.space * indent + temp_line[j:].lstrip()

        if line1[-1] != self.newline:
            line1 += self.newline
        if line2 and line2[-1] != self.newline:
            line2 += self.newline
        # print(line2)

        return line1, line2
    else:
        line1 = ff_line + temp_line + cmnt_line
        return line1, ""
