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
    lineCont = False
    comloc = 0
    # The whole point of this is to look for a string
    for j, char in enumerate(temp_line):
        if not single_quote_skip and not double_quote_skip:
            comloc = j
        if j > self.last_col - len(ff_line) - 1:
            lineCont = True
            break  # We know we have to bump over to the next, so no need to be in here anymore
        # String check
        if char == "'" and not double_quote_skip:
            single_quote_skip = not single_quote_skip
        if char == '"' and not single_quote_skip:
            double_quote_skip = not double_quote_skip
    if lineCont:  # then we need to find a good place to stop this line
        # Let's find the first, last space and call it there...
        if single_quote_skip or double_quote_skip:  # unless it was a comment that went overboard, then we need that to go over
            j = comloc
        else:
            j = self.last_col - len(ff_line)
            if temp_line[j] != self.newline:
                j -= 1

        if temp_line[j] != self.space:
            while temp_line[j] != self.space:
                j -= 1
        
        if self.free_form:
            if temp_line[j+1] == self.continuation_char:
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
                line2 = self.space * indent + temp_line[j:].strip() + self.newline
        else:
            line1 = ff_line + temp_line[:j].rstrip() + cmnt_line
            indent = len(temp_line[:j]) - len(temp_line[:j].lstrip())
            line2 = ff_line[:-1] + self.continuation_char + self.space * indent + temp_line[j:].strip() + self.newline
            # print(line2)

        if line1[-1] != self.newline:
            line1 += self.newline
        if line2 and line2[-1] != self.newline:
            line2 += self.newline

        return line1, line2
    else:
        line1 = ff_line + temp_line + cmnt_line
        return line1, ""
