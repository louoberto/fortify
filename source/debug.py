# ========================================================================
# Function: slash_spacing
# ========================================================================
# Purpose:
# Print out line, character, index, and code line for debugging purposes
# ========================================================================
from inspect import currentframe

def debug(line_no, char, code_line, index):
    print(f"line = {line_no} | char = {char} | index = {index} | code_line: {code_line}")