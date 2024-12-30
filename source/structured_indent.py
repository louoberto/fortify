# ========================================================================
# Function: structured_indent
# ========================================================================
# Purpose:
# This will properly nest and indent code largely based on the keyword
# lists found in keywords_increase and keywords_decrease
# ========================================================================
def structured_indent(self, code_line, indenter, skip, first_case):
    if ": do" in code_line and not code_line[code_line.find(": do") - 1] == ":":
        # templyne = code_line.replace(' : do', ': do', 1)
        # code_line = templyne
        indenter += 1
        skip = True
    elif any(code_line.startswith(keyword + self.space) for keyword in self.keywords_increase) or any(code_line.startswith(item + " function ") for item in self.data_types):
        indenter += 1
        skip = True
    elif code_line.startswith("case"):
        if not first_case:
            first_case = True
            indenter += 1
            skip = True
    elif code_line.startswith("endselect") or code_line.startswith("end select"):
        indenter -= 2
    elif any(code_line.startswith(keyword) for keyword in self.keywords_decrease):
        indenter -= 1

    if ("else" in code_line[:4] or "elseif" in code_line[:6] or "elsewhere" in code_line[:6]):  # else statements go back one, but that's it
        skip = True

    if skip:
        code_line = self.space * self.tab_len * (indenter - 1) + code_line
        skip = False
    else:
        code_line = self.space * self.tab_len * indenter + code_line

    return code_line, indenter, skip, first_case
