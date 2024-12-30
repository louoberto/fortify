# ========================================================================
# Function: no_format
# ========================================================================
# Purpose:
# Check to see if a line says 'do not fortify'. If it does, leave it as is
# ========================================================================
def no_format(line):
    if 'do not fortify' in line:
        return True
    else:
        return False
