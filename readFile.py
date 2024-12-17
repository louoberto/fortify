from donotformat import doNotFormatCheck

# ==========================================================
def read_file(fileName):
    """
    Open a file, return all the lines in it
    """
    try:
        with open(fileName, "r") as inFile:
            lynes = inFile.readlines()
            return lynes
    except:
        print("Could not open/read: ", fileName)
        print("Quitting")
        sys.exit(1)
