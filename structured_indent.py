# ========================================================================
# Function: structured_indent
# ========================================================================
# Purpose:
# Will format  I believe this handles = - 0.213 to = -0.213 for example
# ========================================================================
from no_format import no_format


def structured_indent(self):
    indenter = 0
    skip = False
    caller = False
    callerIndent = 0
    first_case = False
    endsub = False
    space = ' '
    new_file_lines = []
    for line in self.file_lines:
        # Skip blank lines
        if not line.strip():
            new_file_lines.append(line)
            continue
        
        # Skip formatting if any of the following conditions are met
        #   1. If there is a comment in the first column
        #   2. FORMAT statement is in the line.
        #   3. There is a "do not fortify" in the line.
        #   4. Preprocessor directive
        cmt_index = line.find("!")
        if cmt_index == 0 or "format" in line[:cmt_index] or no_format(line) or "#" in line.strip()[0]:
            new_file_lines.append(line)
            continue
        elif cmt_index > 0:
            code_line = line[:cmt_index]
            cmnt_line = line[cmt_index:]
        else:
            code_line = line
            cmnt_line = ""

        if not self.free_form:
            ff_line = code_line[:self.ff_column_len]
            code_line = code_line[self.ff_column_len:]
        else:
            ff_line = ""

        stop = False
        btr = 0 
        
        for jtr, char in enumerate(code_line):
            if stop:
                continue
            elif char.isalpha():
                btr = jtr
                stop = True

        temp = ''
        weird_indent = False        
        if code_line.replace(' ', '')[0].isnumeric() and ('if (' in code_line[btr:btr+4] or 'do ' in code_line[btr:btr+3]):
            temp = code_line[:btr].strip()
            code_line = code_line[btr:].lstrip()
            indenter += 1
            skip = True
        elif code_line.replace(' ', '')[0].isnumeric() and 'enddo' in code_line[btr:btr+5]:
            temp = code_line[:btr].strip()
            code_line = code_line[btr:].lstrip()
            indenter -= 1
        elif code_line.strip().startswith('if (') and 'else' not in code_line.strip()[0:4]:
            indenter += 1
            skip = True
        elif (any(code_line.strip().startswith(keyword + space) for keyword in self.keywords_increase) or 
              any(code_line.strip().startswith(item + ' function ') for item in self.data_types)):
            indenter += 1
            skip = True
        elif any(code_line.strip().startswith(keyword) for keyword in self.keywords_decrease):
            indenter -= 1
        
        elif code_line.strip().startswith('do ') and not code_line[3].isdigit():
            indenter += 1
            skip = True
        elif ': do' in code_line and not code_line[code_line.find(': do')-1] == ':':
            if not code_line.strip().startswith('!'):
                templyne = code_line.lstrip().replace(' : do', ': do', 1)
                code_line = templyne
                indenter += 1
                skip = True
        elif code_line.strip().startswith('enddo'):
            indenter -= 1
        elif code_line.strip().startswith('type ') and code_line[5].isalpha():
            indenter += 1
            skip = True
        elif code_line.strip().startswith('type, ') and code_line[6].isalpha():
            indenter += 1
            skip = True
        elif code_line.strip().startswith('module ') and code_line.strip()[len('module ')+1].isalpha():
            indenter += 1
            skip = True
        elif 'interface ' in code_line.strip()[:len('interface ')] and code_line.strip()[len('interface ')+1].isalpha() or code_line.strip().startswith('interface'):
            indenter += 1
            skip = True
        elif code_line.strip().startswith('select case'):
            indenter += 1
            skip = True
        elif code_line.strip().startswith('case'):
            if not first_case:
                first_case = True
                indenter += 1
            elif first_case:
                weird_indent = True
            skip = True
        elif code_line.strip().startswith('endselect') or code_line.strip().startswith('end select'):
            indenter -= 2
        elif code_line.strip().startswith('structure ') and code_line.strip()[len('structure ')] == '/':
            indenter += 1
            skip = True
        if 'else' in code_line.lstrip()[:4] or 'elseif' in code_line.strip()[:6] or 'elsewhere' in code_line.strip()[:6]:
            skip = True
        if endsub:
            if code_line.strip():
                if 'endprogram' == code_line.strip()[:len('endprogram')]:
                    endsub = False
                    indenter -= 1
        code_line = code_line.lstrip() #Remove that whitespace and start over
        if code_line:
            if code_line[0] == '!': #Get comments out of the way first
                if self.free_form:
                    code_line = space*self.tab_len*indenter+code_line
                else:
                    code_line = space*self.ff_column_len + space*self.tab_len*indenter+code_line
            elif code_line[0] == '&':
                if skip:
                    if weird_indent:
                        code_line=space*(self.ff_column_len-1) + code_line[0] + space*self.tab_len *(indenter-2)+code_line[1:].lstrip()
                        weird_indent = False
                    else:
                        code_line=space*(self.ff_column_len-1)+code_line[0] + space*self.tab_len*(indenter-1)+code_line[1:].lstrip()
                    skip=False
                else:
                    checkindent=0
                    if indenter == 0:
                        checkindent=1
                    if code_line[jtr-1].lstrip()[:5] == 'call ':
                        caller=True
                        if indenter != 0:
                            callerIndent=1
                    if caller and code_line[1:].lstrip()[0]==')':
                        caller=False
                    code_line = space *(self.ff_column_len-1) + code_line[0] + space*self.tab_len*indenter + space*self.tab_len*checkindent + space*self.tab_len*callerIndent + code_line[1:].lstrip()
                    if not caller:
                        callerIndent=0
            elif code_line[0].isnumeric():
                flag=True
                ktr=0
                for jtr, char in enumerate(code_line):
                    if flag:
                        if char.isnumeric():
                            pass
                        else:
                            flag = False
                            ktr = jtr
                if self.free_form:
                    code_line=space*self.tab_len*indenter + code_line.lstrip()
                else:
                    code_line=code_line[:ktr] + space *(6-ktr)+ space*self.tab_len*indenter + code_line[ktr:].lstrip()
            else:
                if skip:
                    if self.free_form:
                        code_line=space*self.tab_len*(indenter-1) + code_line
                    else:
                        code_line=space*(self.ff_column_len-1) + space+ space*self.tab_len*(indenter-1) + code_line
                    skip = False
                else:
                    if self.free_form:
                        code_line = space*self.tab_len *indenter +code_line
                    else:
                        code_line = space*self.ff_column_len + space*self.tab_len *indenter +code_line
        else:
            code_line='\n'
        if temp != '':
            code_line = temp + code_line[len(temp):]
        new_file_lines.append(ff_line + code_line + cmnt_line)
    self.file_lines = new_file_lines
    return