# ========================================================================
# Function: no_format
# ========================================================================
# Purpose:
# Check to see if a line says 'do not format'. If it does, leave it as is
# ========================================================================
def no_format(self, line):
    cmt_index = line.find(self.comment)
    if cmt_index >= 0 and self.no_format in line[cmt_index:]:
        return True
    else:
        return False
