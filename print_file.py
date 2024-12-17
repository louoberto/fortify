import sys

# ===========================================================
def print_file(lynes, fileName):
    """
    Prints lynes to fileName
    """
    try:
        with open(fileName, "w") as outFile:
            outFile.writelines(lynes)

    except:
        print("Could not open/read: ", fileName)
        print("Quitting")
        sys.exit(2)