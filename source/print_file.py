# ========================================================================
# Function: print_file
# ========================================================================
# Purpose:
# Replace the original file with the newly formatted lines.
# ========================================================================
import sys

def print_file(self, filename):
    try:
        with open(filename, "w") as out_file:
            out_file.writelines(self.file_lines)
    except Exception as e:
        print(f"Could not open/read: {filename}")
        print(f"Error: {e}")
        print("Quitting")
        sys.exit(2)
