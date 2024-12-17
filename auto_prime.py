#!/Users/z1133171/anaconda3/python.app/Contents/MacOS/python
#==========================================================
# auto_prime.py will auto-generate the init_prime.f file based on the "include" statements
# comment
from subprocess import PIPE, run
import argparse
import sys
import os
import re

spacing = 6 # First 6 columns go unused in most cases
spaceamp = 5
indent = 3 #Default indentation
lastcol = 131 # last usable column in Fortran

def out( command ):
    # Function: out
    # Purpose: Interact with terminal/
    #-----Inputs
    # Command: Any command you would give to the terminal in the format of a string
    #----------Outputs
    #Result: An object that will return the text of the terminal's output message. To retrieve you will need to specify if
    # you want the standard out out std err by usinf .stdout or .stderr
    #===================================================================
    result = run( command, stdout=PIPE, stderr= PIPE, universal_newlines=True, shell=True)
    result.stdout = result.stdout.splitlines()
    result.stderr = result.stderr.splitlines()
    return result # If you want to store the results you'll need the .stdout after you call this

#====================================================================
#====================================================================
#====================================================================

def writePrime( includeList ):
    lynes = []
    lynes.append( spacing*' ' + 'subroutine init_prime\n' )
    lynes.append( '\n' )
    lynes.append( spacing*' ' + '!============================\n')
    lynes.append( spacing*' ' + '! Common block initialization\n')
    lynes.append( spacing*' ' + '!============================\n')
    if listy in includeList:
        lynes.append( spacing*' ' + 'call ' + listy[:-4] + '_init\n' )
    lynes.append( '\n' )
    lynes.append( spacing*' ' + 'return\n' )
    lynes.append( spacing*' ' + 'end\n' )
    #==================================================================
    newfile = open( 'INCLUDE/init_prime.f', 'w' ) #Will this folder structure
    newfile.writelines(lynes)
    newfile.close()
    #==================================================================

#====================================================================
#====================================================================
#====================================================================
def globetrot( fileName, includeList ):
    noWrite = False
    #================================================================
    # Make sure the file can be open, and, if so, store the lines
    print(fileName)
    try:
        with open( fileName, 'r' ) as inFile: #Inhale the whole file
            lynes = inFile.readlines()
    except:
        print(sys.error)
        print( 'Could not open/read: ', fileName)
        print( 'Quitting' )
        sys.exit(0)
    localList = []
    found = False
    process = True
    for itr, lyne in enumerate(lynes):
        if lyne.lstrip() is not '!':
            if process:
                if lyne.lstrip()[:7] == 'include':
                    found = True
                if found and lyne.lstrip()[:7] != 'include' and lynes[itr+1].lstrip()[:7] != 'include': #once found, and no longer finding includes, get lost
                    process = False
                if found and lyne.lstrip() and lyne.strip()[0] is not '!':
                    temp = lyne.strip()
                    temp = temp[temp.find(' '):].lstrip()
                    localList.append(temp)
    # Process includes again, by getting just the names
    for itr, inclu in enumerate( localList ):
        localList[itr] = inclu[1:]
        localList[itr] = localList[itr][:localList[itr].find( "'" ) ]
        includeList.append(localList[itr])

#=============================================================
#Main
#=============================================================
if __name__ == '__main__':
    #Directory listings
    dirList = [
        'DECLARE',
    ]
    fileList = []
    for fzdir in dirList:
        listing = out( 'ls ' + fzdir ).stdout
        for item in listing:
            if '.f' == item[-2:]:
                fileList.append( fzdir + '/' + item )

    #Process each file one at a time
    includeList = []
    for f in fileList:
        globetrot( f, includeList )
    includeList.sort()
    tempList = []
    for itr, listy in enumerate( includeList ):
        if '.cmn' == listy[-4:]:
            if itr >= 1 and includeList[ itr ] != includeList[ itr - 1 ]:
                tempList.append(listy)
            elif itr == 0:
                tempList.append(listy)
    includeList = tempList

    writePrime( includeList )
    print('init_prime.f generated')