from donotformat import doNotFormatCheck
import re

#Variable declartion types, referenced in multiple functions
data_types = [
    'integer',
    'real',
    'complex',
    'character',
    'logical'
    ]

#===========================================================
def processParens( lynes ): 
    new_lynes = []
    #===============================================================
    # Process each line of the file one at a time. If raw == given, store those lines.
    #==============
    mathops = ['+','-', '/', '*', ',','(', '.', '=', ]

    temp=''
    diff_parens=0
    format_found=False
    for lyne in lynes:
        if format_found and diff_parens == 0:
            format_found = False # closed the format statement this line

        cmt_index = lyne.find("!")
        if 'format' in lyne[:cmt_index] or diff_parens != 0:
            lparens = lyne.count('(')
            rparens = lyne.count(')')
            diff_parens = diff_parens + lparens - rparens

        if 'format' in lyne[:cmt_index]:
            format_found=True # This line still has a format statement

        if not doNotFormatCheck( lyne ) and diff_parens == 0 and lyne.strip():
            if '#' not in lyne.strip()[0]: # Don't modify preprocessor directives
                #=====================
                # change math symbols: <=, <, >, >=, /=, ==
                temp = ''
                skip = False
                totalSkip = False
                skipeqs = False
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        totalSkip=True
                    elif char == '"' or char == "'":
                        skip = not skip

                    if not skip and not totalSkip and not skipeqs:
                        if char == '<' and not format_found:
                            if lyne[jtr+1] == '=':
                                char = '.le.'
                                skipeqs = True
                            else:
                                char = '.lt.'
                        elif char == '>' and not format_found:
                            if lyne[jtr+1] == '=':
                                char = '.ge.'
                                skipeqs = True
                            else:
                                char = '.gt.'
                        elif char == '/' and lyne[jtr+1] == '=':
                            char = '.ne.'
                            skipeqs = True
                        elif char == '=' and not skipeqs:
                            if lyne[jtr-1] == '<' or lyne[jtr-1] == '>' or lyne[jtr-1] == '/' or lyne[jtr-1] == '=':
                                pass
                            elif lyne[jtr+1] == '=':
                                char = '.eq.'
                                skipeqs = True
                    elif skipeqs:
                        char = ''
                        skipeqs = False
                    temp += char

                lyne = temp
                #================================
                # Process paren (
                temp = ''
                skip = False
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        temp += lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp += char
                    else:
                        if char == '(' and lyne[jtr+1] != ' ':
                            temp += char + ' '
                        else:
                            temp += char
                lyne = temp
                #==============================
                # Process paren (, part2
                temp = ''
                skip = False
                for jtr, char in enumerate(lyne):
                    if char =="!":
                        temp +=lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp += char
                    else:
                        if char == '(' and lyne[jtr-3] == ' ' and lyne[jtr-2] == 'i' and lyne[jtr-1] == 'f':
                            temp += ' ' + char
                        else:
                            temp += char
                lyne = temp
                #================================
                # Process paren )
                temp = ''
                skip = False
                for jtr, char in enumerate( lyne ):
                    if char == "!": #If the current character is a comment, store til the end of the line and go to next line. 
                        temp = temp + lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp = temp + char
                    else:
                        if char == ')' and lyne[jtr-1] != ' ':
                            temp = temp + ' ' + char
                        else:
                            temp = temp + char
                lyne = temp
                #==============================
                # Process paren ), part2
                skip = False
                for jtr, char in enumerate(lyne):
                    if char =="!":
                        temp = temp + lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp = temp + char
                    else:
                        if char == ')' and lyne[jtr-2] == '(': #Not sure why I wrote this..
                            lyne=lyne[:jtr-1]+lyne[jtr:]
                            skip = True
                        else:
                            pass
                #==============================
                # Process paren ), part3
                skip = False
                temp = ''
                for jtr, char in enumerate(lyne):
                    if char =="!":
                        temp = temp + lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp = temp + char
                    else:
                        if char == ')' and jtr+1 < len(lyne) and lyne[jtr+1] and lyne[jtr+1] not in ('\n', ' ', '%'):
                            temp = temp + char + ' '
                        else:
                            temp = temp + char
                lyne = temp
                #================================
                # Process commas ,
                temp = ''
                skip = False
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        temp += lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp = temp + char
                    else:
                        if char == ',' and lyne[jtr+1] != ' ':
                            temp = temp + char + ' '
                        else:
                            temp = temp + char
                lyne = temp
                #================================
                # Process commas , 2
                temp = ''
                skip = False
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        temp += lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp = temp + char
                    else:
                        if char == ',' and lyne[jtr-1] == ' ':
                            temp = temp[:-1] + char
                        else:
                            temp = temp + char
                lyne = temp
                #================================
                # Process colons :
                temp = ''
                skip = False
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        temp += lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip

                    if skip:
                        temp += char
                    else:
                        if char == ':' and lyne[jtr+1] != ':' and lyne[ jtr-1 ] != ':':
                            if lyne[ jtr + 1 ] != ' ' and lyne[ jtr - 1] != ' ': #a=b
                                temp += ' ' + char + ' '
                            elif lyne[jtr+1] != ' ' and lyne[jtr-1] == ' ': #maybe a =b
                                temp += char + ' '
                            elif lyne[jtr+1] == ' ' and lyne[ jtr - 1 ] != ' ': #could be a= b
                                temp += ' ' + char
                            else: #could be a = b
                                temp += char
                        elif char == ':' and lyne[jtr+1] == ':' and lyne[jtr-1] != ':':
                            if lyne[jtr-1] != ' ': #a=b
                                temp += ' '+char
                            else: #could be a = b
                                temp += char
                        elif char == ':' and lyne[jtr+1] != ':' and lyne[jtr-1] == ':':
                            if lyne[jtr+1] != ' ': #a=b
                                temp += char + ' '
                            else: #could be a = b
                                temp += char
                        else:
                            temp += char
                lyne = temp
                #================================
                # Process equals =
                temp = ''
                skip = False
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        temp += lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp += char
                    else:
                        if char == '=':
                            if lyne[ jtr+1 ] != ' ' and lyne[jtr-1] != ' ': #a=b
                                temp += ' ' + char + ' '
                            elif lyne[jtr+1] != ' ' and lyne[jtr-1] == ' ': #maybe a =b
                                temp+= char + ' '
                            elif lyne[jtr+1] == ' ' and lyne[jtr-1] != ' ': #maybe a= b
                                temp += ' ' + char
                            else: #could be a = b
                                temp += char
                        else:
                            temp += char
                lyne = temp
                #================================
                # Process plus sign +
                temp = ''
                skip = False
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        temp += lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp += char
                    else:
                        if char == '+':
                            if lyne[ jtr+1 ] != ' ' and lyne[jtr-1] != ' ': #so its (thing)+(thing)
                                #print('before', lyne[:-1], lyne[jtr-2])
                                if (lyne[jtr-1] == 'e' or lyne[jtr-1] == 'd'): #so its d+(thing)
                                    if lyne[jtr-2].isnumeric() and lyne[jtr+1].isnumeric(): #so its (number)d+(number)
                                        temp += char #leave it alone
                                    else: #so its (thing)d+(thing)
                                        temp+= ' ' + char + ' '
                                else: #so its (thing)+(thing)
                                    if lyne[jtr-2] == '=': #so its =+(thing)
                                        temp += ' ' + char
                                    else: #so its (thing)+(thing)
                                        temp+= ' ' + char + ' '
                                        #temp+= ' ' + char + ' '
                                        # if lyne[jtr+1].isnumeric(): # 0d-a
                                        #     #if (lyne[jtr-1] == 'e' or lyne[jtr-1] == 'd') and not lyne[jtr-2].isnumeric()
                                        #     #print(lyne)
                                        #     pass #temp+= ' ' + char + ' ' # 0d - a or 0d - 0
                                        # else:
                                        #temp+= ' ' + char + ' ' # 0d - a or 0d - 0
                            elif lyne[jtr+1] != ' ': #so its (thing) +(thing)
                                if lyne[jtr-2] == '=': #so its = +(thing)
                                    temp += char
                                else: #so its (thing) +(thing)
                                    temp+= char + ' '
                            elif lyne[jtr-1] != ' ': #so its (thing)+ (thing)
                                temp += ' ' + char
                            else: #so its (thing) + (thing)
                                temp += char
                        else:
                            temp += char
                lyne = temp
                #================================
                # Process minus sign -
                temp = ''
                skip = False
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        temp += lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp += char
                    else:
                        if char == '-':
                            if lyne[ jtr+1 ] != ' ' and lyne[jtr-1] != ' ': #so its (thing)+(thing)
                                #print('before', lyne[:-1], lyne[jtr-2])
                                if (lyne[jtr-1] == 'e' or lyne[jtr-1] == 'd'): #so its d+(thing)
                                    if lyne[jtr-2].isnumeric() and lyne[jtr+1].isnumeric(): #so its (number)d+(number)
                                        temp += char #leave it alone
                                    else: #so its (thing)d+(thing)
                                        temp+= ' ' + char + ' '
                                else: #so its (thing)+(thing)
                                    if lyne[jtr-2] == '=': #so its =+(thing)
                                        temp += ' ' + char
                                    else: #so its (thing)+(thing)
                                        temp+= ' ' + char + ' '
                                        #temp+= ' ' + char + ' '
                                        # if lyne[jtr+1].isnumeric(): # 0d-a
                                        #     #if (lyne[jtr-1] == 'e' or lyne[jtr-1] == 'd') and not lyne[jtr-2].isnumeric()
                                        #     #print(lyne)
                                        #     pass #temp+= ' ' + char + ' ' # 0d - a or 0d - 0
                                        # else:
                                        #temp+= ' ' + char + ' ' # 0d - a or 0d - 0
                            elif lyne[jtr+1] != ' ': #so its (thing) +(thing)
                                if lyne[jtr-2] == '=': #so its = +(thing)
                                    temp += char
                                else: #so its (thing) +(thing)
                                    temp+= char + ' '
                            elif lyne[jtr-1] != ' ': #so its (thing)+ (thing)
                                temp += ' ' + char
                            else: #so its (thing) + (thing)
                                temp += char
                        else:
                            temp += char
                lyne = temp
                #================================
                # Process fwd slash /
                temp = ''
                skip = False
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        temp += lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp += char
                    else:
                        if char == '/':
                            if lyne[ jtr+1 ] != ' ' and lyne[jtr-1] != ' ':
                                temp += ' ' + char + ' '
                            elif lyne[ jtr+1 ] != ' ' and lyne[jtr-1] == ' ':
                                temp+= char + ' '
                            elif lyne[ jtr+1 ] == ' ' and lyne[jtr-1] != ' ':
                                temp += ' ' + char
                            else:
                                temp += char
                        else:
                            temp += char
                lyne = temp

                #================================
                # Process asterisk *
                temp = ''
                skip = False
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        temp += lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp += char
                    else:
                        if char == '*' and lyne[jtr+1] != '*' and lyne[jtr-1] != '*' and not any(lyne[jtr-4:jtr] in x for x in data_types):
                            if lyne[ jtr + 1] != ' ' and lyne[jtr-1] != ' ':
                                temp+=' ' + char + ' '
                            elif lyne[jtr+1] != ' ':
                                temp += char + ' '
                            else:
                                temp += ' ' + char
                            if temp[-2] == ' ' and temp[-3] == ' ':
                                temp=temp[:-2] + temp[-1]
                        else:
                            temp += char
                lyne = temp
                #================================
                # Process asterisk *, part 2
                skip = False
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        temp += lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp += char
                    else:
                        if char == '*' and lyne[jtr+1] != '*' and lyne[jtr-1] != '*' and not any(lyne[jtr-4:jtr] in x for x in data_types):
                            if lyne[jtr+2] == ',':
                                lyne = lyne[:jtr+1]+lyne[jtr+2:]
                                skip=True
                        else:
                            pass
                #================================
                # Process exponential **
                skip = False
                temp = ''
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        temp += lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp += char
                    else:
                        if char == '*' and lyne[jtr+1] == '*':
                            if lyne[jtr+2] != ' ' and lyne[jtr-1] != ' ':
                                temp += ' ' + ( char + lyne[ jtr + 1 ] ) + ' '
                            elif lyne[jtr+2] != ' ' and lyne[jtr-1] == ' ':
                                temp += ( char + lyne[jtr+1] ) + ' '
                            elif lyne[jtr+2] == ' ' and lyne[jtr-1] != ' ':
                                temp += ' ' + ( char + lyne[jtr+1] )
                            else:
                                temp += char + lyne[jtr+1]
                        elif char == '*' and lyne[jtr-1] == '*':
                            pass
                        else:
                            temp+=char
                lyne = temp
                #================================
                # Process spaces ' '
                skip = False
                temp = ''
                for jtr, char in enumerate( lyne ):
                    if char == "!":
                        temp += lyne[jtr:]
                        break
                    elif char == '"' or char == "'":
                        skip = not skip
                    if skip:
                        temp += char
                    else:
                        if char == ' ':
                            if lyne[jtr-1] == ' ':
                                pass
                            else:
                                temp += char
                        else:
                            temp+=char
                lyne = temp
                #========================== -, part 2 I believe this handles = - 0.213 to = -0.213 for example
                skip = False
                mlocs = re.finditer('-', lyne)
                skipElem = 0
                temp = lyne
                for loc in mlocs:
                    jtr = loc.start()
                    if jtr < lyne.find('!') and lyne.find('!') > -1 or lyne.lstrip()[0] == '!':
                        temp = lyne
                        pass
                    else:
                        if any( lyne[jtr-2] in x for x in mathops ) or ( lyne.strip()[0] == '&' and lyne.lstrip()[1:].lstrip()[0] == '-'):
                            if lyne[jtr+1] == ' ':
                                if not temp:
                                    temp = lyne[ : jtr+1] + lyne[jtr+2:]
                                    skipElem = skipElem + 1
                                else:
                                    temp = temp[: jtr+1 - skipElem] + temp[jtr+2-skipElem:]
                                    skipElem = skipElem + 1
                        elif ( lyne[ jtr-2] == 'e' or lyne[jtr-2] == 'E' ) and lyne[jtr-3] == '.':
                            if lyne[jtr+1] == ' ' and lyne[jtr-1] == ' ':
                                temp = lyne[:jtr-2-skipElem] + lyne[jtr-skipElem] - temp[:jtr+1-skipElem] + temp[jtr+2-skipElem:]
                                skipElem = skipElem + 1
                        elif ( lyne[ jtr-2] == 'd' or lyne[jtr-2] == 'D' ) and lyne[jtr-3] == '.':
                            if lyne[jtr+1] == ' ' and lyne[jtr-1] == ' ':
                                temp = lyne[:jtr-2-skipElem] + lyne[jtr-skipElem] - temp[:jtr+1-skipElem] + temp[jtr+2-skipElem:]
                                skipElem = skipElem + 1
                        else:
                            temp = lyne
                lyne = temp
        #=============================
        if ('//' in lyne) or ('/ /' in lyne):
            lyne = lyne.replace('/ /', '//')

        new_lynes.append(lyne)
    return new_lynes
