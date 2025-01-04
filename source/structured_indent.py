# ========================================================================
# Function: structured_indent
# ========================================================================
# Purpose:
# This will properly nest and indent code largely based on the keyword
# lists found in keywords_increase and keywords_decrease
# ========================================================================
def structured_indent(self, temp_line, indenter, skip, first_case):
    if ": do" in temp_line and not temp_line[temp_line.find(": do") - 1] == ":":
        indenter += 1
        skip = True
    elif any(temp_line.startswith(keyword) for keyword in self.keywords_increase) or any(temp_line.startswith(item + " function ") for item in self.data_types):
        if temp_line.startswith('if'):
            if temp_line[-5:].strip() == 'then':
                indenter += 1
                skip = True     
        else:
            indenter += 1
            skip = True
    elif temp_line.startswith("case"):
        if not first_case:
            first_case = True
            indenter += 1
            skip = True
    elif temp_line.startswith("endselect") or temp_line.startswith("end select"):
        indenter -= 2
    elif any(temp_line.startswith(keyword) for keyword in self.keywords_decrease):
        indenter -= 1
    if ("else" in temp_line[:4] or "elseif" in temp_line[:6] or "elsewhere" in temp_line[:6]):  # else statements go back one, but that's it
        skip = True

    if skip:
        temp_line = self.space * self.tab_len * (indenter - 1) + temp_line
        skip = False
    else:
        temp_line = self.space * self.tab_len * indenter + temp_line

    return temp_line, indenter, skip, first_case
