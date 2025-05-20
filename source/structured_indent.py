# =============================================================================
# Function: structured_indent
# =============================================================================
# Purpose:
# This will properly nest and indent code largely based on the keyword
# lists found in keywords_increase and keywords_decrease
# =============================================================================
import re
from inspect import currentframe
debug_me = 0

do_list = []
do_count = 0
def structured_indent(self, temp_line, current_line, ff_line, self_skip_true):
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
    # print(repr(temp_line))
    temp = ''
    if self.code_line.strip() and self.code_line.strip()[-1] == self.continuation_char:
        temp = temp_lower
        for k in range(len(self.lines) - 1, -1, -1):
            prev_line = self.lines[k].rstrip()  # remove any trailing whitespace including '\n'
            if prev_line.endswith('&'):
                prev_line = prev_line.rstrip()[:-1].rstrip() # Remove the '&' and any extra spaces
                temp = prev_line + temp    # Prepend the previous line
                temp = temp.replace('&','')
                # if temp_lower.startswith('block'):
                #     print(repr(temp.replace('&','')))
                j -= 1
            else:
                break
        # print(repr(temp.strip()))
    keyword_match = False
    keyword_dec_match = False
    # print(repr(temp_line))
    if temp_lower.strip()[0] != '!':
        #======================================================================
        # Keyword and Data Type combines
        # Checks for things like:
        # elemental function or subroutine, real(8) elemental function, etc
        #======================================================================
        for function in self.function:
            # print(function)
            if re.search(rf'^\s*\d{{0,5}}\s*end\s*{re.escape(function)}\b', temp_lower):
                continue
            pattern = rf'^\s*\d{{0,5}}\s*(?:[a-z0-9_]+(?:\*[\w\d]+|\([^()]*\)|\([^()]*\([^()]*\)[^()]*\))?\s+){{0,5}}{re.escape(function)}\b(?!\s*\()'
            pattern2 = rf'^\s*\d{{0,5}}\s*[a-zA-Z_][a-zA-Z0-9_]*\*\(\*\)\s+{re.escape(function)}\b(?!\s*\()'
            if re.match(pattern, temp_lower) or re.match(pattern2, temp_lower):
                if temp and re.match(pattern, temp) or re.match(pattern2, temp):
                    keyword_match = False
                else:
                    keyword_match = True
                    keyword = function
                    # print(repr(temp_lower), keyword_match, repr(keyword))
                break
        #======================================================================

        #======================================================================
        # Keyword Increase
        #======================================================================
        if not keyword_match:
            # print(repr(temp_line))
            # if debug_me:
            #     self.debug(currentframe().f_lineno, '', repr(temp_line), j)
            for keyword in self.keywords_increase:
                pattern = rf'^\s*(?:[a-z0-9_]+\s*:\s*|\d{{0,5}}\s*)?{re.escape(keyword)}(?=\b|\s|\(|$)'
                if re.match(pattern, temp_lower) and (' interface_' + keyword + ' ' not in temp_lower):
                    keyword_match = True
                    self.skip = True
                    if debug_me:
                        self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
                    if temp:
                        # if keyword == 'block':
                        #     print(repr(temp))
                        for keyword in self.keywords_increase:
                            pattern = rf'^\s*(?:[a-z0-9_]+\s*:\s*|\d{{0,5}}\s*)?{re.escape(keyword)}(?=\b|\s|\(|$)'
                            if re.match(pattern, temp):
                                keyword_match = True
                                self.skip = True
                                # print(repr(temp.lstrip()))
                                if debug_me:
                                    self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
                                break
                            else:
                                keyword_match = False
                                self.skip = False
                                if debug_me:
                                    self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
                                # print(keyword, self.indenter, repr(temp_line))
                        # print(repr(temp_lower), repr(temp))
                    # print(repr(temp_lower))#, keyword_match, repr(keyword))
                    break
        #======================================================================

        #======================================================================
        # Keyword Decrease
        #======================================================================
        if not keyword_match:
            # print(repr(temp_line))
            for keyword in self.keywords_decrease:
                pattern1 = r'^\s*\d{0,5}\s*' + re.escape(keyword) + r'(?=\s|\(|$|\n|\;)'
                if re.match(pattern1, temp_lower):
                    keyword_dec_match = True
                    # print(repr(temp_line), repr(keyword))
                    break
        #======================================================================

        #======================================================================
        # Check for goto's that randomly match the start of the line from a do loop
        #======================================================================
        if not keyword_match and not keyword_dec_match:
            for goto in do_list:
                pattern1 = r'^\s*' + re.escape(goto[0]) + r'\b'
                idx = temp_lower.find(self.space)
                if re.match(pattern1, temp_lower.strip()[:idx]):
                    keyword_dec_match = True
            # if keyword_dec_match:
            #     print(repr(temp_line), keyword_match, repr(keyword))
            if keyword_dec_match:
                if debug_me:
                    self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
        #======================================================================

    else:
        keyword = self.empty
        if debug_me:
            self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
    # print(repr(temp_line), keyword_match, repr(keyword))
    pattern_equal = rf'^\s*(?:[a-z0-9_]+\s*:\s*)?{re.escape(keyword)}\s*(?:\([^()]*\))?\s*=' # Match 'keyword ='
    if re.match(pattern_equal, temp_lower):
        self.skip = False
        # print(repr(temp_line), keyword_match, repr(keyword))
        if debug_me:
            self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
    elif keyword_match:
        if debug_me:
            self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
        # print(repr(keyword), self.indenter, repr(temp_line))
        pattern2 = r"^(?:[a-z0-9_]+:\s*|\s*\d{0,5}\s*)?do\b"
        pattern_select = r'\s*(?:[a-z0-9_]+\s*:\s*)?select\s+\w+\b(?!\s*=|\s*\([^)]*\)\s*=)'
        # ^\s*(?:[a-z0-9_]+\s*:\s*
        if keyword == 'select':
            # print(repr(keyword), self.indenter, repr(temp_lower), self.select_indent)
            if re.match(pattern_select, temp_lower):
                # print(repr(keyword), self.indenter, repr(temp_lower), self.select_indent)
                if self.select_indent:
                    self.indenter += 1
                self.select_indent = True
            else:
                # print(repr(keyword), self.indenter, repr(temp_lower), self.select_indent)
                self.skip = False
        if keyword in ['type', 'where'] and not self.select_indent and not temp_lower.startswith('type (') and not temp_lower.startswith('type(') and not temp_lower.startswith('type ='):
            # print(keyword, self.indenter, repr(temp_line))
            if self.is_where_oneliner(temp_lower):
                # print(keyword, self.indenter, repr(temp_line))
                self.skip = False
            else:
                # =======================================================
                # Look ahead for 'end type'
                # =======================================================
                is_type_block = False
                for k in range(j + 1, len(self.file_lines)):
                    pattern = rf"^end\s*{re.escape(keyword.strip())}\s*;?\b"
                    if re.match(pattern, self.file_lines[k].lower().strip()):
                        # print(keyword, self.indenter, repr(temp_line))
                        is_type_block = True
                        break
                    else:
                        is_type_block = False
                if is_type_block:
                    # print(keyword, self.indenter, repr(temp_line))
                    self.indenter += 1
                    self.skip = True
                else:
                    # print(keyword, self.indenter, repr(temp_line))
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
                # print(keyword, self.indenter, repr(temp_line))
                self.skip = False
        elif keyword == 'if ' or keyword == 'if\n':
            # print(keyword, self.skip, self.indenter, repr(temp_line))
            if temp_lower[-5:].strip() == 'then' or (") then;" in temp_lower and not any(keyword in temp_lower for keyword in ['end if', 'endif'])):
                # print(keyword, self.skip, self.indenter, repr(temp_line))
                self.indenter += 1
                self.skip = True
            elif temp_lower[-2].strip() == self.continuation_char or temp_lower[-1].strip() == self.continuation_char or (not self.free_form and len(self.file_lines[j+1]) > 6 and self.file_lines[j+1][5] != self.space):
                # print(keyword, self.skip, self.indenter, repr(temp_line))
                # print(repr(self.file_lines[j+1][-2].strip()))
                # pattern = r'^\s*(?:\d{0,5}\s*)?if\s*\([^\)]*&\s*$'
                if (
                    j + 1 < len(self.file_lines)
                    and len(self.file_lines[j + 1]) >= 2
                    and self.file_lines[j + 1][-2].strip() == self.continuation_char
                ) or re.match(pattern, temp_lower) or not self.free_form:
                    # print(keyword, self.skip, self.indenter, repr(temp_line))
                    if self.free_form:
                        while (
                            j + 1 < len(self.file_lines)
                            and len(self.file_lines[j + 1]) >= 2
                            and self.file_lines[j + 1][-2].strip() == self.continuation_char
                        ):
                            j += 1
                    else:
                        # print(self.file_lines[j+2]) #self.file_lines[j+2][
                        while (j + 2 < len(self.file_lines) and len(self.file_lines[j + 2]) > 0 and ((len(self.file_lines[j + 2]) > 5 and self.file_lines[j + 2][5] != self.space) or self.file_lines[j + 2].lstrip().startswith((self.continuation_char, '#'))) ):
                            # print(self.file_lines[j+2])
                            self_skip_true += 1
                            j += 1
                        # will need to come back here possibly in case the if statement goes over and over
                    dummy1, line_to_check, dummy2, dummy3 = self.line_breakup(self, self.file_lines[j + 1])
                    if line_to_check.strip().lower().endswith('then'):
                        # print(temp_line)
                        self.indenter += 1
                        self.skip = True
                    else:
                        # print(keyword, self.skip, self.indenter, repr(self.file_lines[j+1][-6:].strip().lower()))
                        self.skip = False
                elif self.file_lines[j+1][-5:].strip().lower() == 'then':
                    # print(keyword, self.skip, self.indenter, repr(temp_line))
                    self.indenter += 1
                    self.skip = True
                else:
                    # print(keyword, self.skip, self.indenter, repr(temp_line))
                    self.skip = False
            else:
                pattern = r'^\s*\d{0,5}\s*if\s*\([^()]*\)\s*$' # Match case for 'if (...)' followed by no then nor any text afterward, but an else may follow
                if re.match(pattern, temp_lower):
                    self.indenter += 1
                    self.skip = True
                else:
                    # print(keyword, self.indenter, repr(temp_line))
                    self.skip = False
        elif keyword in ['do ', 'do\n'] and re.match(pattern2, temp_lower.strip()):
            self.indenter += 1
            self.skip = True
            # print(temp_line, self.indenter)
            # Check if there is a continue with it
            i = temp_lower.find('do')
            if i != -1:
                i += len('do')
                while i < len(temp_lower) and temp_lower[i] == self.space:
                    i += 1
                if i < len(temp_lower) and temp_lower[i].isnumeric():
                    # print(temp_lower[i])
                    temp_num = self.empty
                    while i < len(temp_lower) and temp_lower[i].isnumeric():
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
            if keyword in ['type is', 'class is', 'class default', 'case', 'rank']:
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
            elif re.match(r'\bselect\b(?=[^\n=]*=)', temp_lower) and not 'select type' in temp_lower:
                # print(keyword, self.indenter, repr(temp_line))
                self.skip = False
            elif not (temp_lower.startswith('type *') and not self.select_indent) and not temp_lower.startswith('type ='):
                # print(keyword, self.indenter, repr(temp_line))
                pattern = r'^\s*forall\s*\([^)]*\)\s+(?!;)\S' # skip the forall() + code one-liner
                pattern_map = r'^\s*map\s*=>'
                if self.is_forall_oneliner(temp_lower) or re.match(pattern_map, temp_lower):
                    # print(bool(re.match(pattern, temp_lower)))
                    self.skip = False
                else:
                    if keyword == 'module procedure':
                        if self.inside_submod:
                            # print(keyword, self.indenter, repr(temp_line))
                            self.indenter += 1
                            self.skip = True
                        else:
                            # print(keyword, self.indenter, repr(temp_line))
                            self.skip = False
                    else:
                        if keyword == 'submodule':
                            self.inside_submod = True
                        # print(keyword, self.indenter, repr(temp_line))
                        self.indenter += 1
                        self.skip = True
            else:
                # print(keyword, self.indenter, repr(temp_line))
                self.skip = False
        elif re.search(rf"\b{re.escape('type')}(?:\s*\*\w+|\s*\(\w+\))?\s*function\b", temp_lower):
            # print(keyword, self.skip, self.indenter, repr(temp_line))
            self.indenter += 1
            self.skip = True
        else:
            # print(keyword, self.skip, self.indenter, repr(temp_lower))
            if keyword in self.function:
                self.indenter += 1
                self.skip = True
            else:
                # print(keyword, self.indenter, repr(temp_line))
                self.skip = False
    elif re.match(r'^\s*\d{0,5}\s+continue(\s|$)', temp_lower) and self.free_form:
        # print(repr(temp_line), do_list)
        for goto in do_list:
            # print(goto[0])
            if temp_line.startswith(goto[0]):
                self.indenter -= (1 + goto[1])
                do_list.remove(goto)
                break
    elif not self.free_form and any(re.search(r'\d', line) for line in self.file_lines[j][0:5]):
        number_line = self.file_lines[j][0:5].strip()
        for goto in do_list:
            # print(goto[0])
            if number_line == goto[0]:
                self.indenter -= (1 + goto[1])
                do_list.remove(goto)
                break
    elif keyword_dec_match:
        # print(keyword, self.indenter, repr(temp_line))
        if keyword == 'endsubmodule' or (keyword == 'end' and 'end submodule' in temp_lower):
            self.inside_submod = False
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
                    if debug_me:
                        self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
                    # print(keyword, self.indenter, repr(temp_line))
        else:
            # print(keyword, self.indenter, repr(temp_line))
            self.indenter -= 1
            self.skip = False
            if debug_me:
                self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
            # print(self.file_lines[j-1].lower(), self.indenter, repr(temp_line))
        # if temp_lower.strip().endswith(self.continuation_char):
        #     print(self.file_lines[j-1].lower(), self.indenter, repr(temp_line))

    if re.match(r"^else(where|if)?\b", temp_lower): # else statements go back one, but that's it
        self.skip = True
        if debug_me:
            self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
    # print(repr(temp_line), keyword_match, repr(keyword))
    if self.skip or self_skip_true > 0:
        # print(repr(temp_line), keyword_match, repr(keyword))
        if keyword == 'select':
            if self.skip_select:
                # print(keyword, self.skip, self.indenter, repr(temp_line), self.select_indenter)
                temp_line = self.space * self.tab_len * (self.indenter + self.select_indenter - 1) + temp_line
                self.skip_select = False
                if debug_me:
                    self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
            else:
                # print(keyword, self.skip, self.indenter, repr(temp_line), self.select_indenter)
                temp_line = self.space * self.tab_len * (self.indenter - 1) + temp_line
                if debug_me:
                    self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
        else:
            temp_line = self.space * self.tab_len * (self.indenter - 1) + temp_line
            # print(repr(temp_line), self.indenter - 1)
            if debug_me:
                self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
        # print(temp_line)
        if self.free_form:
            # print(temp_line)
            if temp_line.strip()[-1] == self.continuation_char:
                self.skip = True
                if debug_me:
                    self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
            else:
                # print(keyword, self.indenter, repr(temp_line))
                self.skip = False
                if debug_me:
                    self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
        else:
            # print(temp_line)
            if len(self.file_lines) > j + 1 and len(self.file_lines[j + 1]) > 5 and self.file_lines[j + 1][5] != self.space and not self.file_lines[j + 1][0].isalpha() and self.file_lines[j + 1][0] not in ['*', self.comment, '#']:
                # print(temp_line)
                self.skip = True
                if debug_me:
                    self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
            else:
                # print(temp_line)
                self.skip = False
                if debug_me:
                    self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)
        if self_skip_true > 0:
            self_skip_true -= 1
    else:
        # print(repr(temp_line), keyword_match, repr(keyword), self.indenter)
        temp_line = self.space * self.tab_len * self.indenter + temp_line
        if debug_me:
            self.debug(currentframe().f_lineno, keyword, repr(temp_line), j)

    if self.indenter < 0:
        self.indenter = 0
    # print(self.indenter, repr(temp_line))
    if temp_lower.strip().endswith(self.continuation_char):
        self.cont_happened = True
    else:
        self.cont_happened = False

    return temp_line, self_skip_true
