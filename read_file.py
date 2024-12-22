import sys

def read_file(self, filename):
    """
    Open the file and return all the lines in an array
    """
    free_form = True
    try:
        with open(filename, "r") as in_file:
            self.file_lines = in_file.readlines()
            if ".f" == filename[-2:] or ".F" == filename[-2:]:
                free_form = False
            self.free_form = free_form
            return self
    except:
        print("Could not open/read: ", filename)
        print("Quitting")
        sys.exit(1)
