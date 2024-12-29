#!/Users/z1133171/anaconda3/python.app/Contents/MacOS/python
#===========================================================================
# tron.py; fights for the user
# Generate a Fortran common block and its associated initializer(s).
#
# Regardless of the order in the specification, variables in the block will
# be allocated in order of decreasing granularity, Within a given granularity,
# variables will be ordered alphabetically by type and name.
#
# For each input file (e.g. xxx.dcl), two output files will be created. The
# first is xxx.cmn, which contains the common block declaration; the common
# block name will be xxx. The second is xxx_init.f, which contains the code
# to initialize all variables in block xxx. If block_init() is specified in
# the input file, the named initializer(s) will be called after the standard
# initializations have been performed. Multiple block_init()s will be called
# in the order in which they are specified.
#
# If an inout file contains only parameter-type delcarations (i.e., there
# are no declarations that require a common block and its initialization),
# only one file will be written; its name will be of the form xxx.inc.
#===========================================================================

import argparse
import sys
import os
import re
import clu

global spacing
spacing = 6

def processFile( fileName ):
    """
    Process each input file.
    """

    #=======================================================================
    # This is the list of functions that will do something
    functions = [
        'block_init', #custom initializer for block [none]
        'character',  # declaration of character var
        'comment', # comment following file header
        'complex', # declr of cmplex var
        'iinclude', # add an include but only to _init.f file
        'include', # add include to cmn/inc
        'integer', # declare int
        'logical', # declare log
        'raw', # Start reading in raw fortran from the input file (until EOF)
        'real', # declare real
        'structstart',
        'structend',
        'record'
        ]
    #=======================================================================

    #=======================================================================
    # Make sure the file can be open, and, if so, store the line
    try:
        with open( fileName, 'r' ) as inFile: #Inhale the whole file
            lynes = inFile.readlines()
        print( 'Processing: ' + fileName )
    except:
        print( 'Could not open/read: ', fileName)
        print( 'Quitting' )
        sys.exit( 0 )
    #=======================================================================

    #=======================================================================
    # Process each line of the file one at a time. If raw is given, store those lines.
    numLynes = len( lynes )
    lyneNum = 0
    newLynes= [ '' ] * len( lynes )
    raw = [] # Must go last
    skipThis = False
    for itr, lyne in enumerate( lynes ):
        if not skipThis:
            if lyne is not '\n' and lyne[0] is not '#': # Skip blank lines & comments
                flen = lyne.find('(')
                if flen >= 1:
                    func = lyne[0:flen].strip().lower()
                    if func in functions: # We have a registered function
                        newLynes[ lyneNum ] = lyne
                        lyneNum = lyneNum + 1
        if 'raw' in lyne[0:3]:
            raw = lynes[itr+1:]
            skipThis = True
    newLynes = newLynes[0:lyneNum] # So now newLynes is a list containing registered functions
    #=======================================================================

    #=======================================================================
    # Bin the line into their respective function arrays.
    comments = ['']* numLynes 
    c = 0
    declars = ['']* numLynes 
    d = 0
    iinclus = ['']* numLynes 
    ii = 0
    inclus = ['']* numLynes 
    i = 0
    blox = ['']* numLynes 
    b = 0
    structName = ['']* numLynes  #Currently can only accept one struct per file
    sn = 0
    structs = [['' for itr in range(numLynes)] for jtr in range(numLynes)] 
    s = 0
    skip = False
    struxExist = False
    records = ['']*numLynes
    recordsName = ['']*numLynes
    r = 0
    # Now lets split this list into categories for further processing:
    # 1. Comment blocks which are placed directly above what comes next
    # 2. Other items
    #--------------------------------------------------------------------
    for lyne in newLynes:
        lyne = lyne.strip() + '\n'
        flen = lyne.find('(')
        func = lyne[0:flen].lower()
        if 'comment' in func:
            bgn = flen + 2
            #end = lyne.find(')') - 1
            comments[c]=lyne[bgn:-2].strip()#[lparens[0]:rparens[-1]]
            if comments[c][0] == "'":
                comments[c]=comments[c][1:]
            if comments[c][-1] == "'":
                comments[c] = comments[c][ :-1]
            c = c + 1
        elif 'integer' in func or 'logical' in func or 'real' in func or 'complex' in func or 'character' in func or 'record' in func:
            if not skip:
                declars[d]=lyne
                d=d+1
            else:
                structs[sn][s]=lyne
                s =s +1
        elif 'iinclude' in func:
            iinclus[ii]=lyne
            ii + ii + 1
        elif 'include' in func:
            include[i] = lyne
            i=i+1
        elif 'block_init' in func:
            blox[b]=lyne[lyne.find('(') + 1 : lyne.find(')')]
            b = b + 1
        elif 'structstart' in func:
            skip=True
            bgn=flen + 1
            end = lyne.find(')')
            structName[ sn ] = lyne[bgn:end].strip("'").strip( '"' ).lower()
            struxExist = True
        elif 'structend' in func:
            skip = False
            sn = sn + 1
            s = 0 # reset the struct variable counter
        #elif 'record' in func and skip:
        #       bgn = flen + 1
        #       end = lyne.find( ')' )
        #       records[r] = lyne[bgn:end].strip("'").strip('"').lower()
        #       recordsName[r]=structName[sn]
        #       r = r +1
    #---------------------------------------------------------------------
    if skip: # If more than one struct per dcl file gets implemented, something smarter will need to be done here.
        print('Missing structend statement.')
        print('Quitting.')
        sys.exit(0)

    #---------------------------------------------------------------------
    # Clean up
    blox = blox[0:b]
    comments=comments[0:c]
    declars=declars[0:d]
    structName = structName[:sn]
    structs=structs[:sn]
    #records=records[:r]
    #recordsName=recordsName[:r]
    if ii > 1:
        iinclus = sorted( inclus[0:ii])
        # Process includes
        for i in range( len( iinclus ) ):
            iinclus[i] = iinclus[i][iinclus[i].find('(')+1:iinclus[i].find(')')]
    elif ii is 1:
        iinclus = [ iinclus[0][iinclus[0].find('(') + 1:iinclus[0].find(')')]]
    else:
        iinclus=[]
    if i > 1:
        inclus = sorted( inclus[0:i])
        #Process includes
        for j in range(len(inclus)):
            inclus[j]=inclus[j][inclus[j].find('(') + 1: inclus[j].find(')')]
    elif i is 1:
        inclus = [ inclus[0][inclus[0].find('(') + 1:inclus[0].find(')')]]
    else:
        inclus=[]
    #=======================================================================

    # Process vars list
    # Further sorting between parameters and not
    # 1. parameters list
    # 2. variables list
    params = ['']*len(declars)
    p=0
    varList = ['']*len(declars)
    v=0
    noSortName = False
    wasParam = False
    for item in declars:
        if "comment='donotsort'" in item.lower().replace(' ', ''):
            noSortName = True
        if 'parameter=true' in item.replace(' ','').lower(): #then this is a parameter
            params[p] = item
            p=p+1
            wasParam=True
        else:
            varList[v]=item
            v=v+1
    if not wasParam:
        params=[]
    if not noSortName:
        #Sort hese in alphabetical order
        params = sorted( params[0:p] )
        varList = sorted( varList[0:v] )
    #=======================================================================

    #=======================================================================
    # Finally, start to write to file
    fileName = os.path.splitext( os.path.basename( fileName ) )[0] # Get the input filename
    if params and not varList: # Then that means we have only parameters and an .inc file gets created
        #=================================================
        # Process the inc
        # order is
        # 1. Write the comments at the top of the file
        # 2. Write the parameters
        incFile = fileName + '.inc'
        inc = open( incFile, 'w' ) # Create the inc file every single time
        # Go through the chain of inc stuff
        writeComments( inc, comments)
        writeVars( inc, params, isParams=True)
        noSortAll = False
        if struxExist:
            for itr, strux in enumerate( structName ):
                theStrux = []
                record = []
                for jtr, varz in enumerate( structs[ itr ]):
                    if varz:
                        if 'record' in varz.strip().lower()[0:len('record')]:
                            record = varz
                        else:
                            theStrux.append(varz)
                noSortAll = writeStructs(inc, theStrux, strux, record)
        #if records:
        #       writeRecords( inc, records, recordsName)

        #Close the file and exit program
        inc.close()
        clu.processCommons( incFile, noSortAll )

    elif not params and not varList: # Then both lists are empty
        if struxExist:
            incFile = fileName + '.inc'
            inc = open( incFile, 'w' ) # Create cmn file every single time
            noSortAll = False
            for itr, strux in enumerate( structName ):
                theStrux = []
                records = []
                for jtr, varz in enumerate( structs[ itr ] ):
                    if varz:
                        if 'record' in varz.strip().lower()[0:len('record')]:
                            record=varz
                        else:
                            theStrux.append(varz)
                noSortAll = writeStructs(inc, theStrux, strux, record)
            # Close the file and exit program
            inc.close()
            clu.processCommons(incFile, noSortAll)
            #==========================================================
        else:
            print( 'No parameters or variables specified. Nothing to write')

    elif varList:
        #=============================================================
        # Process the cmn file first
        # Order is:
        # 1. Write comments at the top of the file
        # 2. Write the variable-params.
        # 3. Write the variables
        # 4. Write the structs.
        # 5. Write the common blocks
        cmnFile = fileName + '.cmn'
        cmn = open( cmnFile, 'w' ) # Create cmn file every single time
        writeComments( cmn, comments)
        if inclus:
            writeIncludes( cmn, inclus )
        if params:
            writeVars( cmn, params, isParams=True)
        writeVars( cmn, varList )
        noSortAll = False
        if struxExist:
            for itr, strux in enumerate( structName ):
                theStrux = []
                record = []
                for jtr, varz in enumerate( structs[itr] ):
                    if varz:
                        if 'record' in varz.strip().lower()[0:len('record')]:
                            record=varz
                        else:
                            theStrux.append(varz)
                noSortAll=writeStructs(cmn, theStrux, strux, record)
        #if records:
        #       writeRecords( cmn, records, recordsName )
        writeBlks( cmn, varList )
        # Close the file and exit the program
        cmn.close()
        clu.processCommons( cmnFile, noSortAll)
        #===============================================================

        #===============================================================
        # Process the init file
        # Order is:
        # 1. Write comments at the top of the file.
        # 2. Write the variable inits and call() blocks.
        # 3. Write the raw code, if it exists.
        initFile = fileName + '_init.f'
        ini = open( initFile, 'w' ) # Create init file every single time
        writeComments( ini, comments )
        writeInis( ini, varList, cmn, iinclus, blox, raw )
        ini.close()
        clu.processFile( initFile )
        #===============================================================

#=======================================================================
def writeComments( theFile, comments ):
    """
    Write out the comments into the file
    """
    for c in comments:
        if c[-1] == "'":
            c = c[:-1]
        lenText = len(c) + 1
        theFile.writelines( ' '*spacing + '!' + ( '=' *lenText ) + '\n')
        theFile.writelines( ' '*spacing + '!' + c + '\n')
        theFile.writelines( ' '*spacing + '!' + ( '=' *lenText ) + '\n')
    if comments:
        theFile.writelines( '\n' )

#=======================================================================
def writeVars( theFile, varsList, isParams=False):
    """
    Write out the variables into the file.
    """
    fullList = sortVars( varsList ) # Send the var list to be sorted and dict-ted.

    # Cycle through each variable one at a time and process:
    for i, item in enumerate( fullList ):
        lyne2write( item, theFile )
        #=======================================================================
        # If the parameter was set to true, we are going to do this
        if isParams:
            item[ 'init' ] = spaceInitLyne( item[ 'init' ] ) #temp
            #------------------------------------------------------
            if '(' in item['name']:
                item['name']=item['name'][:item['name'].find('(')]
            theFile.writelines( ' '*spacing + 'parameter ( ' + item[ 'name' ] + ' = ' + item['init'] + ' )\n' )
            if i < len( fullList ) - 1:
                theFile.writelines( '\n' )
        #=======================================================================
    theFile.writelines( '\n' ) # Getting a new line in there at the end

def spaceInitLyne(lyne):
    return lyne

#=======================================================================
def sortVars( varsList, from_ini = False, noSortAll = False ):
    """
    Sorts the variable list by type, then size, then name
    """

    lenVars = len( varsList )
    fullList = [ ] #*lenVars
    noSortName = False
    for v in range( lenVars ):
        if "comment='donotsort'" in varsList[v].lower().replace(' ', ''):
            noSortName = True
        if 'skipinit=true' in varsList[v].lower().replace(' ','') and from_ini:
            pass
        else:
            fullList.append( parseParams( varsList[v] ) )

    if noSortName:
        return sorted( fullList, key = lambda x:( x['type'], x['size']))
    elif noSortAll:
        return fullList
    else:
        return sorted( fullList, key = lambda x:( x['type'], x['size'], x['name']))

#=======================================================================
def parseParams( item ):
    """
    Take the item from the vars list and parse what is there.
    """
    item = item[0:-2] # Remove the new line comment and the final paren
    ptype = item[0:item.find('(')] # The variable type( int, real, cmplx, char)
    item = item[ item.find( '(' ) + 1 : ] # Getting the rest of the args
    item = item.split(',')

    #============================================
    # Check if name is actually a vector and missing a paren
    # (i.e. if the var name is a vector, rejoin everything
    # separated by a comma form the split line above inside the parens
    # If there is amissing paren, this rejoins it
    isVector = False
    if item[0].find('(') > -1: # then it's a vecotr
            isVector = True
            lparens = item[0]. count('(')
            rparens = item[0]. count(')')
            while lparens - rparens > 0:
                item[0] = item[0] + ',' + item[1]
                item[1:] = item[2:]
                lparens = item[0].count('(')
                rparens = item[0].count(')')
    name = item[0] # Variable name
    if isVector: # then get vector length
        vec_len = name[name.find('(') + 1 : name.find(')') ]
    #=========================================================

    #=========================================================

    size = 0
    init = 0
    comment = ''
    # If the size, init, and comment params were given, let's store those
    for guy, i in enumerate( item ):
        if 'size=' in i or 'size =' in i:
            val = i.find('=')
            size = i[val+1:]
        elif 'init=' in i or 'init =' in i:
            val = i.find( '=' )
            init = i[val + 1: ]
            if '[' in i[val+1:]: #assume its vector init
                for elems in range(int(vec_len)):
                    if elems > 0:
                        init = init + ", "
                        init = init + item[guy+elems]
        elif 'comment=' in i or 'comment =' in i:
            val = i.find( '=' )
            comment = i[val+1:].strip()
            jtr = 1
            while comment.count("'") % 2 is not 0:
                comment = comment + ', ' + item[guy+jtr]
                jtr = jtr +1
            comment = "! " + comment

    # Set the default var size, if none given
    ptype = ptype.lower().strip()
    if size is 0: #no size was given, need to give the default then.
        if 'complex' in ptype:
            size = 8 # default is 8
        elif 'character' in ptype:
            size = 1 #default is ?
        else:
            size = 4 # Default is 4


    init = str( init ).lower().strip().strip('"').strip("'")
    if ptype == 'character':
        if init == '0':
            init = "''" #Characters get inited to blank strings
        else:
            init = "'" + init + "'"
    elif ptype == 'logical':
        if init == '0':
            init = '.false.'
    elif ptype == 'real':
        if init == '0':
            init = '0.0'
    if "z'" in init[0:2]: # Handles params or vars that are z'ABCD' in form.
        init = init + "'"

    # Send back that info in a dict-style array
    return { 'type': ptype, 'name': name.upper().strip(), 'size': str(size).strip(), 'init': init, 'comment': comment.strip('"').strip("'")}

#=======================================================================
def lyne2write( listItem, theFile, indent=0, isStruct=False):
    """
    Write the variable line to file.
    """
    if isStruct:
        firstHalf = ' '*(spacing+indent) + listItem['type'] + '*' + listItem['size'] + ' '+ listItem['name'].lower()
        if listItem['size'] == '0':
            firstHalf = ' '* ( spacing + indent ) + listItem[ 'type' ] + ' ' + listItem['name'].lower() # If size is zero, don't specify the size
    else:
        firstHalf = ' '*( spacing+indent) + listItem['type'] + '*' + listItem['size'] + ' ' + listItem['name'] # First part of the lyne2write to file
        if listItem['size'] == '0':
            firstHalf = ' '* ( spacing + indent ) + listItem[ 'type' ] + ' ' + listItem['name'] # If size is zero, don't specify the size
    cmtspacer = 1 # Send this string to the spacer method, which will make sure all comments line up on the same column of the file

    # Write this whole thing to the line
    if listItem['comment'] and listItem['comment'][-2] == "'":
        listItem[ 'comment' ] = listItem[ 'comment' ][:-2]
    theFile.writelines( firstHalf + ' '*cmtspacer + listItem[ 'comment' ][0:2] + listItem['comment'][3:] + '\n')
    #=====================================================================

#=======================================================================
def spacer( textString ):
    """
    Spacer dynamically checks what length should be added to a variable/parameter
    so that all comments line up on the same column (col2start)
    """
    lenString = len(textString)
    col2start = 70 # Which column do you want comments to start at for thispart?
    return col2start - lenString

#=======================================================================
def writeStructs( theFile, varsList, name, rekord) :
    """
    This functions similar to write variables, but for structs instead
    """
    options = name.split(',')
    name = options[0].split()
    nosort = False
    if len( options ) is 2:
        nosort = options[ 1] 
        if 'nosort=true' in nosort.lower().replace(' ','').strip():
            nosort=True

    fullList = sortVars( varsList, False, nosort )

    theFile.writelines( ' '*spacig + 'structure /' + name + '/\n' )
    for item in fullList:
        lyne2write( item, theFile, indent = 3, isStruct = True )
    theFile.writelines( ' '*spacing + 'end structure\n' )
    if rekord:
        bgn = len( 'record' ) + 1
        end = rekord.find( ')' )
        rekord = rekord[ bgn : end ].strip("'").strip('"').lower()
        writeRecords( theFile, [rekord], [name])
    theFile.writelines( '\n' )

    return nosort


#=======================================================================
def writeRecords( theFile, varsList, theNames ):
    """
    This functions similar to write variables, but for records instead.
    """
    itsCommon = False
    for itr, recorder in enumerate( varsList ):
        if 'common=true' in recorder.replace(' ', '').strip().lower():
            itsCommon = True
            recorder = recorder[:recorder.find(',')].strip()
        theFile.writelines(' '*spacing+ 'record /' + theNames[itr] + '/ ' + recorder + '\n' )
        if itsCommon:
            theFile.writelines(' '*spacing+ 'common /' + theNames[itr] + '_cmn/ ' + recorder + '\n' )
            itsCommon = False
        theFile.writelines('\n')

#=======================================================================
def writeBlks( theFile, varsList ):
    """
    Write the common block
    """
    fullList = sortVars( varsList )
    for item in fullList:
        if '(' in item['name']:
            item[ 'name' ] = item['name'][0:item['name'].find('(')]
        lyne2write = ' '*spacing + "common /" + theFile.name[0:-4] + "/ " + item['name'] + '\n'
        theFile.writelines(lyne2write)
    theFile.writelines('\n')
#=======================================================================

def writeIncludes( theFile, inclus ):
    # Write out the includes
    for inc in inclus:
        theFile.writelines( ' '*spacing + 'include ' + inc + '\n' )
    theFile.writelines('\n')

#=======================================================================
def writeInis( theFile, varsList, cmnFile, inclus, blox=[], raw=[]):
    """
    Write out the parameters into the _init.f and give them their init files.
    """

    #====================================================================
    # File header part
    theFile.writelines(' '*spacing + 'subroutine ' + theFile.name[0:2] + '\n')  
    theFile.writelines(' '*spacing + 'implicit none\n')
    theFile.writelines('\n')
    #Write out the includes
    theFile.writelines(' '*spacing + "include '" + cmnFile.name + "'\n" )
    for inc in inclus:
        theFile.writelines( ' '*spacing + 'include ' + inc + '\n' )
    theFile.writelines( '\n' )
    #====================================================================
    #====================================================================
    if raw:
        writeRaw( theFile, raw )

    fullList = sortVars( varsList, from_ini = True )
    for item in fullList:
        if '(' in item['name']:
            item['name'] = item['name'][0:item['name'].find('(')]
        lyne2write = ' ' * spacing + item['name'] + ' = ' + item['init']+ '\n'
        theFile.writelines( lyne2write )
    theFile.writelines( '\n' )

    #====================================================================
    # If the block_init, write it out
    if blox:
        for blok in blox:
            theFile.writelines( ' '*spacing + 'call ' + blok.lower() + '\n' )
        theFile.writelines('\n')

    theFile.writelines( ' '*spacing + 'return\n' )
    theFile.writelines( ' '*spacing + 'end\n' )
    theFile.writelines( '\n' )

#========================================================================
def writeRaw( theFile, raw ):
    """
    Write out the raw() text to the _init.f file.
    """
    lenRaw = len( raw )
    for lyne in raw:
        lyne2write = ' '*spacing + lyne
        theFile.writelines( lyne2write )
    theFile.writelines( '\n' )

#========================================================================
# Main
#========================================================================
if __name__ == '__main__':
    descript = '''
====================================== block_init =======================================
Usage:
block_init( 'function' ), where function = a subroutine call where vars from the cmn file are declared.
-----------------------------------------------------------------------------------------

=====================character, complex, integer, logical, real =========================
Usage:
integer( name, [size, parameter, init, comment])

name = the name of the var/param -- REQUIRED
size =  int size of the var (default is 4, 8, or 1 for a string)
parameter = bool, default is false
init = initial value (0 or false is default)
comment = in line comment
skipinit = will skip init to zero, etc
-----------------------------------------------------------------------------------------

====================================== iinclude =======================================
Usage:
iinclude( 'file2include' ), includes a cmn file in the _init.f
-----------------------------------------------------------------------------------------

====================================== include =======================================
Usage:
include( 'file2include' ), includes a cmn file in the .cmn
-----------------------------------------------------------------------------------------

====================================== raw =======================================
Usage:
raw()
Everythin in the line below gets copied verbatim in the _init.f file. This must come last on the .dcl.
-----------------------------------------------------------------------------------------

====================================== structstart/structend =======================================
Usage:
structstart( 'structname '), where the 'structname' = is the name of the structure block
structend(), end of the struct block

NOTE: You cannot have a startstruct without a structend. It will quit out with a warning message.
-----------------------------------------------------------------------------------------

'''
    parser = argparse.ArgumentParser( formatter_class = argparse.RawDescriptionHelpFormatter, description = descript )
    parser.add_argument( 'filename', action = 'store', nargs = '+', help='Path(s) to input file(s)' )
    argz = parser.parse_args()
    fileList = argz.filename

    #Process each file one at a time
    for f in fileList:
        processFile( f )