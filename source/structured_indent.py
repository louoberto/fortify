# ========================================================================
# Function: structured_indent
# ========================================================================
# Purpose:
# This will properly nest and indent code largely based on the keyword
# lists found in keywords_increase and keywords_decrease
# ========================================================================
import sys
def structured_indent(self, code_line, indenter, skip, first_case):
    if "ctemp .eq. " in code_line.strip():
        print(indenter)
    if ": do" in code_line and not code_line[code_line.find(": do") - 1] == ":":
        indenter += 1
        skip = True
    elif any(code_line.startswith(keyword) for keyword in self.keywords_increase) or any(code_line.startswith(item + " function ") for item in self.data_types):
        if code_line.startswith('if'):
            if code_line[-5:].strip() == 'then':
                indenter += 1
                skip = True
            if "ctemp .eq. " in code_line.strip():
                print(code_line[-5:].strip())         
        else:
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
        # if indenter == 0:
        #     print(code_line, indenter, skip)
    if "ctemp .eq. " in code_line.strip():
        print(indenter)
        #sys.exit(0)
    if ("else" in code_line[:4] or "elseif" in code_line[:6] or "elsewhere" in code_line[:6]):  # else statements go back one, but that's it
        skip = True

    if skip:
        code_line = self.space * self.tab_len * (indenter - 1) + code_line
        skip = False
        # print(code_line, indenter, skip)
    else:
        # print(code_line, indenter, skip)
        code_line = self.space * self.tab_len * indenter + code_line

    return code_line, indenter, skip, first_case
