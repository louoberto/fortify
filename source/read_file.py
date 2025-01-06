# ========================================================================
# Function: read_file
# ========================================================================
# Purpose:
# Open a file, read and store the lines in an array. Also determine if
# we are fixed or free form.
# ========================================================================
import sys


def read_file(self, filename):
    free_form = True
    try:
        with open(filename, "r") as in_file:
            self.file_lines = in_file.readlines()
            if ".f" == filename[-2:] or ".F" == filename[-2:]:
                free_form = False
            self.free_form = free_form
            return
    except:
        print("Could not open/read: ", filename)
        print("Quitting")
        sys.exit(1)
