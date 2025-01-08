# ========================================================================
# Function: structured_indent
# ========================================================================
# Purpose:
# This will properly nest and indent code largely based on the keyword
# lists found in keywords_increase and keywords_decrease
# ========================================================================
def structured_indent(self, temp_line, indenter, skip, first_case,i):
    j = i
    if ": do" in temp_line and not temp_line[temp_line.find(": do") - 1] == ":":
        indenter += 1
        skip = True
    elif any(temp_line.startswith(keyword) for keyword in self.keywords_increase) or any(temp_line.startswith(item + " function ") for item in self.data_types):
        if temp_line.startswith('if'):
            # print(temp_line)
            if temp_line[-5:].strip() == 'then':
                indenter += 1
                skip = True
            elif temp_line[-2].strip() == self.continuation_char:
                if self.file_lines[j+1][-2].strip() == self.continuation_char:
                    while self.file_lines[j+1][-2].strip() == self.continuation_char:
                        if temp_line[-5:].strip() == 'then':
                            indenter += 1
                            skip = True
                        else:
                            j += 1
                else:
                    if self.file_lines[j+1][-5:].strip() == 'then':
                        indenter += 1
                        skip = True
        else:
            # if temp_line.startswith('type'):
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
        if temp_line.strip()[-1] == self.continuation_char:
            skip = True
        else:
            skip = False
    else:
        temp_line = self.space * self.tab_len * indenter + temp_line

    return temp_line, indenter, skip, first_case
