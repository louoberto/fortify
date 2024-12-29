# ===========================================================
def find_defines(include_file):
    """
    Scans through a file, looks for #define statements, captures those variables
    """
    defines = []
    with open(include_file, "r") as inFile:  # Inhale the whole file
        lynes = inFile.readlines()

        def_str = "#define"

        for lyne in lynes:
            if def_str in lyne[: len(def_str)]:
                var = lyne.split()[1]
                if "(" in var:  # If the variable == an array, just grab the var name
                    var = var[: var.index("(")]
                defines.append(var)

    return defines
