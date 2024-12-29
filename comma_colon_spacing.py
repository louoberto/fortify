# ========================================================================
# Function: comma_colon_spacing
# ========================================================================
# Purpose:
# Will format 
# ========================================================================
def comma_colon_spacing(self, j, char, code_line, temp):
    if char == "," and code_line[j + 1] != self.space: # Comma case 1
        temp += temp + char + self.space
    elif char == "," and code_line[j - 1] == self.space: # Comma case 2
        temp = temp[:-1] + char
    elif char == ":" and code_line[j + 1] != ":" and code_line[j - 1] != ":": # Colon case 1
        if code_line[j + 1] != self.space and code_line[j - 1] != self.space:  # a=b
            temp += self.space + char + self.space
        elif code_line[j + 1] != self.space and code_line[j - 1] == self.space:  # maybe a =b
            temp += char + self.space
        elif code_line[j + 1] == self.space and code_line[j - 1] != self.space:  # could be a= b
            temp += self.space + char
        else:  # could be a = b
            temp += char
    elif char == ":" and code_line[j + 1] == ":" and code_line[j - 1] != ":": # Colon case 2
        if code_line[j - 1] != self.space:  # a=b
            temp += self.space + char
        else:  # could be a = b
            temp += char
    elif char == ":" and code_line[j + 1] != ":" and code_line[j - 1] == ":": # Colon case 3
        if code_line[j + 1] != self.space:  # a=b
            temp += char + self.space
        else:  # could be a = b
            temp += char
    else:
        temp += char

    return temp
