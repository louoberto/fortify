# ========================================================================
# Function: structured_indent
# ========================================================================
# Purpose:
# This will properly nest and indent code largely based on the keyword
# lists found in keywords_increase and keywords_decrease
# ========================================================================
import re
def structured_indent(self, temp_line, indenter, skip, first_case,i, ff_line,do_list,do_count):
    j = i
    if any(temp_line.lower().startswith(keyword) for keyword in self.keywords_increase) or \
         any(temp_line.lower().startswith(item + " function ") or \
         any(temp_line.lower().startswith(f"{item}({x}) function") or \
             temp_line.lower().startswith(f"{item}*{x} function") for x in [1, 2, 4, 8, 16]) for item in self.data_types) or\
         any(re.search(r"^[a-z0-9_]+:\s*"  + re.escape(keyword) + r"\b", temp_line.lower()) for keyword in self.keywords_increase):
        if temp_line.lower().startswith('if'):
            if temp_line.lower()[-5:].strip() == 'then':
                indenter += 1
                skip = True
            elif temp_line.lower()[-2].strip() == self.continuation_char:
                if self.file_lines[j+1][-2].strip() == self.continuation_char:
                    while self.file_lines[j+1][-2].strip() == self.continuation_char:
                        j += 1
                    if self.file_lines[j+1][-5:].strip() == 'then':
                            indenter += 1
                            skip = True
                else:
                    if self.file_lines[j+1][-5:].strip() == 'then':
                        indenter += 1
                        skip = True
        elif temp_line.lower().startswith('do ') or temp_line.lower().strip() == 'do':
            indenter += 1
            skip = True
            if not self.free_form:
                # Need to check if there is a continue with it
                i = len('do')
                while temp_line.lower()[i] == self.space:
                    i += 1
                if temp_line.lower()[i].isnumeric():
                    temp_num = self.empty
                    while temp_line.lower()[i].isnumeric():
                        temp_num += temp_line[i]
                        i += 1
                    if any(temp_num == item[0] for item in do_list):
                        for index, item in enumerate(do_list):
                            if temp_num == item[0]:
                                do_list[index] = (item[0], item[1] + 1)
                                break
                    else:
                        do_list.append((temp_num, do_count))
        elif not temp_line.lower().replace(self.space, self.empty).startswith('type(') and not temp_line.lower().startswith('do'):
            if temp_line.lower().startswith('type is'):
                if not first_case:
                    first_case = True
                    indenter += 1
                skip = True
            else:
                indenter += 1
                skip = True
    elif temp_line.lower().startswith("case"):
        if not first_case:
            first_case = True
            indenter += 1
        skip = True
    elif any(temp_line.lower().startswith(keyword) for keyword in self.keywords_decrease) or any(temp_line.lower() == keyword[:-1] for keyword in self.keywords_decrease):
        if temp_line.lower().startswith("endselect") or temp_line.lower().startswith("end select"):
            first_case = False
            indenter -= 2
        elif temp_line.lower().startswith("continue"):
            for goto in do_list:
                if ff_line.lstrip().startswith(goto[0]):
                    indenter -= (1 + goto[1])
                    do_list.remove(goto)
                    break
        else:
            indenter -= 1

    if ("else" in temp_line.lower()[:4] or "elseif" in temp_line.lower()[:6] or "elsewhere" in temp_line.lower()[:6]):  # else statements go back one, but that's it
        skip = True

    if skip:
        temp_line = self.space * self.tab_len * (indenter - 1) + temp_line
        # print(temp_line)
        if self.free_form:
            if temp_line.strip()[-1] == self.continuation_char:
                skip = True
            else:
                skip = False
        else:
            if len(self.file_lines) > j + 1 and len(self.file_lines[j + 1]) > 5 and self.file_lines[j + 1][5] != self.space and not self.file_lines[j + 1][0].isalpha() and self.file_lines[j + 1][0] not in ['*', self.comment]:
                skip = True
            else:
                skip = False
    else:
        temp_line = self.space * self.tab_len * indenter + temp_line

    return temp_line, indenter, skip, first_case
