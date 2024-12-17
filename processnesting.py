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
    'logical',
    'double precision'
    ]


#===========================================================
def processNesting(lynes, f90):
    """
    Formats indentation of if, do, etc statements
    """
    new_lynes = []
    #=======================================================
    # Process each line of the file one at a time. If raw == given, store those lines.
    indenter = 0
    skip = False
    caller = False
    callerIndent=0
    diff_parens=0
    first_case=False
    endsub =False
    for itr, lyne in enumerate(lynes):
        temp = ''
        stop = False
        btr =0 
        weird_indent = False
        if 'format(' in lyne:
            lparens = lyne.count( '(' )
            rparens = lyne.count( ')' )
            diff_parens=diff_parens+lparens-rparens
        elif diff_parens != 0:
            lparens = lyne.count( '(' )
            rparens = lyne.count( ')' )
            diff_parens=diff_parens+lparens-rparens

        if not doNotFormatCheck(lyne):
            for jtr, char in enumerate(lyne):
                if stop:
                    continue
                elif char.isalpha():
                    btr = jtr
                    stop = True
                    
            if lyne.replace(' ', '')[0].isnumeric() and ('if (' in lyne[btr:btr+4] or 'do ' in lyne[btr:btr+3]):
                temp = lyne[:btr].strip()
                lyne = lyne[btr:].lstrip()
                indenter += 1
                skip = True
            elif lyne.replace(' ', '')[0].isnumeric() and 'enddo' in lyne[btr:btr+5]:
                temp = lyne[:btr].strip()
                lyne = lyne[btr:].lstrip()
                indenter -= 1
            elif lyne.strip().startswith('if (') and 'else' not in lyne.strip()[0:4]:
                indenter += 1
                skip = True
            elif lyne.strip().startswith('endif'):
                indenter -= 1
            elif lyne.strip().startswith('contains'):
                indenter += 1
                skip = True
            elif lyne.strip().startswith('subroutine'):
                indenter += 1
                skip = True
            elif lyne.strip().startswith('program'):
                indenter += 1
                skip = True
            elif lyne.strip().startswith('where'):
                indenter += 1
                skip = True
            elif lyne.strip().startswith('function') or any(lyne.strip().startswith(item + ' function') for item in data_types):
                indenter += 1
                skip = True
            elif lyne.strip().startswith('recursive function'):
                indenter += 1
                skip = True
            elif lyne.strip().startswith('endsubroutine'):
                indenter -= 1
                endsub = True
            elif lyne.strip().startswith('do ') and not lyne[3].isdigit():
                indenter += 1
                skip = True
            elif ': do' in lyne and not lyne[lyne.find(': do')-1] == ':':
                if not lyne.strip().startswith('!'):
                    templyne = lyne.lstrip().replace(' : do', ': do', 1)
                    lyne = templyne
                    indenter += 1
                    skip = True
            elif lyne.strip().startswith('enddo'):
                indenter -= 1
            elif lyne.strip().startswith('type ') and lyne[5].isalpha():
                indenter += 1
                skip = True
            elif lyne.strip().startswith('type, ') and lyne[6].isalpha():
                indenter += 1
                skip = True
            elif lyne.strip().startswith('module ') and lyne.strip()[len('module ')+1].isalpha():
                indenter += 1
                skip = True
            elif 'interface ' in lyne.strip()[0:len('interface ')] and lyne.strip()[len('interface ')+1].isalpha() or lyne.strip().startswith('interface'):
                indenter += 1
                skip = True
            elif lyne.strip().startswith('select case'):
                indenter += 1
                skip = True
            elif lyne.strip().startswith('case'):
                if not first_case:
                    first_case = True
                    indenter += 1
                elif first_case:
                    weird_indent = True
                skip = True
            elif lyne.strip().startswith('endselect') or lyne.strip().startswith('end select'):
                indenter -= 2
            elif lyne.strip().startswith('end type'):
                indenter -= 1
            elif lyne.strip().startswith('end module'):
                indenter -= 1
            elif lyne.strip().startswith('end interface') or lyne.strip().startswith('endinterface'):
                indenter -= 1
            elif lyne.strip().startswith('end function'):
                indenter -= 1
            elif lyne.strip().startswith('end program'):
                indenter -= 1
            elif lyne.strip() == 'end':
                indenter -= 1
            elif lyne.strip().startswith('end subroutine') or lyne.strip().startswith('endsubroutine'):
                indenter -= 1
            elif lyne.strip().startswith('structure ') and lyne.strip()[len('structure ')] == '/':
                indenter += 1
                skip = True
            elif lyne.strip().startswith('end structure'):
                indenter -= 1
            elif lyne.strip().startswith('end where') or lyne.strip().startswith('endwhere'):
                indenter -= 1
            if 'else' in lyne.lstrip()[:4] or 'elseif' in lyne.strip()[:6] or 'elsewhere' in lyne.strip()[:6]:
                skip = True
            if endsub:
                if lyne.strip():
                    if 'endprogram' == lyne.strip()[:len('endprogram')]:
                        endsub = False
                        indenter -= 1
            lyne=lyne.lstrip() #Remove that whitespace and start over
            if lyne:
                # print(indenter)
                # print(lyne)
                if lyne[0] == '!': #Get comments out of the way first
                    if f90:
                        lyne = ' '*indent*indenter+lyne
                    else:
                        lyne = ' '*spacing + ' '*indent*indenter+lyne
                elif lyne[0] == '&':
                    if skip:
                        if weird_indent:
                            lyne=' '*spaceamp + lyne[0] + ' '*indent *(indenter-2)+lyne[1:].lstrip()
                            weird_indent = False
                        else:
                            lyne=' '*spaceamp+lyne[0] + ' '*indent*(indenter-1)+lyne[1:].lstrip()
                        skip=False
                    else:
                        checkindent=0
                        if indenter == 0:
                            checkindent=1
                        if lynes[itr-1].lstrip()[:5] == 'call ':
                            caller=True
                            if indenter != 0:
                                callerIndent=1
                        if caller and lyne[1:].lstrip()[0]==')':
                            caller=False
                        lyne = ' ' *spaceamp + lyne[0] + ' '*indent*indenter + ' '*indent*checkindent + ' '*indent*callerIndent + lyne[1:].lstrip()
                        if not caller:
                            callerIndent=0
                elif lyne[0].isnumeric():
                    flag=True
                    ktr=0
                    for jtr, char in enumerate(lyne):
                        if flag:
                            if char.isnumeric():
                                pass
                            else:
                                flag = False
                                ktr = jtr
                    if f90:
                        lyne=' '*indent*indenter + lyne.lstrip()
                    else:
                        lyne=lyne[:ktr] + ' ' *(6-ktr)+ ' '*indent*indenter + lyne[ktr:].lstrip()
                else:
                    if skip:
                        if f90:
                            lyne=' '*indent*(indenter-1) + lyne
                        else:
                            lyne=' '*spaceamp + ' '+ ' '*indent*(indenter-1) + lyne
                        skip = False
                    else:
                        if f90:
                            lyne = ' '*indent *indenter +lyne
                        else:
                            lyne = ' '*spacing + ' '*indent *indenter +lyne
            else:
                lyne='\n'
            if temp != '':
                lyne = temp + lyne[len(temp):]
            new_lynes.append(lyne)
        else:
            new_lynes.append(lyne)
    return new_lynes