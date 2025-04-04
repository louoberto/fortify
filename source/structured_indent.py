# ========================================================================
# Function: structured_indent
# ========================================================================
# Purpose:
# This will properly nest and indent code largely based on the keyword
# lists found in keywords_increase and keywords_decrease
# ========================================================================
import re
def structured_indent(self, temp_line, indenter, skip, first_case, i, ff_line, do_list, do_count, select_indent):
    j = i
    # print(temp_line)
    temp_lower = temp_line.lower()
    if (any(temp_lower.startswith(item + " function ") \
        or re.search(rf"{item}\(\w+\) function", temp_line, re.IGNORECASE) \
        or re.search(rf"{item}\*\w+ function", temp_line, re.IGNORECASE) for item in self.data_types) \
        or any(temp_lower.startswith(keyword) \
        or re.match(r"^[a-z0-9_]+:\s*" + re.escape(keyword) + r'(?=\s|\(|$)', temp_lower) \
        or re.match(r'^\s*\d{0,5}\s*' + re.escape(keyword) + r'(?=\s|\(|$)', temp_lower) \
        or re.match(r"^[a-z0-9_]+:" + re.escape(keyword) + r'(?=\s|\(|$)', temp_lower) for keyword in self.keywords_increase) \
        and ('module procedure' not in temp_lower) and ('interface_' not in temp_lower)):
        if temp_lower.startswith('select'):
            select_indent = True
        if temp_lower.strip().startswith('module procedure'):
            # print(indenter, repr(temp_line))
            skip = True
            pass
        # print(indenter, repr(temp_line))
        if temp_lower.lstrip().startswith('type ') and not select_indent:
            # print(indenter, repr(temp_lower))
            # look ahead for 'end type'
            is_type_block = False
            for k in range(j + 1, len(self.file_lines)):
                if self.file_lines[k].lower().strip().startswith('endtype') or self.file_lines[k].lower().strip().startswith('end type'):
                    is_type_block = True
                    break
                else:
                    is_type_block = False
            if is_type_block:
                # print(indenter, repr(temp_lower))
                indenter += 1
                skip = True
            # else:
                # print(indenter, repr(temp_lower))
        elif temp_lower.startswith('if') or re.match(r"^\s*[a-z0-9_]+ if ", temp_lower) or re.match(r"^\s*[a-z0-9_]+ if" + r'(?=\s|\()', temp_lower):
            # print(temp_line)
            if temp_lower[-5:].strip() == 'then' or (") then;" in temp_lower and not any(keyword in temp_lower for keyword in ['end if', 'endif'])):
                # print(temp_line)
                indenter += 1
                skip = True
            elif temp_lower[-2].strip() == self.continuation_char or (not self.free_form and len(self.file_lines[j+1]) > 6 and self.file_lines[j+1][5] != self.space):
                # print(temp_line)
                if self.file_lines[j+1][-2].strip() == self.continuation_char or not self.free_form:
                    # print(temp_line)
                    if self.free_form:
                        while self.file_lines[j+1][-2].strip() == self.continuation_char:
                            j += 1
                    else:
                        while self.file_lines[j+2][5] != self.space:
                            j += 1
                        # will need to come back here possibly in case the if statement goes over and over
                    if self.file_lines[j+1][-5:].strip().lower() == 'then':
                        # print(temp_line)
                        indenter += 1
                        skip = True
                else:
                    # print(repr(self.file_lines[j+1][-5:].strip()))
                    if self.file_lines[j+1][-5:].strip().lower() == 'then':
                        # print(temp_line)
                        indenter += 1
                        skip = True

        elif temp_lower.startswith('do ') or temp_lower.strip() == 'do' or re.search(r"^[a-z0-9_]+: *do(?=\n| )", temp_lower):
            indenter += 1
            skip = True
            # print(temp_line)
            # Check if there is a continue with it
            i = len('do')
            while temp_lower[i] == self.space:
                i += 1
            if temp_lower[i].isnumeric():
                # print(temp_lower[i])
                temp_num = self.empty
                while temp_lower[i].isnumeric():
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
        elif not temp_lower.replace(self.space, self.empty).startswith('type(') and not temp_lower.startswith('do'):
            if temp_lower.startswith('type is') or temp_lower.startswith('class is') or temp_lower.startswith('class default'):
                # print(temp_line)
                if select_indent:
                    if not first_case:
                        first_case = True
                        indenter += 1
                    skip = True
            else:
                # print(temp_line, not (temp_lower.startswith('type ') and len(temp_line) > j + 1 and temp_line[j+1].isalpha() and temp_line[j+1] in ['('] and not select_indent))
                if not (temp_lower.startswith('type *') and not select_indent):
                    indenter += 1
                    skip = True
        # print(temp_line)
        # indenter += 1
        # skip = True
    elif temp_lower.startswith("case"):
        if not first_case:
            first_case = True
            indenter += 1
        skip = True
    elif any(temp_lower.startswith(keyword) for keyword in self.keywords_decrease)\
      or any(temp_lower == keyword[:-1] for keyword in self.keywords_decrease)\
      or any(re.match(r'^\s*\d{0,5}\s*' + re.escape(keyword) + r'(?=\s|\(|$)', temp_lower) for keyword in self.keywords_decrease):
        # print(indenter, repr(temp_line))
        if temp_lower.startswith("end =") or re.match(r'^\s*\d{0,5}\s+end =', temp_lower):
            pass
        else:
            # print(indenter, repr(temp_line))
            if temp_lower.startswith("endselect") or temp_lower.startswith("end select"):
                select_indent = False
                first_case = False
                indenter -= 2
            elif (temp_line.strip() == 'continue') or (temp_lower.startswith("continue") and not self.free_form) or (re.match(r'^\s*\d{0,4}\s+continue\s*\S*(\s|$)', temp_line, re.IGNORECASE) and self.free_form):
                    # print(temp_line)
                    for goto in do_list:
                        if ff_line.lstrip().startswith(goto[0]) or temp_line.startswith(goto[0]):
                            indenter -= (1 + goto[1])
                            do_list.remove(goto)
                            break
            # elif self.file_lines[j-1].strip().lower().startswith('if') or (re.search(r"^\s*[a-z0-9_]+ if", self.file_lines[j-1].lower()) and not any(keyword in self.file_lines[j-1] for keyword in ['end if', 'endif'])):
            #     # print(indenter, repr(self.file_lines[j-1]))
            #     pass
            else:
                indenter -= 1
                # print(self.file_lines[j-1].lower(), indenter, repr(temp_line))
    elif re.match(r'^\s*\d{0,4}\s+continue(\s|$)', temp_line, re.IGNORECASE) and self.free_form:
        # print(temp_line, do_list)
        for goto in do_list:
            # print(goto[0])
            if temp_line.startswith(goto[0]):
                indenter -= (1 + goto[1])
                do_list.remove(goto)
                break

    if ("else" in temp_lower[:4] or "elseif" in temp_lower[:6] or "elsewhere" in temp_lower[:6]):  # else statements go back one, but that's it
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

    if indenter < 0:
        indenter = 0
    # print(indenter, repr(temp_line))
    return temp_line, indenter, skip, first_case, select_indent
