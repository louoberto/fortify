# ========================================================================
# Function: line_carry_over
# ========================================================================
# Purpose:
# The purpose of this is to carry over lines that might have been
# formatted past the last usable column
# ========================================================================
from no_format import no_format


def line_carry_over(self, ff_line, code_line, cmnt_line):
    quote_skip = False  # Skip strings
    lineCont = False
    comloc = 0
    # The whole point of this is to look for a string
    for j, char in enumerate(code_line):
        # String check
        if char == """ or char == """:
            quote_skip = not quote_skip
            comloc = j
        if j > (self.last_col - len(ff_line)):
            lineCont = True
            break  # We know we have to bump over to the next, so no need to be in here anymore
    if lineCont:  # then we need to find a good place to stop this line
        # Let's find the first, last space and call it there...
        if quote_skip:  # unless it was a comment that went overboard, then we need that to go over
            j = comloc
        else:
            j = self.last_col
            if self.free_form:
                j -= 1
        if code_line[j] == self.space or quote_skip:
            if self.free_form:
                line1 = ff_line + code_line[:j] + self.continuation_char + self.space + cmnt_line
                line2 = code_line[j:]
            else:
                line1 = ff_line + code_line[:j] + cmnt_line
                line2 = ff_line[-1] + self.continuation_char + code_line[j:]
        else:
            while code_line[j] != self.space:
                j = j - 1
            if self.free_form:
                if not cmnt_line:
                    line1 = ff_line + code_line[:j] + self.continuation_char + "\n"
                else:
                    line1 = (
                        ff_line
                        + code_line[:j]
                        + self.continuation_char
                        + self.space
                        + cmnt_line
                    )
                line2 = code_line[j:]
            else:
                if not cmnt_line:
                    line1 = ff_line + code_line[:j] + "\n"
                else:
                    line1 = ff_line + code_line[:j] + cmnt_line
                line2 = ff_line[-1] + self.continuation_char + code_line[j:]
        return line1, line2
    else:
        line1 = ff_line + code_line + cmnt_line
        return line1, ""
