# ========================================================================
# Function: structured_indent
# ========================================================================
# Purpose:
# This will properly nest and indent code largely based on the keyword
# lists found in keywords_increase and keywords_decrease
# ========================================================================
import re
def structured_indent(self, temp_line, indenter, skip, first_case,i, ff_line,do_list, do_count, select_indent):
    j = i
    # print(temp_line)
    if any(temp_line.lower().startswith(keyword) for keyword in self.keywords_increase) or \
       any(temp_line.lower().startswith(item + " function ") or \
       any(temp_line.lower().startswith(f"{item}({x}) function") or \
           temp_line.lower().startswith(f"{item}*{x} function") for x in [1, 2, 4, 8, 16]) for item in self.data_types) or\
       any(re.match(r"^[a-z0-9_]+:\s*" + re.escape(keyword) + r'(?=\s|\(|$)', temp_line.lower()) for keyword in self.keywords_increase) or\
       any(re.match(r'^\s*\d{0,5}\s*' + re.escape(keyword) + r'(?=\s|\(|$)', temp_line.lower()) for keyword in self.keywords_increase) or \
       any(re.match(r"^[a-z0-9_]+:" + re.escape(keyword) + r'(?=\s|\(|$)', temp_line.lower()) for keyword in self.keywords_increase):
        if temp_line.lower().startswith('select'):
            select_indent = True
        # print(indenter, repr(temp_line))
        if temp_line.lower().startswith('if'):# or re.search(r"^\s*[a-z0-9_]+ if", temp_line.lower()):
            # print(temp_line)
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
        elif temp_line.lower().startswith('do ') or temp_line.lower().strip() == 'do' or re.search(r"^[a-z0-9_]+: *do(?=\n| )", temp_line.lower()):
            indenter += 1
            skip = True
            # print(temp_line)
            # Check if there is a continue with it
            i = len('do')
            while temp_line.lower()[i] == self.space:
                i += 1
            if temp_line.lower()[i].isnumeric():
                # print(temp_line.lower()[i])
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
                # print(do_list)
        elif not temp_line.lower().replace(self.space, self.empty).startswith('type(') and not temp_line.lower().startswith('do'):
            if temp_line.lower().startswith('type is'):
                if select_indent:
                    if not first_case:
                        first_case = True
                        indenter += 1
                    skip = True
            else:
                # print(temp_line, not (temp_line.lower().startswith('type ') and len(temp_line) > j + 1 and temp_line[j+1].isalpha() and temp_line[j+1] in ['('] and not select_indent))
                if not (temp_line.lower().startswith('type *') and not select_indent):
                    indenter += 1
                    skip = True
    elif temp_line.lower().startswith("case"):
        if not first_case:
            first_case = True
            indenter += 1
        skip = True
    elif any(temp_line.lower().startswith(keyword) for keyword in self.keywords_decrease)\
      or any(temp_line.lower() == keyword[:-1] for keyword in self.keywords_decrease)\
      or any(re.match(r'^\s*\d{0,5}\s*' + re.escape(keyword) + r'(?=\s|\(|$)', temp_line.lower()) for keyword in self.keywords_decrease):
        # print(indenter, repr(temp_line))
        if temp_line.lower().startswith("end =") or re.match(r'^\s*\d{0,5}\s+end =', temp_line.lower()):
            pass
        else:
            if temp_line.lower().startswith("endselect") or temp_line.lower().startswith("end select"):
                select_indent = False
                first_case = False
                indenter -= 2
            elif temp_line.lower().startswith("continue") and not self.free_form or re.match(r'^\s*\d{0,4}\s+continue(\s|$)', temp_line, re.IGNORECASE) and self.free_form:
                    # print(temp_line)
                    for goto in do_list:
                        if ff_line.lstrip().startswith(goto[0]) or temp_line.startswith(goto[0]):
                            indenter -= (1 + goto[1])
                            do_list.remove(goto)
                            break
            else:
                indenter -= 1
    elif re.match(r'^\s*\d{0,4}\s+continue(\s|$)', temp_line, re.IGNORECASE) and self.free_form:
        # print(temp_line, do_list)
        for goto in do_list:
            # print(goto[0])
            if temp_line.startswith(goto[0]):
                indenter -= (1 + goto[1])
                do_list.remove(goto)
                break

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
    # print(indenter, repr(temp_line))
    return temp_line, indenter, skip, first_case, select_indent
