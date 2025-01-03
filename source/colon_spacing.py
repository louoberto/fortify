# ========================================================================
# Function: comma_colon_spacing
# ========================================================================
# Purpose:
# Should handle cases :: and , related formatting
# ========================================================================
def colon_spacing(self, j, char, code_line, temp_line):    
    if code_line[j + 1] and ':' not in [code_line[j - 1], code_line[j + 1]]: # Colon case 1
        if self.space not in [code_line[j - 1], code_line[j + 1]]:  # a:b
            if code_line[j - 1] == '(':
                if code_line[j + 1] == ',':
                    temp = temp_line + char
                else:
                    temp = temp_line + char + self.space
            else:
                temp = temp_line + self.space + char + self.space
        elif code_line[j + 1] != self.space and code_line[j - 1] == self.space:  # maybe a :b
            temp = temp_line + char + self.space
        elif code_line[j + 1] == self.space and code_line[j - 1] != self.space:  # could be a: b
            temp = temp_line + self.space + char
        else:  # could be a : b
            temp = temp_line + char
    elif code_line[j - 1] != ":" and code_line[j + 1] == ":": # Colon case 2
        if code_line[j - 1] != self.space:  # a::
            temp = temp_line + self.space + char
        else:  # could be a ::
            temp = temp_line + char
    elif code_line[j - 1] == ":" and code_line[j + 1] != ":": # Colon case 3
        if code_line[j + 1] != self.space:  # ::b
            temp = temp_line + char + self.space
        else:  # could be :: b
            temp = temp_line + char
    else:
        temp = temp_line + char
    return temp