def remove_extra_space(self, j, char, code_line, temp_line):
    if code_line[j + 1] in [self.newline, self.space]:
        temp = temp_line
    else:
        temp = temp_line + char

    return temp