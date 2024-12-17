# ===========================================================
def processOpenFile(fileName):
    """
    Open a file, return all the lines in it and a new file to print to
    """
    try:
        with open(fileName, "r") as inFile:  # Inhale the whole file
            lynes = inFile.readlines()
            newfile = open(fileName, "w")
            return lynes, newfile
    except:
        print("Could not open/read: ", fileName)
        print("Quitting")
        sys.exit(3)