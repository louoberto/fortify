# ========================================================================
# Function: line_carry_over
# ========================================================================
# Purpose:
# The purpose of this is to carry over lines that might have been
# formatted past the last usable column
# ========================================================================
import sys
def line_carry_over(self, ff_line, temp_line, cmnt_line, indenter, skip):
    single_quote_skip = False  # Skip strings
    double_quote_skip = False  # Skip strings
    lineCont = False
    comloc = 0
    # The whole point of this is to look for a string
    for j, char in enumerate(temp_line):
        # String check
        if char == "'" and not double_quote_skip:
            single_quote_skip = not single_quote_skip
        if char == '"' and not single_quote_skip:
            double_quote_skip = not double_quote_skip
        if not single_quote_skip and not double_quote_skip:
            comloc = j
        if j > self.last_col - len(ff_line):
            lineCont = True
            break  # We know we have to bump over to the next, so no need to be in here anymore
    if lineCont:  # then we need to find a good place to stop this line
        # Let's find the first, last space and call it there...
        if single_quote_skip or double_quote_skip:  # unless it was a comment that went overboard, then we need that to go over
            j = comloc
        else:
            j = self.last_col
            if self.free_form and temp_line[j] != '/n':
                j -= 1

        if temp_line[j] != self.space:
            while temp_line[j] != self.space:
                j = j - 1
        
        if self.free_form:
            if temp_line[j+1] == self.continuation_char:
                line1 = temp_line[:j] + self.continuation_char
                if cmnt_line:
                    line1 += self.space + cmnt_line
                line2 = ''
            else:
                line1 = temp_line[:j] + self.continuation_char
                if cmnt_line:
                    line1 += self.space + cmnt_line
                else:
                    line1 += "\n"
                indent = len(line1) - len(line1.lstrip())
                line2 = self.space * indent + temp_line[j:].strip() + "\n"
        else:
            line1 = ff_line + temp_line[:j] + cmnt_line
            line2 = ff_line[-1] + self.continuation_char + temp_line[j:].strip()

        if line1[-1] != '\n':
            line1 += '\n'
        if line2 and line2[-1] != '\n':
            line2 += '\n'

        return line1, line2
    else:
        line1 = ff_line + temp_line + cmnt_line
        return line1, ""
