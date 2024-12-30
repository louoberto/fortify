# ========================================================================
# Function: print_file
# ========================================================================
# Purpose:
# Replace the original file with the newly formatted lines.
# ========================================================================
import sys


def print_file(self, fortran_file):
    try:
        with open(fortran_file, "w") as out_file:
            out_file.writelines(self.file_lines)
    except:
        print("Could not open/read: ", fortran_file)
        print("Quitting")
        sys.exit(2)
