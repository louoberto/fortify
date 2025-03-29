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
            if filename[-2:].lower() in [".f"] or filename[-4:].lower() in [".for", ".f77", ".ftn", ".fpp", ".f66"]:
                free_form = False
            self.free_form = free_form
            return
    except Exception as e:
        print(f"Could not open/read: {filename}")
        print(f"Error: {e}")
        print("Quitting")
        sys.exit(1)
