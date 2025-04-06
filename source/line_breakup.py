# ========================================================================
# Function: line_breakup
# ========================================================================
# Purpose:
# Breaks up the given line into the fixed format, code line, and comment
# line sections for later processing.
# ========================================================================
def line_breakup(self, line):
    cmt_index = line.find(self.comment)
    if cmt_index >= 0:
        # print(repr(line))
        if cmt_index > 0:
            # print(cmt_index, line)
            single_quote_skip = False  # Skip strings
            double_quote_skip = False  # Skip strings
            j = 0
            while j < len(line):
                char = line[j]
                # String check
                if char == "'" and not double_quote_skip:
                    single_quote_skip = not single_quote_skip
                if char == '"' and not single_quote_skip:
                    double_quote_skip = not double_quote_skip
                if not single_quote_skip and not double_quote_skip:
                    if char == self.comment or cmt_index < j:
                        if j > cmt_index:
                            cmt_index = line[j:].find(self.comment)
                            # print(cmt_index, line[j:], j)
                        else:
                            # print(cmt_index)
                            break
                j += 1

            if not self.free_form:
                code_line = line[self.ff_column_len:cmt_index].lstrip()
                ff_line = line[:self.ff_column_len]
                # print(repr(line))
            else:
                code_line = line[:cmt_index].lstrip()
                # print(repr(line))
                ff_line = self.empty
            add_space = len(code_line) - len(code_line.rstrip()) # Keep original spacing
            cmnt_line = self.space * add_space + line[cmt_index:]
            code_line = code_line.rstrip()
            # print(repr(cmnt_line))
        elif cmt_index == 0:
            while len(line) > 2 and line[-2] == self.space:
                line = line[:-2] + line[-1:]
            if self.comment_behavior in [self.as_is, self.first_col]:
                return ff_line, code_line, cmnt_line, False
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
    return ff_line, code_line, cmnt_line, True