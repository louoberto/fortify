from donotformat import doNotFormatCheck

#Variable declartion types, referenced in multiple functions
data_types = [
    'integer',
    'real',
    'complex',
    'character',
    'logical'
    ]

#===========================================================
def sortaVars(lynes, noSortName, f90):
    """
    Organizes variable declarations in order of the type and size
    """
    # Open file, grab lines in the file
    new_lynes=[]

    #Initialize flags and varaibles
    found = False
    varList=[]
    key=0
    keyList=[]

    for itr, lyne in enumerate(lynes):
        this_line = lyne.strip()
        if this_line != '!': # Skip line comments
            spaceloc=this_line.find(' ')
            parenloc=this_line.find('(') # For edge cases like 'character(len=*)'

            #Flag if there might be a declaration in this line
            if this_line[:spaceloc] in data_types or this_line[:parenloc] in data_types:
                found=True

            #Once found, and no longer finding data_types we must be done with this declar block
            if found and this_line[:spaceloc] not in data_types and this_line[:parenloc] not in data_types:
                found=False
                key+=1

            if found:
                if this_line.strip(): #check if this line == just empty whitespace, or if there == code in here
                    cmtloc = this_line.find('!')

                    #Deal with allocatable and save varaibles
                    if 'allocatable' in this_line[:cmtloc] and this_line[this_line.find('allocatable') -2] != ',':
                        this_line = this_line[ : this_line.find('allocatable')-1] + ',' + this_line[this_line.find('allocatable')-1:]

                    if ('save' in this_line[:cmtloc]) and (this_line[this_line.find('save')-2] != ',') and ( '::' in this_line[:cmtloc]):
                        this_line=this_line[:this_line.find('save')-1]+','+this_line[this_line.find('save')-1:]

                    keyList.append([this_line, key])

    newKeys=[]
    for itr in range(key):
        varList = []
        ktr = 0
        for jtr in range(len(keyList)):
            if keyList[jtr][1]==itr:
                varList.append(keyList[jtr][0])
                ktr+=1
        newKeys.append([itr, varList])

    varList = []
    for itr in range(key):
        if newKeys[itr][0]==itr:
            varList.append(sortVars(newKeys[itr][1], noSortName ))
    varList = [item for sublist in varList for item in sublist ]

    # Loop back through lines again
    found = False
    jtr= 0
    key = 0
    for itr, lyne in enumerate(lynes):
        this_line = lyne.lstrip()

        if doNotFormatCheck(lyne):
            new_lynes.append(lyne)
            jtr+=1 #Increment to the next varaible, even though we aren't formatting this one
        elif this_line != '!':
            parenloc = this_line.find('(')
            spaceloc=this_line.find(' ')
            specifierloc = this_line.find('::')

            #Check if first several characters look like a variable declaration
            if this_line[:spaceloc] in data_types or this_line[:parenloc] in data_types:
                found = True

            #once found, and no longer finding data_types we must be done with this declare block
            elif found and ( this_line[:spaceloc] not in data_types and this_line[:parenloc] not in data_types):
                found=False
                key += 1

            if found and lyne.strip():
                if specifierloc:
                    new_line = varList[jtr]['type'] + varList[jtr]['size'] + varList[jtr]['attributes'] + ' ' + varList[jtr]['name']
                else:
                    new_line = varList[jtr]['type'] + varList[jtr]['size'] + ' ' + varList[jtr]['name']
                if varList[jtr]['comment']:
                    new_line = new_line + ' ' + varList[jtr]['comment']
                new_line = new_line + '\n'
                new_lynes.append( new_line )
                jtr += 1
            else:
                new_lynes.append(lyne)
        else:
            new_lynes.append(lyne)
    return new_lynes


#===========================================================
# Helper functions
#===========================================================
def sortVars( varsList, noSortName = False ):
    """
    Sorts the variable list by type, then size, then name.
    """
    lenVars = len( varsList )
    fullList = [ '' ]*lenVars
    for v in range( lenVars):
        fullList[v] = parseParams(varsList[v])
    if noSortName:
        return sorted( fullList, key = lambda x:(x['type'], x['size']))
    else:
        return sorted( fullList, key = lambda x:(x['type'], x['size'], x['attributes'], x['name']))

#===========================================================
def parseParams( item ):
    """
    Take the item from the vars list and parse what == there.
    """
    cmtloc = item.find( '!' )
    spcloc = item.find( ' ' )
    paren_loc1 = item.find('(')
    paren_loc2 = item.find(')')
    dtype = item[0: paren_loc1 ] # The variable type (int, real, cmplx, char)
    size = item[paren_loc1:paren_loc2 + 1]

    # Just going to assume these lines are of the form datatype, paren with stuff, attributes, double colon, variables
    specifier_loc = item.find('::')
    if specifier_loc > 0:
        if cmtloc > 0:
            var = item[specifier_loc+2:cmtloc] #getting the rest of the args
            comment = item[cmtloc:]
        else:
            var = item[specifier_loc+2:] #Getting the rest of the args
            comment = ''
    else:
        if cmtloc > 0:
            var = item[paren_loc2+2:cmtloc] #getting the rest of the args
            comment = item[cmtloc:]
        else:
            var = item[paren_loc2+2:] #Getting the rest of the args
            comment = ''
    attributes = ''
    if item.find(','):
        if item.find(',') < specifier_loc:
            attributes = item[item.find(',') : specifier_loc -1]
    dtype = dtype.strip()
    var = var.strip()
    size=size.strip()
    attributes = attributes.strip() + ' ::'

    #Send back that info in a dict-style array
    return { 'type': dtype, 'name': var, 'size': size, 'comment': comment, 'attributes': attributes }
