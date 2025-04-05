# ========================================================================
# Function: structured_indent
# ========================================================================
# Purpose:
# This will properly nest and indent code largely based on the keyword
# lists found in keywords_increase and keywords_decrease
# ========================================================================
import re
def structured_indent(self, temp_line, indenter, skip, first_case, i, ff_line, do_list, do_count, select_indent, selecter):
    j = i
    # print(temp_line)
    temp_lower = temp_line.lower()
    keyword_match = False
    keyword_dec_match = False
    for keyword in self.data_types:
        if (temp_lower.startswith(keyword + " function ") \
            or re.search(rf"{keyword}\(\w+\) function", temp_line, re.IGNORECASE) \
            or re.search(rf"{keyword}\*\w+ function", temp_line, re.IGNORECASE)):
            keyword_match = True
            break
    # if keyword_match:
    #     print(temp_line, keyword_match)

    if not keyword_match:
        for keyword in self.keywords_increase:
            if ((temp_lower.startswith(keyword) \
                or re.match(r"^[a-z0-9_]+:\s*" + re.escape(keyword) + r'(?=\s|\(|$)', temp_lower) \
                or re.match(r'^\s*\d{0,5}\s*' + re.escape(keyword) + r'(?=\s|\(|$)', temp_lower) \
                or re.match(r"^[a-z0-9_]+:" + re.escape(keyword) + r'(?=\s|\(|$)', temp_lower)) \
                and ('module procedure' not in temp_lower) and ('interface_' not in temp_lower)):
                keyword_match = True
                break
        # print(temp_line, keyword_match)
    
    if not keyword_match:
        for keyword in self.keywords_decrease:
            if temp_lower.startswith(keyword) or temp_lower == keyword[:-1] \
                or re.match(r'^\s*\d{0,5}\s*' + re.escape(keyword) + r'(?=\s|\(|$)', temp_lower):
                keyword_dec_match = True
                break
        # print(temp_line, keyword_dec_match)

    if keyword_match:
        # print(keyword, indenter, repr(temp_line))
        if keyword == 'select':
            if select_indent:
                selecter += 1
                indenter += 1
            select_indent = True
        if keyword == 'type ' and not select_indent and not temp_lower.startswith('type ('):
            # print(indenter, repr(temp_lower))
            # =======================================================
            # Look ahead for 'end type'
            # =======================================================
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
        elif keyword == 'if':
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
                        while len(self.file_lines[j+2]) > 5 and self.file_lines[j+2][5] != self.space:
                            j += 1
                        # will need to come back here possibly in case the if statement goes over and over
                    if self.file_lines[j+1][-5:].strip().lower() == 'then':
                        # print(temp_line)
                        indenter += 1
                        skip = True
                elif self.file_lines[j+1][-5:].strip().lower() == 'then':
                    # print(temp_line)
                    indenter += 1
                    skip = True
        elif keyword == 'do' and re.match(r"^(do\b|[a-z0-9_]+:\s*do\b)", temp_lower.strip()):
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
            # print(temp_line)
            if keyword + 'is' == 'type is' or keyword in ['class is', 'class default']:
                # print(temp_line)
                if select_indent:
                    if not first_case:
                        first_case = True
                        indenter += 1
                    skip = True
            elif not (temp_lower.startswith('type *') and not select_indent):
                indenter += 1
                skip = True
    elif temp_lower.startswith("case"):
        if not first_case:
            first_case = True
            indenter += 1
        # print(select_indent, first_case, temp_lower)
        skip = True
    elif keyword_dec_match:
        # print(indenter, repr(temp_line))
        if temp_lower.startswith("end =") or re.match(r'^\s*\d{0,5}\s+end =', temp_lower):
            pass
        else:
            # print(indenter, repr(temp_line))
            if temp_lower.startswith("endselect") or temp_lower.startswith("end select"):
                select_indent = False
                first_case = False
                indenter -= 2
                if selecter > 0:
                    selecter -= 1
            elif (temp_line.strip() == 'continue') or (temp_lower.startswith("continue") and not self.free_form) or (re.match(r'^\s*\d{0,4}\s+continue\s*\S*(\s|$)', temp_line, re.IGNORECASE) and self.free_form):
                    # print(temp_line)
                    for goto in do_list:
                        if ff_line.lstrip().startswith(goto[0]) or temp_line.startswith(goto[0]):
                            indenter -= (1 + goto[1])
                            do_list.remove(goto)
                            break
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
        if keyword == 'select':
            temp_line = self.space * self.tab_len * (indenter - 1 - selecter) + temp_line
        else:
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
    return temp_line, indenter, skip, first_case, select_indent, selecter
