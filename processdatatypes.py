from donotformat import doNotFormatCheck

#----------------------------------------------
# Define global variables used across multiple functions
#----------------------------------------------
spacing = 6 #First 6 cols go unused in most cases
spaceamp = 5
indent = 3 #default indentation
lastcol = 131 #Last usable column in Fortran


#Variable declartion types, referenced in multiple functions
data_types = [
    'integer',
    'real',
    'complex',
    'character',
    'logical'
    ]

#===========================================================
def processDatatypes( lynes, f90 ):
    """
    Organizes the data types, makes their size explicit
    """
    new_lynes=[]
    #=======================================================
    # Process each line of the file one at a time. If raw == given, store those lines.
    temp = ''
    skipLynes = [0,0]
    diff_parens=0
    write_statement=False
    for itr, lyne in enumerate(lynes):
        # Now we process multiple variables declared on a single line, as well as 
        #handling variables that didn't space properly.
        if diff_parens != 0 or 'format' in lyne:
            lparens=lyne.count('(')
            rparens=lyne.count(')')
            diff_parens=diff_parens+lparens-rparens

        # If we are converting output format for a write() statement, dont change formatting
        if diff_parens == 0 and 'write' in lyne and lyne.find('write') < lyne.find('!'):
            next_lyne =lynes[itr+1]
            if next_lyne.strip(): #is this line blank?
                if next_lyne.strip()[0] == '&': #It's not blank. Are we continuing a write?
                    write_statement=True

        #If we are in the middle of a write statement, dont reformat these print statements
        elif write_statement and '&' not in lyne.strip():
            write_statement = False

        # Loop through, format the code
        if not doNotFormatCheck( lyne ) and diff_parens == 0 and not write_statement:
            if f90:
                lyne_strip = lyne[:].lstrip()
            else:
                lyne_strip = lyne[spacing:].lstrip()

            specifier_info = ''
            specifier_loc = 0
            for dtype in data_types:
                numAmps = 0  # This counts number of ampersands (line conts)
                if dtype == lyne_strip[:len(dtype)] and not lyne_strip[len(dtype)].isalnum():
                    # Then we found a line that has a datatype. Start to process it.
                    # Find the data length, if given
                    tempType = dtype
                    if lyne_strip.replace(' ', '')[len(dtype)] == '(':
                        parenon = lyne.find('(')
                        parenoff = lyne.find(')')
                        #print(lyne)
                        if lyne[parenoff+1] == ',':
                            specifier_loc = lyne.find('::')
                            specifier_info = lyne[parenoff+1:specifier_loc]
                        tempType = dtype + lyne[parenon:parenoff+1] #this should get things like 'real( 4 )'
                        if specifier_loc > 0:
                             temp = tempType + lyne[specifier_loc+2:-1]
                        else:
                            temp = tempType + lyne[parenoff+1:-1]
                    else:
                        #print(lyne[len(dtype)],lyne)
                        # No size was given, also we want to try and find if there is a comma involved. 
                        this_happened = False
                        if lyne.strip()[len(dtype)] == ',':
                            tempType = lyne[len(dtype)]
                            this_happened = True
                        if dtype == 'complex':
                            tempType = dtype + '(8),' if this_happened else dtype + '(8)'
                        elif dtype == 'character':
                            tempType = dtype + '(1),' if this_happened else dtype + '(1)'
                        else:
                            tempType = dtype + '(4),' if this_happened else dtype + '(4)'

                        parenon = tempType.find('(')
                        parenoff = tempType.find(')')
                        if this_happened:
                            specifier_loc = lyne.find('::')
                            specifier_info = lyne[len(dtype):specifier_loc]
                        #tempType = dtype + lyne[parenon:parenoff+1] #this should get things like 'real( 4 )'
                        if specifier_loc > 0:
                             temp = tempType + lyne[specifier_loc+2:-1]
                        else:
                            temp = tempType + lyne[parenoff+1:-1]

                        addstar = lyne.lstrip()
                        addstar = addstar.find(' ')

                        if f90:
                            temp = tempType + lyne.lstrip()[addstar:]
                        else:
                            temp = ' ' * spacing + tempType + lyne.lstrip()[addstar:]

                    #===========================================
                    if lyne.find('!') == -1: #Then this line had no comments, making life easy for us. If there are comments at this juncture, that will be difficult....
                        if lyne.strip()[-1]==',':#Then we got continuations to contend with.
                            numAmps=numAmps + 1
                            temp += lynes[itr+numAmps]
                            while lynes[ itr+numAmps].strip()[-1]==',':
                                numAmps=numAmps+1
                                temp +=lynes[itr+numAmps]
                    skipLynes=[itr,numAmps] #This will be used to skip the continuations later
                    #=================================================
                    # At this point we have datatype and its name. Time to process the lyne based on
                    # how many there are first. Will need to sort later
                    # this may include one var or many lines of vars.
                    #==================================================
                    #if "=" not in temp:# and "::" not in temp:
                    #print(temp, tempType)
                    temp, datatypeinfo = processVars(temp.split('\n'), tempType)
                    #print(temp)
                    # Should consider doing something with either datatypeinfo or specifier_info, 06/09/2023
                    for guy in temp: #Write out the newly process vars
                        parenoff2=guy.find(')') + 1
                        guy = guy[:parenoff2] + specifier_info + ' :: ' + guy[parenoff2+1:].lstrip()
                        #print(guy)
                        if f90:
                            new_lynes.append(guy+'\n')
                        else:
                            new_lynes.append(' '*spacing+guy+'\n')
                    # else:
                    #     new_lynes.append(temp)

            #Skip writing lines based on the number of line continuations we already processed.
            if itr == skipLynes[0] and itr > 0:
                if skipLynes[1]>0:
                    skipLynes[0]=skipLynes[0]+1
                    skipLynes[1]=skipLynes[1]-1
            #=======================================
            elif lynes[itr-1].strip() == '' and lynes[itr].strip() == '':
                #Then skip writing two blanks in a row
                pass
            else:
                if lyne[0].isnumeric(): #Then assume this == a goto ref
                    pass
                elif lyne.strip() != '' and '&' == lyne.strip()[0]: #Then assume we are a line continuation
                    lyne=lyne.strip()
                    #====================================================
                    #NOTE: The line below removes indentation from nested lines. Come back later to resolves nested loops
                    lyne = ' ' *spaceamp + lyne[0] + ' ' *indent + lyne[1:].strip() + '\n'
                    #====================================================
                new_lynes.append(lyne)
        else:
            new_lynes.append(lyne)
    return new_lynes

#===========================================================
def processVars( lyne, dtype ):
    newvars = [] # Used to store potentially many vars
    #print(lyne)
    for item in lyne:
        #===================================================
        # Check to see if the line had a comment in it
        # If it did, we capture it in its own temp var and then
        # also store the var(s)
        cmt = ''
        if item.find('!') > -1: #Then this line had comments
            cmt = ' ' + item[item.find('!'):]
            item = item[:item.find('!')]

        if item.find('::') > -1: #Then this line had specifier, get the stuff after that
            datatypeinfo = item[:item.find('::') ].strip()
            item = item[item.find('::') + 2 : ].strip()
        else: # it should of the form "real(4) var" at this point
            datatypeinfo = ''
            if item:
                item = item[item.find(')') + 1 : ].lstrip()

        #===================================================
        # Split the array based on commas. This will cause isseus for vectors,
        # but we handle that here, too.
        linecont = False
        if item: # Python for some reason processes empty strings here, so skip there
            comma_split = item.strip().split(',')
            #print(comma_split, datatypeinfo)

            #Temporary var declars
            newguy = ''
            next = 0 #This var == used for vectors
            # Time to process the var(s)
            for jtr, guy in enumerate( comma_split ):
                if next == 0: #then we don't have a vector to deal with.
                    if guy: # Python for some reason process empty strings here, so skip those
                        if jtr == 0:
                            if guy[ jtr ] == '&': # Remove the & and continue to process
                                newguy = guy[1:].strip()
                            else: 
                                newguy = guy

                        else: #multiple vars in this lyne and we split, so let's keep going
                            newguy = guy
                    #=======================================
                    # Process vectors and get those spaces in the parens
                    leftParens = 0
                    rightParens = 0
                    for let in newguy:
                        if let == '(':
                            leftParens = leftParens + 1
                        elif let == ')':
                            rightParens = rightParens + 1
                    openToClose = leftParens - rightParens #...Assuming there's not
                    if openToClose > 0:
                        #Then we had a vector to declare with more than one dimension
                        next = 1 #So count that
                        newguy = newguy.replace(' ', '') #Removes whitespace
                        #===========================================================================================
                        # Take var up to first paren + add a space + add the dimension + add the comma plus space + add the next dimension
                        #===========================================================================================
                        newguy = newguy[0:newguy.find('(')+1] + ' ' + newguy[newguy.find('(')+1:] + ', ' + comma_split[jtr + next].replace(' ', '')
                        leftParens = 0
                        rightParens = 0
                        for let in newguy:
                            if let == '(':
                                leftParens = leftParens + 1
                            elif let == ')':
                                rightParens = rightParens + 1
                        openToClose = leftParens - rightParens
                        while openToClose > 0:
                            # Then we still have more dimensions to process
                            next = next + 1 # So count that
                            newguy = newguy + ', ' + comma_split[jtr + next].strip() # Keep on adding those dimensions until we get that closing paren
                            leftParens = 0
                            rightParens = 0
                            for let in newguy:
                                if let == '(':
                                    leftParens = leftParens+ 1
                                elif let == ')':
                                    rightParens = rightParens + 1
                            openToClose = leftParens - rightParens
                            if newguy[-1] == '&':
                                linecont = True
                                break # there is a line continuation at the end of the line instead of on the the next line.
                        if not linecont:
                            newguy = newguy[0:-1].rstrip() + ' )' #Now we've found it
                        else:
                            linecont = False
                    elif newguy.find('(') > 0 and newguy.find(')') > 0: #There's only on thing inside the paren
                        if newguy.lstrip()[:len('function ')]== 'function ':
                            tempguy1 = newguy.lstrip()[:len('function ')]
                            tempguy2 = newguy.lstrip()[len('function '):]
                            tempguy2 = tempguy2.replace(' ', '') #Remove all preexisting whitespace and make it our own
                            newguy = tempguy1 + tempguy2
                        else:
                            newguy = newguy.replace(' ','') #Remove all preexisiting whitespace and make it our own
                        newguy = newguy[0:newguy.find('(') + 1]+ ' '+ newguy[newguy.find('(') +1:newguy.find(')')] + ' )'
                    #============================================================================
                    newvars.append( dtype + ' ' + newguy + cmt )
                else: #Skipt the dimenstions that we processed
                    next = next + 1
    return newvars, datatypeinfo