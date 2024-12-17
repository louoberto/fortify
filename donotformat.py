#===========================================================
def doNotFormatCheck( lyne ):
    """
    Check to see if a line says 'do not format':
    """
    if "do not format" in lyne:
        return True
    else:
        return False