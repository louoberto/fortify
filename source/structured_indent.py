# =============================================================================
# Function: structured_indent
# =============================================================================
# Purpose:
# This will properly nest and indent code largely based on the keyword
# lists found in keywords_increase and keywords_decrease
# =============================================================================
import re
do_list = []
do_count = 0
def structured_indent(self, temp_line, current_line, ff_line):
    j = current_line
    # print(repr(temp_line))
    #==========================================================================
    # Specific case for select
    #==========================================================================
    if re.match(r'(?i)^\s*selectcase\b', temp_line.lower()):
        if self.lowercasing:
            temp_line = re.sub(r'(?i)\bselectcase\b', 'select case', temp_line)
            temp_lower = temp_line.lower()
        else:
            temp_lower = temp_line.lower()
            temp_lower = re.sub(r'(?i)\bselectcase\b', 'select case', temp_lower)
    else:
        temp_lower = temp_line.lower()
    #==========================================================================

    keyword_match = False
    keyword_dec_match = False
    keyword_data_types_match = False
    if temp_lower.strip()[0] != '!':
        #======================================================================
        # Keyword Increase
        #======================================================================
        for keyword in self.keywords_increase:
            pattern = r'^(?:[a-z0-9_]+:\s*|\s*\d{0,5}\s*)?' + re.escape(keyword) + r'(?=\b|\s|\(|$)'
            if re.match(pattern, temp_lower) and ('module procedure' not in temp_lower) and ('interface_' not in temp_lower):
                keyword_match = True
                self.skip = True
                break
        # if keyword_match:
        #     print(repr(temp_line), keyword_match, repr(keyword))
        #======================================================================

        #======================================================================
        # Keyword Decrease
        #======================================================================
        if not keyword_match:
            for keyword in self.keywords_decrease:
                pattern1 = r'^\s*\d{0,5}\s*' + re.escape(keyword) + r'(?=\s|\(|$|\n)'
                if re.match(pattern1, temp_lower):
                    keyword_dec_match = True
                    break
            # if keyword_dec_match:
            #     print(repr(temp_line), repr(keyword))
        #======================================================================

        #======================================================================
        # Keyword and Data Type combines e.g. real(8) elemental function
        #======================================================================
        if not keyword_match and not keyword_dec_match:
            for keyword in self.data_types:
                for function in self.combinations:
                    # print(keyword + ' ' + function)
                    pattern = rf"\b{re.escape(keyword)}(?:\s*\*\w+|\s*\([^()]*\))?\s*{re.escape(function)}\b"
                    if re.search(pattern, temp_lower):
                        keyword_data_types_match = True
                        break
                # if keyword_data_types_match:
                #     print(repr(temp_line), keyword_match, repr(keyword))
        
        #======================================================================
        # Checks for things like: elemental function or subroutine, etc
        #======================================================================
        if not keyword_match and not keyword_dec_match:
            for function in self.combinations:
                # print(function)
                #pattern = r'^(?:[a-z0-9_]+:\s*|\s*\d{0,5}\s*)?' + re.escape(function) + r'(?=\b|\s|\(|$)'
                pattern = (r'^(?:[a-z0-9_]+:\s*|\s*\d{0,5}\s*)?'
                            + re.escape(function).replace(
                            'type\\(\\.\\.\\.\\)',  # escape it as it appears in re.escape output
                            r'(?:type\s*\([^()]*\)|type\s*\*\w+)')  # real regex for type(charint) or type *mytype
                            + r'(?=\b|\s|\(|$)')
                # print(pattern)
                if re.match(pattern, temp_lower):
                    keyword_match = True
                    keyword_data_types_match = True
                    self.skip = True
                    break
                # if keyword_data_types_match:
                #     print(repr(temp_line), keyword_match, repr(keyword))
        #======================================================================
        # Check for goto's that randomly match the start of the line from a do loop
        #======================================================================
        if not keyword_match and not keyword_dec_match and not keyword_data_types_match:
            for goto in do_list:
                pattern1 = r'^\s*' + re.escape(goto[0]) + r'\b'
                idx = temp_lower.find(self.space)
                if re.match(pattern1, temp_lower.strip()[:idx]):
                    keyword_dec_match = True
            # if keyword_dec_match:
            #     print(repr(temp_line), keyword_match, repr(keyword))
        #======================================================================

    else:
        keyword = self.empty

    if keyword_match:
        # print(repr(keyword), self.indenter, repr(temp_line))
        pattern2 = r"^(?:[a-z0-9_]+:\s*|\s*\d{0,5}\s*)?do\b"
        if keyword.strip() == 'select':
            if self.select_indent:
                self.indenter += 1
            self.select_indent = True
        if keyword in ['type', 'where'] and not self.select_indent and not temp_lower.startswith('type (') and not temp_lower.startswith('type(') and not temp_lower.startswith('type ='):
            # print(keyword, self.indenter, repr(temp_line))
            # =======================================================
            # Look ahead for 'end type'
            # =======================================================
            is_type_block = False
            for k in range(j + 1, len(self.file_lines)):
                pattern = rf"^end\s*{re.escape(keyword.strip())}\b"
                if re.match(pattern, self.file_lines[k].lower().strip()):
                    is_type_block = True
                    break
                else:
                    is_type_block = False
            if is_type_block:
                # print(keyword, self.indenter, repr(temp_line))
                self.indenter += 1
                self.skip = True
            else:
                self.skip = False
        elif keyword == 'associate':
            # print(keyword, self.indenter, repr(temp_line))
            # =======================================================
            # Look ahead for 'end associate'
            # =======================================================
            is_associate_block = False
            for k in range(j + 1, len(self.file_lines)):
                pattern = rf"^end\s*{re.escape(keyword.strip())}\b"
                if re.match(pattern, self.file_lines[k].lower().strip()):
                    is_associate_block = True
                    break
                else:
                    is_associate_block = False
            if is_associate_block:
                # print(keyword, self.indenter, repr(temp_line))
                self.indenter += 1
                self.skip = True
            else:
                self.skip = False
        elif keyword == 'if ' or keyword == 'if\n':
            # print(keyword, self.skip, self.indenter, repr(temp_line))
            if temp_lower[-5:].strip() == 'then' or (") then;" in temp_lower and not any(keyword in temp_lower for keyword in ['end if', 'endif'])):
                # print(keyword, self.skip, self.indenter, repr(temp_line))
                self.indenter += 1
                self.skip = True
            elif temp_lower[-2].strip() == self.continuation_char or (not self.free_form and len(self.file_lines[j+1]) > 6 and self.file_lines[j+1][5] != self.space):
                # print(keyword, self.skip, self.indenter, repr(temp_line))
                if self.file_lines[j+1][-2].strip() == self.continuation_char or not self.free_form:
                    # print(keyword, self.skip, self.indenter, repr(temp_line))
                    if self.free_form:
                        while self.file_lines[j+1][-2].strip() == self.continuation_char:
                            j += 1
                    else:
                        while len(self.file_lines[j+2]) > 5 and self.file_lines[j+2][5] != self.space:
                            j += 1
                        # will need to come back here possibly in case the if statement goes over and over
                    if self.file_lines[j+1][-5:].strip().lower() == 'then':
                        # print(temp_line)
                        self.indenter += 1
                        self.skip = True
                    else:
                        # print(keyword, self.skip, self.indenter, repr(temp_line))
                        self.skip = False
                elif self.file_lines[j+1][-5:].strip().lower() == 'then':
                    # print(keyword, self.skip, self.indenter, repr(temp_line))
                    self.indenter += 1
                    self.skip = True
                else:
                    # print(keyword, self.skip, self.indenter, repr(temp_line))
                    self.skip = False
            else:
                pattern = r'^\s*\d{0,5}\s*if\s*\([^()]*\)\s*$' # Match case for 'if (...)' followed by no then, but an else may follow
                if re.match(pattern, temp_lower):
                    self.indenter += 1
                    self.skip = True
                else:
                    self.skip = False
        elif keyword == 'do ' or keyword == 'do\n' and re.match(pattern2, temp_lower.strip()):
            self.indenter += 1
            self.skip = True
            # print(temp_line, self.indenter)
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
        elif not temp_lower.replace(self.space, self.empty).startswith('type(') and not temp_lower.startswith('do '):
            # print(keyword, self.indenter, repr(temp_line))
            if keyword in ['type is', 'class is', 'class default', 'case']:
                # print(keyword, self.indenter, repr(temp_line))
                self.class_happened = True
                if self.select_indent:
                    if not self.first_case:
                        self.first_case = True
                        self.indenter += 1
                    self.skip = True
                # =======================================================
                # Look ahead for 'select'
                # =======================================================
                is_type_block = False
                for k in range(j + 1, len(self.file_lines)):
                    pattern_end = rf"^\s*end\s?select\b"
                    pattern_start = rf"^\s*select\b"
                    if re.match(pattern_start, self.file_lines[k].lower().strip()):
                        self.skip_select = True
                        if not self.first_case:
                            self.select_indenter = 0
                        else:
                            self.select_indenter = -1
                        break
                    if re.match(pattern_end, self.file_lines[k].lower().strip()):
                        self.select_indenter = self.indenter
                        break
                    
            elif not (temp_lower.startswith('type *') and not self.select_indent) and not temp_lower.startswith('type ='):
                self.indenter += 1
                self.skip = True
            else:
                self.skip = False
        elif re.search(rf"\b{re.escape('type')}(?:\s*\*\w+|\s*\(\w+\))?\s*function\b", temp_lower):
            # print(keyword, self.skip, self.indenter, repr(temp_line))
            self.indenter += 1
            self.skip = True
        else:
            # print(keyword, self.skip, self.indenter, repr(temp_line))
            self.skip = False
    elif keyword_data_types_match:
        # print(temp_lower)
        self.indenter += 1
        self.skip = True
    elif re.match(r'^\s*\d{0,5}\s+continue(\s|$)', temp_lower) and self.free_form:
        # print(repr(temp_line), do_list)
        for goto in do_list:
            # print(goto[0])
            if temp_line.startswith(goto[0]):
                self.indenter -= (1 + goto[1])
                do_list.remove(goto)
                break
    elif keyword_dec_match:
        # print(keyword, self.indenter, repr(temp_line))
        if temp_lower.startswith("end =") or re.match(r'^\s*\d{0,5}\s+end =', temp_lower):
            pass
        elif temp_lower.startswith("endselect") or temp_lower.startswith("end select"):
            self.select_indent = False
            self.first_case = False
            if self.class_happened:
                self.indenter -= 2
            else:
                # print(keyword, self.indenter, repr(temp_line))
                self.indenter -= 1
            if self.select_indenter:
                self.select_indenter += 1
        elif (temp_line.strip() == 'continue') or (temp_lower.startswith("continue") and not self.free_form) or (re.match(r'^\s*\d{0,5}\s+continue\s*\S*(\s|$)', temp_lower) and self.free_form) \
            or (re.match(r'^\s*\d{0,5}\s+end do\s*\S*(\s|$)', temp_lower) and self.free_form) or (re.match(r'^\s*\d{0,5}\s+enddo\s*\S*(\s|$)', temp_lower) and self.free_form):
                # print(keyword, self.indenter, repr(temp_line))
                if do_list:
                    for goto in do_list:
                        # print(goto)
                        if re.match(r'^' + re.escape(goto[0]) + r'\b', ff_line.lstrip()) or temp_line.startswith(goto[0]):
                            self.indenter -= (1 + goto[1])
                            do_list.remove(goto)
                            break
                elif (re.match(r'^\s*\d{0,5}\s+end do\s*\S*(\s|$)', temp_lower) and self.free_form) or (re.match(r'^\s*\d{0,5}\s+enddo\s*\S*(\s|$)', temp_lower) and self.free_form):
                    self.indenter -= 1
                    self.skip = False
        else:
            # print(keyword, self.indenter, repr(temp_line))
            self.indenter -= 1
            self.skip = False
            # print(self.file_lines[j-1].lower(), self.indenter, repr(temp_line))

    if re.match(r"^else(where|if)?\b", temp_lower): # else statements go back one, but that's it
        self.skip = True

    if self.skip:
        if keyword == 'select':
            if self.skip_select:
                # print(keyword, self.skip, self.indenter, repr(temp_line), self.select_indenter)
                temp_line = self.space * self.tab_len * (self.indenter + self.select_indenter - 1) + temp_line
                self.skip_select = False
            else:
                # print(keyword, self.skip, self.indenter, repr(temp_line), self.select_indenter)
                temp_line = self.space * self.tab_len * (self.indenter - 1) + temp_line
        else:
            temp_line = self.space * self.tab_len * (self.indenter - 1) + temp_line
        # print(temp_line)
        if self.free_form:
            if temp_line.strip()[-1] == self.continuation_char:
                self.skip = True
            else:
                self.skip = False
        else:
            if len(self.file_lines) > j + 1 and len(self.file_lines[j + 1]) > 5 and self.file_lines[j + 1][5] != self.space and not self.file_lines[j + 1][0].isalpha() and self.file_lines[j + 1][0] not in ['*', self.comment]:
                self.skip = True
            else:
                self.skip = False
    else:
        temp_line = self.space * self.tab_len * self.indenter + temp_line

    if self.indenter < 0:
        self.indenter = 0
    # print(self.indenter, repr(temp_line))
    return temp_line
