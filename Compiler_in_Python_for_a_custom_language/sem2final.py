'''
Created on Feb 09, 2012

@author: Aravindh Sampathkumar and Sakthi Gurumaharaj
 
 
'''

import re
import time
from collections import deque

from Codes import *
from Data import *
progname = ""
procname = ""
locsymbtab = []
glosymbtab = []
global in_proc_flag 
in_proc_flag = False
dupflag = False
global semantic_stack
semantic_stack = []
global inp_stack
inp_stack = []
global valref
valref = ""
global looplist
looplist = []
global looplist1
looplist1 = []
global intintermedctr
intintermedctr = 1
global realintermedctr
realintermedctr = 1
global r
r = ""
global boointermedctr
boointermedctr = 1
global loopintermedctr
loopintermedctr = 1
global outvarctr
outvarctr = 1
global retlabelctr
retlabelctr = 1
global tuples
tuples = []
global reg 
reg = [" "," "," "]
def lexicalanalysis(inpline):
    isymb = ""
    colcount = 0
    outline = ""
    outsrc = []
    istring = ""
    rowcount = 1
    mlcommentflag = False
    length = len(inpline)
    isymb = inpline[0]
    while(colcount < length):
        isymb = inpline[colcount]
        if isymb == '"' and mlcommentflag == False: 
            istring = isymb
            colcount += 1
            isymb = inpline[colcount]
            while (isymb != '"' and colcount != length):
                isymb = inpline[colcount]
                istring += inpline[colcount]
                colcount += 1
            #print "Token :  " + istring + "  Code :   " + str(codes["String"])
            outline += str(codes["String"]) + " "
            outsrc.append(istring)
            
        elif isymb == "/" and mlcommentflag == False:
            colcount += 1
            istring = isymb
            isymb = inpline[colcount]
            if (isymb == "/"):
                while (colcount < length):
                    istring += inpline[colcount]
                    colcount += 1 
                #print "Single line Comment :  " + istring 
            elif (isymb == "*"):
                mlcommentflag = True
                istring += isymb
                colcount += 1
                isymb = inpline[colcount]
                while(isymb != "*" and colcount < length-1):
                    istring += inpline[colcount]
                    colcount += 1
                    isymb = inpline[colcount]
                if (isymb == "*" and inpline[colcount+1] == "/"):
                    istring += inpline[colcount] + inpline[colcount+1]
                    colcount += 2
                    mlcommentflag = False
                colcount = length
                #print "Multi line comment :   " + istring
            else:
                #print "Token :  " + istring + "  Code : " + str(codes[istring])
                outline += str(codes[istring]) + " "
                outsrc.append(istring)
                   
        elif mlcommentflag == True:
            istring = isymb
            while(isymb != "*" and colcount < length-1):
                istring += inpline[colcount]
                colcount += 1
                isymb = inpline[colcount]
            if (isymb == "*" and inpline[colcount+1] == "/"):
                istring += inpline[colcount] + inpline[colcount+1]
                colcount += 2
                mlcommentflag = False  
            colcount = length
            #print "Multi line comment :   " + istring
        elif (colcount < length-1 and isymb == "#" and inpline[colcount+1] == "#" and mlcommentflag == False):
            colcount += 1
            istring += isymb + inpline[colcount]
            colcount += 1
            while(colcount < length-1 and inpline[colcount] != "#" and inpline[colcount+1] != "#"):
                istring += inpline[colcount]
                colcount += 1
            istring += inpline[colcount] + inpline[colcount+1] + inpline[colcount+2]
            colcount += 3
            if(istring[-2:] != "##"):
                print "Invalid Flag  " + istring + "  - Missing end of flag  "
            else:
                istring = istring[2:-2]
                pattern=re.compile(r"""(?P<flags>[+|-][0-9]+)""",re.VERBOSE)
                for t in re.finditer(pattern,istring):
                    if t.group('flags') :
                        i=(t.group('flags'))
                        #print i[1:]
                        if (i[0] == "+" and i[1:] in flags):
                            switch = "on"
                            flags[i[1:]] = switch
                            #print "The Flag  " + i[1:] + "  is turned on" 
                        elif (i[0] == "-" and i[1:] in flags):
                            switch = "off"
                            flags[i[1:]] = switch
                            #print "The Flag  " + i[1:] + "  is turned off" 
                        else:
                            print "Invalid Flag switch detected "
                
        elif (symbols.__contains__(isymb)) and mlcommentflag == False:
            istring = isymb
            if (isymb == "!" and inpline[colcount+1] == "="):
                istring += inpline[colcount+1]
                colcount += 2
            elif (isymb == "<" and inpline[colcount+1] == "="):
                istring += inpline[colcount+1]
                colcount += 2
            elif (isymb == ">" and inpline[colcount+1] == "="):
                istring += inpline[colcount+1]
                colcount += 2
            elif (isymb == "<" and inpline[colcount+1] == "-"):
                istring += inpline[colcount+1]
                colcount += 2
            elif (isymb == ":" and inpline[colcount+1] == ":"):
                istring += inpline[colcount+1]
                colcount += 2
            elif ((isymb == "-") and digits.__contains__(inpline[colcount+1])):
                colcount += 1
                while(colcount < length and (digits.__contains__(inpline[colcount]) or inpline[colcount] == "." )):
                    istring += inpline[colcount]
                    colcount +=1
                if(istring.find(".") == -1):
                    if(len(istring) > 10):
                        print "Invalid Integer value  "  + istring + "  exceeds the length limit of 9 "
                    else:
                        #print "Token :  " + istring + "  Code : " + str(codes["Integer"]) 
                        outline += str(codes["Integer"]) + " "
                        outsrc.append(istring)
                else:
                    if(len(istring) > 9):
                        print "Invalid Real number value  "  + istring + "  exceeds the length limit of 7 "
                    else:
                        #print "Token :  " + istring + "  Code : " + str(codes["Real"])  
                        outline += str(codes["Real"]) + " "
                        outsrc.append(istring)
            else:
                colcount += 1
            if len(istring) == 1:
                #print "Token :  " + istring + "  Code : " + str(codes[istring])
                outline += str(codes[istring]) + " "
                outsrc.append(istring)
            else:
                if(digits.__contains__(istring[1]) != True):
                    #print "Token :  " + istring + "  Code : " + str(codes[istring])
                    outline += str(codes[istring]) + " "
                    outsrc.append(istring)
                         
        elif(isymb == "=" and inpline[colcount+1] == "=" and mlcommentflag == False):
            istring = isymb + inpline[colcount+1]
            #print "Token :  " + istring + "  Code : " + str(codes[istring])
            outline += str(codes[istring]) + " "
            outsrc.append(istring)
            colcount += 2
        elif(ualpha.__contains__(isymb) and mlcommentflag == False):
            istring = isymb
            colcount += 1
            while(colcount < length and ualpha.__contains__(inpline[colcount])):
                istring += inpline[colcount]
                colcount += 1
            if(keywords.__contains__(istring)):
                #print "Token :  " + istring + "  Code : " + str(codes[istring])
                outline += str(codes[istring]) + " "
                outsrc.append(istring)
            else:
                print "Invalid Keyword :   " + istring

        elif(lalpha.__contains__(isymb)) and mlcommentflag == False:
            istring = isymb
            colcount += 1
            isymb = inpline[colcount]
            while(colcount < length and (lalpha.__contains__(isymb) or ualpha.__contains__(isymb) or digits.__contains__(isymb) or isymb == "_") ):
                istring += isymb
                colcount += 1
                if (colcount < length):
                    isymb = inpline[colcount]
            if len(istring) > 16:
                print "Invalid Identifier  "  + istring + " exceeds the length limit of 16 "
            else:
                #print "Token :  " + istring + "  Code : " + str(codes["Identifier"]) 
                outline += str(codes["Identifier"]) + " "
                outsrc.append(istring)
        elif (digits.__contains__(isymb)) and mlcommentflag == False:
            istring = isymb
            colcount += 1
            while(colcount < length and (digits.__contains__(inpline[colcount]) or inpline[colcount] == "." )):
                istring += inpline[colcount]
                colcount +=1
            if(istring.find(".") == -1):
                if(len(istring) > 9):
                    print "Invalid Integer value  "  + istring + "  exceeds the length limit of 9 "
                else:
                    #print "Token :  " + istring + "  Code : " + str(codes["Integer"])
                    outline += str(codes["Integer"]) + " "
                    outsrc.append(istring)
            else:
                if(len(istring) > 8):
                    print "Invalid Real number value  "  + istring + "  exceeds the length limit of 7 "
                else:
                    #print "Token :  " + istring + "  Code : " + str(codes["Real"]) 
                    outline += str(codes["Real"]) + " "
                    outsrc.append(istring)
        elif (isymb == " " or isymb == newline[0]):
            colcount += 1
        else:
            print "Invalid symbol   " + isymb +  "  Code : " + str(asc[isymb])
            colcount += 1
    istring = ""
    rowcount += 1        
    #print outline
    return outline,outsrc
    outputlist.append(outline) 

def main():
    print "                           Pragmatics           "
    print " Authors : "
    print "            1. Aravindh Sampathkumar , aravins@clemson.edu "
    print "            2. Sakthi Gurumaharaj , sakths@clemson.edu "
    print " "
    print " Time : " + str(time.asctime(time.localtime(time.time())))
    print " "  
    '''print "                           Semantic Analyzer - II           "
    print " Authors : "
    print "            1. Aravindh Sampathkumar , aravins@clemson.edu "
    print "            2. Sakthi Gurumaharaj , sakths@clemson.edu "
    print " "
    print " Time : " + str(time.asctime(time.localtime(time.time())))
    print " "  '''
    global semantic_stack
    ''' print "                           PARSER           "
    print " Authors : "
    print "            1. Aravindh Sampathkumar , aravins@clemson.edu "
    print "            2. Sakthi Gurumaharaj , sakths@clemson.edu "
    print " "
    print " Time : " + str(time.asctime(time.localtime(time.time())))
    print " " '''
    
    """    Prepare the matrix data for reference in the parser    """
    matrixfile = open("matrixdata","r")
    matrix = []
    for row in matrixfile.readlines():
        if row.__contains__(newline[0]):
            row = row.rstrip('\n')
        matrix.append(row)
    """ Now the matrix can be referred using matrix[token1][token2] """
    
    """ Prepare the Grammar for reference in the parser """
    Grammarfile = open('Grammar','r')
    grammar = []
    for g in Grammarfile.readlines():
        if g.__contains__(newline[0]):
            g = g.rstrip('\n')
        gr = g.split()
        grammar.append(gr)
    fgrammar = []
    for line in grammar:
        lhs = []
        rhs = []
        lhs.append(line[-1])
        rhs.append(line[2:-1])
        redno = line[0]
        gr = [redno,lhs,rhs]
        fgrammar.append(gr)
    """ The grammar is represented using the format [[redno,[lhs],[rhs]],[redno,[lhs],[rhs]] . . . ]
        
        To use the grammar : 
        ===========================================================================
        fgrammar[0] ===> [redno,[lhs],[rhs]]   (representation of a production)
        fgrammar[0][0] ==> reduction #
        fgrammar[0][1] ==> the lhs of the production
        fgrammar[0][2] ==> List of tokens in the rhs of the production
        fgrammar[0][2][0] ==> first element in the rhs of the production
        len(fgrammar[0][2])  ===> No.of elements in the rhs of a production
        len(fgrammar) ===>  No.of productions in the grammar 
    
    """
    """ Read the input file for the input text """
    #inpfile = open("parsertest.txt","r")
    #inpfile = open("errordata","r")
    #inpfile = open("sem.txt","r")
    #inpfile = open("semerr","r")
    #inpfile = open("sem2inp","r")
    #inpfile = open("sem2err","r")
    #inpfile = open("testpgm","r")
    #inpfile = open("recursion","r")
    #inpfile = open("callbyref","r")
    #inpfile = open("callbyvalue","r")
    #inpfile = open("sorting","r")
    #inpfile = open("procedure","r")
    inpfile = open("recursion","r")
    rowcount = 0
    """ Perform initial data cleaning """
    for line in inpfile.readlines():
        ''' Trim the newline character /n in the input lines '''
        if line.__contains__(newline[0]):
            line = line.rstrip('\n')
            line = line + " "
        ''' Limit the length of an input line to 80 '''    
        if len(line) > 80:
            inp.append(line[0:79])
            rowcount += 1
        else:
            inp.append(line)
            rowcount += 1
    queue = deque()
    stack = []
    initialflag = True
    linectr = 1
    parser2semantics = []
    global tuples
    """ Line by line perform lexical analysis to get tokens and then do the parsing""" 
    for inpline in inp:
        """pass the current input line to lex function and get the tokens """
        #tokens = lexicalanalysis(inpline)
        ret = lexicalanalysis(inpline)
        tokens = ret[0]
        inpsource = ret[1]
        #print "Input source is ...>>>" + str(inpsource)
        #print "Tokenized input is --->>>" + str(tokens)
        inp1 = inpline
        inp1 = inp1.replace(";"," ;")
        inp1 = inp1.replace("{"," {")
        inp1 = inp1.replace("}"," }")
        inp1 = inp1.split()
        inp_stack = []
        for val in inp1:
            inp_stack.append(val)
        inp_stack = inpsource
        #print "inp_stack at the start of inputline is " + str(inp_stack)
        print " "
        print "          " + inpline
        print " "
        if tokens != "" :
            #print tokens
            #print "testing"
            if flags["20"] == "on":
                tuples.append("Tuple is (20,FLAG,#,#)")
            
            """ Parse the tokens into a list structure """
            tokenlist = tokens.split()
            #print tokenlist
            """ Push the individual tokens of the line into the que for processsing """
            for token in tokenlist:
                queue.append(token)
            """ Move the first element of the queue into the stack """
            if initialflag == True:
                token2 = queue.popleft()
                stack.append(token2)
                semantic_stack.append(inp_stack[0])
                inp_stack = inp_stack[1:]
                #print "Added the following to the semantic stack " + str(inp_stack[0])
                initialflag = False
            processctr = 0
            ''' Code included for semantics purpose '''
            parser2semantics = []
            parser2semantics.append(inpline)
            
            """ Until the queue is emptied do the processing """
            while (len(queue) > 0):
                redlist = []
                token1 = stack[-1]
                prevtoken = token2
                token2 = queue.popleft()  
                #print "In the queue" + str(processctr)
                #print "About to process Token : " + token2
                #print "latest item in the stack is " + token1  
                """ Perform Matrix lookup """
                wprelation = matrix[int(token1)][int(token2)]
                #print "wprelation is " + wprelation
                if flags["9"] == "on":
                    print "The top of the stack   is " + symtab[int(stack[-1])]
                    print "The input symbol is   " + symtab[int(token2)]
                    print "The relation is   " + str(wprelation)
                    
                if wprelation == "0":
                    print "****************************************************************************"
                    print "Error occured in line " + str(linectr) + "  between the symbols   " + symtab[int(prevtoken)] + "  and   " + symtab[int(token2)]
                    
                    stackcontents = ""
                    for symb in stack:
                        #print symb
                        stackcontents += symtab[int(symb)] + " "
                    print "The current stack is :  " + stackcontents
                    queueprint = symtab[int(token2)] + " "
                    while (len(queue) > 0):
                        #print queue.popleft()
                        queueprint += symtab[int(queue.popleft())] + " "

                    stackprint = ""
                    #print stackbackup
                    #print stack
                    """
                    for i in range(len(stackbackup),len(stack)):
                        stackprint += symtab[int(stack[i])] """
                    #print processctr
                    for i in range(processctr):
                        stackprint += symtab[int(stack[-(i+1)])] + " "
                    print "Symbols popped out of stack are : " + stackprint
                    stack = stack[0:-processctr]
                    
                    stackcontents = ""
                    for symb in stack:
                        #print symb
                        stackcontents += symtab[int(symb)] + " "
                    print "stack after the modification is  : " + stackcontents
                    print "Symbols ignored from the input statement : " + queueprint
                    print "****************************************************************************"
                elif wprelation == '1' or wprelation == '3' :
                    #print "appending to the stack :  " + token2
                    processctr += 1
                    stack.append(token2)
                    semantic_stack.append(inp_stack[0])
                    #print "appending to the semantic stack " + inp_stack[0]
                    inp_stack = inp_stack[1:]
                    
                    #print "The stack after append is " + str(stack)
                    if stack == ["2","3","39"]:
                        #print "Reduction # : 1   start --> prog body END"
                        print "Parsing successfully Completed !!!!"   
                        parser2semantics.append('1')
                        semantics("1")
                        break                     
                elif wprelation == "2":
                    """ Got to perform grammar look up for token1  """
                    #print "searching grammar for token  " + token1
                    for production in fgrammar:
                        """ Find all productions that end with token1 in RHS """
                        #print "only the RHS last token "
                        #print production[2][0][-1]
                        #redlist = []
                        if production[2][0][-1] == token1:
                            #print "Found Reduction # " + str(production[0])
                            """ List of found applicable reductions """
                            redlist.append(production)
                    """print "The valid reductions are : "
                    for red in redlist:
                        print red  """
                    stacklen = len(stack)
                    """   red[0]  ==> Prod number
                        red[1]   ===> LHS
                        red[2]  ==> RHS
                    """
                    #print "About to chk for applying reductions"
                    #print "The stack as of now is " + str(stack)
                    if flags["8"] == "on":
                        stackcontents = ""
                        for symb in stack:
                            #print symb
                            stackcontents += symtab[int(symb)] + " "
                        print "The stack before applying reduction is :  " + stackcontents
                    
                    for red in redlist:
                        prodlen = len(red[2][0])
                        """ print "checking the production :  " + str(red)
                        print "Prod len is " + str(prodlen)
                        print "stacklen is " + str(stacklen) """
                        
                        if prodlen <= stacklen:
                            """ Check if the RHS of the production matches the end of the stack """
                            #print "About to compare  " + str(red[2][0]) + "vs  " + str(stack[-prodlen:])
                            if red[2][0] == stack[-prodlen:]:
                                """ Apply the production """
                                #print "Applied production #  " + str(red)
                                
                                #print "semantic_stack b4 reduction is ...... " + str(semantic_stack)
                                redstring = ""
                                for i in red[2][0]:
                                    redstring += symtab[int(i)] + " "
                                #flags["10"] = "on"
                                handles = []
                                if flags["10"] == "on":
                                    handles = stack[-prodlen:]
                                    handlestr = ""
                                    for handle in handles:
                                        handlestr += symtab[int(handle)] + " "
                                    print "The matched handle is   " + handlestr  
                                if flags["7"] == "on":
                                    print "Reduction # : " + str(red[0]) + "   " + symtab[int(red[1][0])] + "-->  " + redstring
                                #print "Reduction # : " + str(red[0]) + "   " + symtab[int(red[1][0])] + "-->  " + redstring
                                #print red[1][0]
                                #print stack[-prodlen:]
                                #print "stack b4 mod is" + str(stack) 
                                #parser2semantics.append(list(stack))
                                parser2semantics.append(str(red[0]))
                                #print  "Modding th e stack from " + str(stack[-prodlen:]) + "   To   " + str(red[1][0])
                                semantics(red[0])
                                #print "length of stack b4 modification ==> " + str (len())
                                l = len(stack[-prodlen:])
                                #print "parser is about to pop " +str(l)+ " Times"
                                stack[-prodlen:] = [red[1][0]]
                                #print "stack after modification is  " + str(stack)
                                #parser2semantics.append(list(stack))
                                #print "length of "
                                if red[0] in donotmod:
                                    popctr = l - 1
                                    #print "chk passed hence one less pop"
                                else:
                                    popctr = l
                                #print "About to pop " + str(popctr)+ " times"
                                for i in range(popctr):
                                    semantic_stack.pop()
                                
                                if red[0] in donotmod:
                                    pass
                                else:
                                    for value in [red[1][0]]:
                                        semantic_stack.append(symtab[int(value)])
                                if flags["8"] == "on":
                                    stackcontents = ""
                                    for symb in stack:
                                        #print symb
                                        stackcontents += symtab[int(symb)] + " "
                                    print "The stack after applying reduction is :  " + stackcontents
                                stackforsem = []
                                for symb in stack:
                                    stackforsem.append(symtab[int(symb)])
                                #print "stackfor sem is " + str(stackforsem)
                                queue.appendleft(token2)
                                break

        linectr += 1
        #semantics(parser2semantics)
    

    pragmatics(tuples)
    
def chklocsymtab(var):
    namelist = []
    for row in locsymbtab:
        namelist.append(row['Name'])
    if var in namelist:
        return True
    else:
        print "Error ! ! - Usage of undeclared variable  - " + var
        dupflag = True
        return False
    namelist = []

def chkglosymtab(var):
    namelist = []
    for row in glosymbtab:
        namelist.append(row['Name'])
    if var in namelist:
        return True
    else:
        print "Error ! ! - Usage of undeclared variable  - " + var
        dupflag = True
        return False
    namelist = []
    
def chknumber(var):
    if var.find(".") == -1:
        if var.isdigit():
            return "integer"
        else:
            return "string"
    else:
        return "real"

def getstentry(var):
    found_flag = False
    for row in locsymbtab:
        if row['Name'] == var:
            found_flag = True
            return row
    for row in glosymbtab:
        if row['Name'] == var:
            found_flag = True
            return row
    if found_flag == False:
        print "Error ! - use of undeclared variable - " +var 
        return " "
def getintintermed():
    global intintermedctr
    res = "I$" + str(intintermedctr)
    intintermedctr = intintermedctr + 1
    return res
def getrealintermed():
    global realintermedctr
    res = "R$" + str(realintermedctr)
    realintermedctr = realintermedctr + 1
    return res
def getboointermed():
    global boointermedctr
    res = "B$" + str(boointermedctr)
    boointermedctr = boointermedctr + 1
    return res
def getloopintermed():
    global loopintermedctr
    res = "L$" + str(loopintermedctr)
    loopintermedctr = loopintermedctr + 1
    return res
def getoutvarname():
    global outvarctr
    res = "parameter" + str(outvarctr)
    outvarctr += 1
    return res
def getretlabelname():
    global retlabelctr
    res = "retlbl" + str(retlabelctr)
    retlabelctr += 1
    return res
def findtype(var):

    if (var.find("$") != -1):
        #the var is an intermediate one
        return var[0]
    elif var[0] == "-":
        if var[1:].isdigit():
            return("I")
    elif var.isdigit():
        return("I")
    elif var.find(".") != -1:
        return("R")
    elif var == "" or getstentry(var) == " ":
        return " "
    elif getstentry(var)['Type'] == "INTEGER":
        return("I")
    elif getstentry(var)['Type'] == "REAL":
        return("R")
def getreg(val):
    ctr = 1
    global reg
    foundfree = False
    d = {1:"ebx",2:"ecx",3:"edx"}
    print "about to insert into reg --> " +str(val)
    print "current reg status is "+str(reg)
    for register in reg:
        if register == " ":
            foundfree = True
            reg[ctr-1] = val
            print "inserted into reg ==>  "+str(reg[ctr-1])
            print "reg is " + str(reg)
            return d[ctr]
        ctr += 1     
    if foundfree == False:
        print "Error in register allocation - No free register found"
def freereg(val):
    global reg
    d = {1:"ebx",2:"ecx",3:"edx"}
    print "befor check is "+str(reg)
    avail = reg.index(val)
    if avail != -1:
        reg[avail] = " "
        return d[avail+1]
    else:
        print "Error - register could not be freed"

def semantics(red):
    global semantic_stack
    global locsymbtab
    global glosymbtab
    global dupflag
    global in_proc_flag
    global valref
    global tuples
    procname1 = ""
    
    if red == '1':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is (" + semantic_stack[-3] + ",ENDPROGRAM,#,#)"
        tuples.append("Tuple is (" + semantic_stack[-3] + ",ENDPROGRAM,#,#)")
        print "The Global Symbol Table is "
        for row in glosymbtab:
            print "'Name : " + row['Name'] + "' Type : " + row['Type'] + ", Shape : " + row['Shape'] + ", Rows : " + str(row['Rows']) + ", Cols : " + str(row['Cols']) + ", Calltype" + row['calltype']
        
    elif red == '2':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        semantic_stack[-2] = semantic_stack[-1]
        print "Tuple is (#,PROGRAMBEGIN," + str(semantic_stack[-2]) + ",#)"
        tuples.append("Tuple is (#,PROGRAMBEGIN," + str(semantic_stack[-2]) + ",#)")
        gst = {'Name': semantic_stack[-1] ,'Type':'PROGRAM' ,'Shape':'N/A' ,'Rows':0 ,'Cols':0,'calltype' : 'N/A'}
        glosymbtab.append(gst)

    elif red == '5':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is (#,ENDDECLARATIONS,#,#)"
        tuples.append("Tuple is (#,ENDDECLARATIONS,#,#)")
    elif red == '8':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is (" + semantic_stack[-1] + ",MEMORY" + ",1,0)"
        tuples.append("Tuple is (" + semantic_stack[-1] + ",MEMORY" + ",1,0)")
        gst = {'Name':semantic_stack[-1] ,'Type':semantic_stack[-2],'Shape':'scalar' ,'Rows':1 ,'Cols':0,'calltype' : 'N/A'}
        
        if in_proc_flag == True :
            # Checking for duplicates in local symb table
            namelist = []
            for row in locsymbtab:
                namelist.append(row['Name'])
            if semantic_stack[-1] in namelist:
                print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-1]
                dupflag = True
            namelist = []
            if dupflag == False:
                locsymbtab.append(gst)
            dupflag = False
        else:
            # Checking for duplicates in local symb table
            namelist = []
            for row in locsymbtab:
                namelist.append(row['Name'])
            if semantic_stack[-1] in namelist:
                print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-1]
                dupflag = True
            namelist = []
            # checking for duplicates in global table
            namelist = []
            for row in glosymbtab:
                namelist.append(row['Name'])
            if semantic_stack[-1] in namelist:
                print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-1]
                dupflag = True
            namelist = []
            if dupflag == False:
                glosymbtab.append(gst)
            dupflag = False
        gst = {}
        
    elif red == '9':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is (" + semantic_stack[-2] + ",MEMORY," + semantic_stack[-1] + ",0)"
        tuples.append("Tuple is (" + semantic_stack[-2] + ",MEMORY," + semantic_stack[-1] + ",0)")
        if flags["12"] == "on":

            print "stack before : "
            print "Type :  "+ semantic_stack[-3] +", var : " + semantic_stack[-2]+", Integer : " + semantic_stack[-1]
            print "stack after :"
            print "declstat"
        gst = {'Name':semantic_stack[-2] ,'Type':semantic_stack[-3],'Shape':'vector' ,'Rows':semantic_stack[-1] ,'Cols':0,'calltype' : 'N/A'}
        #glosymbtab.append(gst)
        if in_proc_flag == True :
            # Checking for duplicates in local symb table
            namelist = []
            for row in locsymbtab:
                namelist.append(row['Name'])
            if semantic_stack[-2] in namelist:
                print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-2]
                dupflag = True
            namelist = []
            if dupflag == False:
                locsymbtab.append(gst)
            dupflag = False

        else:
            # Checking for duplicates in local symb table
            namelist = []
            for row in locsymbtab:
                namelist.append(row['Name'])
            if semantic_stack[-2] in namelist:
                print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-2]
                dupflag = True
            namelist = []
            # checking for duplicates in global table
            namelist = []
            for row in glosymbtab:
                namelist.append(row['Name'])
            if semantic_stack[-2] in namelist:
                print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-2]
                dupflag = True
            namelist = []
            if dupflag == False:
                glosymbtab.append(gst)
            dupflag = False
        gst = {}
        
    elif red == '10':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        """ Insert into the symbol table """
        print "Tuple is (" + semantic_stack[-4] + ",MEMORY," + semantic_stack[-3] + "," + semantic_stack[-1] + ")"
        tuples.append("Tuple is (" + semantic_stack[-4] + ",MEMORY," + semantic_stack[-3] + "," + semantic_stack[-1] + ")")
        gst = {'Name':semantic_stack[-4] ,'Type':semantic_stack[-5],'Shape':'matrix' ,'Rows':semantic_stack[-3] ,'Cols':semantic_stack[-1],'calltype' : 'N/A'}
        
        if in_proc_flag == True :
            # Checking for duplicates in local symb table
            namelist = []
            for row in locsymbtab:
                namelist.append(row['Name'])
            if semantic_stack[-4] in namelist:
                print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-4]
                dupflag = True
            namelist = []
            # checking for duplicates in global table
            namelist = []
            for row in glosymbtab:
                namelist.append(row['Name'])
            if semantic_stack[-4] in namelist:
                print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-4]
                dupflag = True
            namelist = []
            if dupflag == False:
                locsymbtab.append(gst)
            dupflag = False
        else:
            # Checking for duplicates in local symb table
            namelist = []
            for row in locsymbtab:
                namelist.append(row['Name'])
            if semantic_stack[-4] in namelist:
                print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-4]
                dupflag = True
            namelist = []
            # checking for duplicates in global table
            namelist = []
            for row in glosymbtab:
                namelist.append(row['Name'])
            if semantic_stack[-4] in namelist:
                print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-4]
                dupflag = True
            namelist = []
            if dupflag == False:
                glosymbtab.append(gst)
            dupflag = False
        gst = {}
    elif red == '11':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        #semantic_stack.append(inputline[0])
        pass
    elif red == '12':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        #semantic_stack.append(inputline[0])
        pass
    elif red == '16':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is ("+ semantic_stack[-4] + ",ENDPROCEDURE,#,#)"
        tuples.append("Tuple is ("+ semantic_stack[-4] + ",ENDPROCEDURE,#,#)")
        in_proc_flag = False
        print "The local Symbol Table is "
        for row in locsymbtab:
            print "'Name : " + row['Name'] + "' Type : " + row['Type'] + ", Shape : " + row['Shape'] + ", Rows : " + str(row['Rows']) + ", Cols : " + str(row['Cols']) + ", Calltype" + row['calltype']
        locsymbtab = [] 
    elif red == '17':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is ("+ semantic_stack[-3] + ",ENDPROCEDURE,#,#)"
        tuples.append("Tuple is ("+ semantic_stack[-3] + ",ENDPROCEDURE,#,#)")
        in_proc_flag = False
        print "The local Symbol Table is "
        for row in locsymbtab:
            print "'Name : " + row['Name'] + "' Type : " + row['Type'] + ", Shape : " + row['Shape'] + ", Rows : " + str(row['Rows']) + ", Cols : " + str(row['Cols']) + ", Calltype" + row['calltype']
        locsymbtab = []
    elif red == '18':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is (#,ENDPARAMETERLIST,#,#)"
        tuples.append("Tuple is (#,ENDPARAMETERLIST,#,#)")
    elif red == '19':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is (#,NOFORMALPARAMETERS,#,#)"
        tuples.append("Tuple is (#,NOFORMALPARAMETERS,#,#)")
    elif red == '20':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        """ Insert into symbol table """ 
        print "Tuple is ("+ semantic_stack[-1] + ",BEGINPROCEDURE,#,#)"
        tuples.append("Tuple is ("+ semantic_stack[-1] + ",BEGINPROCEDURE,#,#)")
        in_proc_flag = True
        gst = {'Name': semantic_stack[-1] ,'Type': 'PROCEDURE','Shape': 'N/A' ,'Rows':0 ,'Cols':0,'calltype' : 'N/A'}
        glosymbtab.append(gst)
        locsymbtab.append(gst)
        gst = {}
        semantic_stack[-2] = semantic_stack[-1]
    elif red == '21':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is (" + semantic_stack[-1] + ",FORMAL" + valref + "PARAMETER," +  "1,0)"  
        tuples.append("Tuple is (" + semantic_stack[-1] + ",FORMAL" + valref + "PARAMETER," +  "1,0)")         
        gst = {'Name':semantic_stack[-1] ,'Type':semantic_stack[-2],'Shape':'scalar' ,'Rows':1 ,'Cols':0,'calltype' : valref}
        # Checking for duplicates in local symb table
        namelist = []
        for row in locsymbtab:
            namelist.append(row['Name'])
        if semantic_stack[-1] in namelist:
            print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-1]
            dupflag = True
        namelist = []
        if dupflag == False:
            locsymbtab.append(gst)
        dupflag = False
        gst = {}
    elif red == '22':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is (" + semantic_stack[-2] + ",FORMAL" + valref + "PARAMETER," + semantic_stack[-1] + ",0)"
        tuples.append("Tuple is (" + semantic_stack[-2] + ",FORMAL" + valref + "PARAMETER," + semantic_stack[-1] + ",0)")
        gst = {'Name':semantic_stack[-2] ,'Type':semantic_stack[-3],'Shape':'vector' ,'Rows':semantic_stack[-1] ,'Cols':0,'calltype' : valref}
        # Checking for duplicates in local symb table
        namelist = []
        for row in locsymbtab:
            namelist.append(row['Name'])
        if semantic_stack[-2] in namelist:
            print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-2]
            dupflag = True
        namelist = []
        # checking for duplicates in global table
        namelist = []
        for row in glosymbtab:
            namelist.append(row['Name'])
        if semantic_stack[-2] in namelist:
            print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-2]
            dupflag = True
        namelist = []
        if dupflag == False:
            locsymbtab.append(gst)
        dupflag = False
        gst = {}                
    elif red == '23':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is (" + semantic_stack[-4] + ",FORMAL" + valref + "PARAMETER," + semantic_stack[-3] + "," + semantic_stack[-1] + ")"
        tuples.append("Tuple is (" + semantic_stack[-4] + ",FORMAL" + valref + "PARAMETER," + semantic_stack[-3] + "," + semantic_stack[-1] + ")")  
        gst = {'Name':semantic_stack[-4] ,'Type':semantic_stack[-5],'Shape':'matrix' ,'Rows':semantic_stack[-3] ,'Cols':semantic_stack[-1],'calltype' : valref}
        # Checking for duplicates in local symb table
        namelist = []
        for row in locsymbtab:
            namelist.append(row['Name'])
        if semantic_stack[-4] in namelist:
            print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-4]
            dupflag = True
        namelist = []
        # checking for duplicates in global table
        namelist = []
        for row in glosymbtab:
            namelist.append(row['Name'])
        if semantic_stack[-4] in namelist:
            print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-4]
            dupflag = True
        namelist = []
        if dupflag == False:
            locsymbtab.append(gst)
        dupflag = False
        gst = {}             
    elif red == '24':  
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is (#,BEGINPARAMETERLIST,#,#)"
        print "Tuple is (" + semantic_stack[-1] + ",FORMAL" + valref + "PARAMETER," +  "1,0)"
        tuples.append("Tuple is (#,BEGINPARAMETERLIST,#,#)")
        tuples.append("Tuple is (" + semantic_stack[-1] + ",FORMAL" + valref + "PARAMETER," +  "1,0)")           
        gst = {'Name':semantic_stack[-1] ,'Type':semantic_stack[-2],'Shape':'scalar' ,'Rows': 1 ,'Cols': 0 ,'calltype' : valref}
        #glosymbtab.append(gst)
        # Checking for duplicates in local symb table
        namelist = []
        for row in locsymbtab:
            namelist.append(row['Name'])
        if semantic_stack[-1] in namelist:
            print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-1]
            dupflag = True
        namelist = []
        # checking for duplicates in global table
        #print "in_proc_flag is " + str(in_proc_flag)
        if in_proc_flag == False: 
            namelist = []
            for row in glosymbtab:
                namelist.append(row['Name'])
            if semantic_stack[-1] in namelist:
                print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-1]
                dupflag = True
            namelist = []
        if dupflag == False:
            locsymbtab.append(gst)
        dupflag = False
        gst = {}
    elif red == '25':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is (#,BEGINPARAMETERLIST,#,#)"
        print "Tuple is (" + semantic_stack[-2] + ",FORMAL" + valref + "PARAMETER," + semantic_stack[-1] + ",0)"
        tuples.append("Tuple is (#,BEGINPARAMETERLIST,#,#)")
        tuples.append("Tuple is (" + semantic_stack[-2] + ",FORMAL" + valref + "PARAMETER," + semantic_stack[-1] + ",0)")    
        gst = {'Name':semantic_stack[-2] ,'Type':semantic_stack[-3],'Shape':'vector' ,'Rows':semantic_stack[-1] ,'Cols': 0 ,'calltype' : valref}
        #glosymbtab.append(gst)
        # Checking for duplicates in local symb table
        namelist = []
        for row in locsymbtab:
            namelist.append(row['Name'])
        if semantic_stack[-2] in namelist:
            print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-2]
            dupflag = True
        namelist = []
        # checking for duplicates in global table
        namelist = []
        for row in glosymbtab:
            namelist.append(row['Name'])
        if semantic_stack[-2] in namelist:
            print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-2]
            dupflag = True
        namelist = []
        if dupflag == False:
            locsymbtab.append(gst)
        dupflag = False
        gst = {}            
    elif red == '26':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        """ Insert into symb table """
        print "Tuple is (#,BEGINPARAMETERLIST,#,#)"
        print "Tuple is (" + semantic_stack[-4] + ",FORMAL" + valref + "PARAMETER," + semantic_stack[-3] + "," + semantic_stack[-1] + ")"
        tuples.append("Tuple is (#,BEGINPARAMETERLIST,#,#)")
        tuples.append("Tuple is (" + semantic_stack[-4] + ",FORMAL" + valref + "PARAMETER," + semantic_stack[-3] + "," + semantic_stack[-1] + ")")
        gst = {'Name':semantic_stack[-4] ,'Type':semantic_stack[-5],'Shape':'matrix' ,'Rows':semantic_stack[-3] ,'Cols':semantic_stack[-1],'calltype' : valref}
        #glosymbtab.append(gst)
        # Checking for duplicates in local symb table
        namelist = []
        for row in locsymbtab:
            namelist.append(row['Name'])
        if semantic_stack[-4] in namelist:
            print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-4]
            dupflag = True
        namelist = []
        # checking for duplicates in global table
        namelist = []
        for row in glosymbtab:
            namelist.append(row['Name'])
        if semantic_stack[-4] in namelist:
            print "Error ! ! - Duplicate variable definition found - " + semantic_stack[-4]
            dupflag = True
        namelist = []
        if dupflag == False:
            locsymbtab.append(gst)
        dupflag = False
        gst = {}
    elif red == '27':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        valref = "value"
        print ""
    elif red == '28':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        valref = "reference"    
    elif red == '30':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is (MAIN,LABEL,#,#)"
        tuples.append("Tuple is (MAIN,LABEL,#,#)")
    elif red == '36':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is(#,ENDOFINPUTPARAMETERS,#,#)"
        print "Tuple is(scanf,ENDINPUTPARAMETERS,#,#)"
        tuples.append("Tuple is(#,ENDOFINPUTPARAMETERS,#,#)")
        tuples.append("Tuple is(scanf,ENDINPUTPARAMETERS,#,#)")
    elif red == '37':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is(printf,ENDOUTPARAMETERS,#,#)"
        tuples.append("Tuple is(printf,ENDOUTPARAMETERS,#,#)")
    elif red == '39':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is(#,INPUTPARAMETER,"+semantic_stack[-1]+",#)"
        tuples.append("Tuple is(#,INPUTPARAMETER,"+semantic_stack[-1]+",#)")
    elif red == '40':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-6]
        index1 = semantic_stack[-4]
        row = getstentry(var)
        if row != " ":
            if row["Shape"] != "vector":
                print "Error ! - Expected a vector but found - " +var
            else:
                if findtype(index1) != "I":
                    print "Error ! - Index value in the matrix is not an integer ."
                else:
                    print "Tuple is(#,INPUTSUBPARAMETER," +var+ "," +index1+ ")"
                    tuples.append("Tuple is(#,INPUTSUBPARAMETER," +var+ "," +index1+ ")")
    elif red == '41':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-6]
        index1 = semantic_stack[-4]
        index2 = semantic_stack[-2]
        row = getstentry(var)
        if row != " ":
            if row["Shape"] != "matrix":
                print "Error ! - Expected a matrix but found - " +var
            else:
                if findtype(index1) != "I" or findtype(index2) != "I":
                    print "Error ! - Index value in the matrix is not an integer ."
                else:
                    ivar2 = getintintermed()
                    ivar3 = getintintermed()
                    print "Tuple is(" +ivar2+ ",IMULT," +getstentry(var)['Cols']+ "," +index1+ ")"
                    print "Tuple is(" +ivar3+ ",IADD," +ivar2+ "," +index2+ ")" 
                    print "Tuple is(#,INPUTSUBPARAMETER," +var+ "," +ivar3+ ")"
                    tuples.append("Tuple is(" +ivar2+ ",IMULT," +getstentry(var)['Cols']+ "," +index1+ ")")
                    tuples.append("Tuple is(" +ivar3+ ",IADD," +ivar2+ "," +index2+ ")")
                    tuples.append("Tuple is(#,INPUTSUBPARAMETER," +var+ "," +ivar3+ ")")
    elif red == '42':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is(#,CALL,scanf,#)"
        print "Tuple is(#,INPUTPARAMETER," +semantic_stack[-1]+ ",#)"  
        tuples.append("Tuple is(#,CALL,scanf,#)")
        tuples.append("Tuple is(#,INPUTPARAMETER," +semantic_stack[-1]+ ",#)" )
    elif red == '43':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is(#,OUTPUTPARAMETER," +semantic_stack[-1]+ ",#)"  
        tuples.append("Tuple is(#,OUTPUTPARAMETER," +semantic_stack[-1]+ ",#)" )  
    elif red == '44':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is(#,OUTPUTSUBPARAMETER," +semantic_stack[-1]+ ",#)" 
        tuples.append("Tuple is(#,OUTPUTSUBPARAMETER," +semantic_stack[-1]+ ",#)" )
    elif red == '45':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-4]
        index1 = semantic_stack[-2] 
        row = getstentry(var)
        if row != " ":
            if row["Shape"] != "vector":
                print "Error ! - Expected a vector but found - " +var
            else:
                if findtype(index1) != "I":
                    print "Error ! - Index value in the matrix is not an integer ."
                else:
                    print "Tuple is(#,OUTPUTSUBPARAMETER," +var+ "," +index1+ ")"
                    tuples.append("Tuple is(#,OUTPUTSUBPARAMETER," +var+ "," +index1+ ")")
    elif red == '46':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-6]
        index1 = semantic_stack[-4]
        index2 = semantic_stack[-2]
        row = getstentry(var)
        if row != " ":
            if row["Shape"] != "matrix":
                print "Error ! - Expected a matrix but found - " +var
            else:
                if findtype(index1) != "I" or findtype(index2) != "I":
                    print "Error ! - Index value in the matrix is not an integer ."
                else:
                    ivar2 = getintintermed()
                    ivar3 = getintintermed()
                    print "Tuple is(" +ivar2+ ",IMULT," +getstentry(var)['Cols']+ "," +index1+ ")"
                    print "Tuple is(" +ivar3+ ",IADD," +ivar2+ "," +index2+ ")" 
                    print "Tuple is(#,OUTPUTSUBPARAMETER," +var+ "," +ivar3+ ")"
                    tuples.append("Tuple is(" +ivar2+ ",IMULT," +getstentry(var)['Cols']+ "," +index1+ ")")
                    tuples.append("Tuple is(" +ivar3+ ",IADD," +ivar2+ "," +index2+ ")")
                    tuples.append("Tuple is(#,OUTPUTSUBPARAMETER," +var+ "," +ivar3+ ")")

    elif red == '47':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is(#,CALL,printf,#)"
        print "Tuple is(#,OUTPUTPARAMETER,"+semantic_stack[-1]+",#)"
        tuples.append("Tuple is(#,CALL,printf,#)")
        tuples.append("Tuple is(#,OUTPUTPARAMETER,"+semantic_stack[-1]+",#)")
    elif red == '48':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is("+semantic_stack[-3]+",ENDACTUALPARAMETERLIST,#,#)"
        tuples.append("Tuple is("+semantic_stack[-3]+",ENDACTUALPARAMETERLIST,#,#)")
    elif red == '49':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is(#,NOACTUALPARAMETERS,#,#)"
        tuples.append("Tuple is(#,NOACTUALPARAMETERS,#,#)")
    elif red == '50':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        proc = semantic_stack[-1]
        if getstentry(proc)["Type"] != "PROCEDURE":
            print "Error ! - CALL should be followed by a procedure name "
        else:
            print "Tuple is("+proc+",CALL,#,#)"
            tuples.append("Tuple is("+proc+",CALL,#,#)")
        semantic_stack[-2] = proc
    elif red == '51':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-1]
        print "Tuple is(#,ORDINARYPARAMETER,"+var+",#)"
        tuples.append("Tuple is(#,ORDINARYPARAMETER,"+var+",#)")
    elif red == '52':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-1]
        index1 = semantic_stack[-2]
        if findtype(index1) != "I" :
            print "Error ! - Subscript of vector is not an integer " 
        print "Tuple is(#,ACTUAL" +semantic_stack[-5]+ "SUBPARAMETER,"+var+","+index1   +")"
        tuples.append("Tuple is(#,ACTUAL" +semantic_stack[-5]+ "SUBPARAMETER,"+var+","+index1   +")")
    elif red == '53':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-6]
        index1 = semantic_stack[-4]
        index2 = semantic_stack[-2]
        
        if getstentry(var)["Shape"] != "matrix":
            print "Error ! - " +var+ "is not a matrix as expected"
        else:
            if findtype(index1) != "I" or findtype(index2) != "I":
                print "Error ! - Subscript of matrix is not an integer " 
        ivar1 = getintintermed()
        ivar2 = getintintermed()
        print "Tuple is(" +ivar1+ ",IMULT," +row['Cols']+ "," +index1+ ")"
        print "Tuple is(" +ivar2+ ",IADD," +ivar1+ "," +index2+ ")" 
        print "Tuple is(#,ACTUAL" +semantic_stack[-5]+ "SUBPARAMETER,"+var+","+ivar2+")"
        tuples.append("Tuple is(" +ivar1+ ",IMULT," +row['Cols']+ "," +index1+ ")")
        tuples.append("Tuple is(" +ivar2+ ",IADD," +ivar1+ "," +index2+ ")")
        tuples.append("Tuple is(#,ACTUAL" +semantic_stack[-5]+ "SUBPARAMETER,"+var+","+ivar2+")")
    elif red == '54':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-1]
        print "Tuple is(#,BEGINPARAMETERLIST,#)"
        print "Tuple is(#,ORDINARYPARAMETER,"+var+",#)"
        tuples.append("Tuple is(#,BEGINPARAMETERLIST,#)")
        tuples.append("Tuple is(#,ORDINARYPARAMETER,"+var+",#)")
    elif red == '55':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-1]
        index1 = semantic_stack[-2]
        if findtype(index1) != "I" :
            print "Error ! - Subscript of vector is not an integer " 
        print "Tuple is(#,BEGINPARAMETERLIST,#)"
        print "Tuple is(#,ACTUAL" +semantic_stack[-5]+ "SUBPARAMETER,"+var+","+index1   +")"
        tuples.append("Tuple is(#,BEGINPARAMETERLIST,#)")
        tuples.append("Tuple is(#,ACTUAL" +semantic_stack[-5]+ "SUBPARAMETER,"+var+","+index1   +")")
    elif red == '56':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-6]
        index1 = semantic_stack[-4]
        index2 = semantic_stack[-2]
        
        if getstentry(var)["Shape"] != "matrix":
            print "Error ! - " +var+ "is not a matrix as expected"
        else:
            if findtype(index1) != "I" or findtype(index2) != "I":
                print "Error ! - Subscript of matrix is not an integer " 
        print "Tuple is(#,BEGINPARAMETERLIST,#)"
        tuples.append("Tuple is(#,BEGINPARAMETERLIST,#)")
        ivar1 = getintintermed()
        ivar2 = getintintermed()
        print "Tuple is(" +ivar1+ ",IMULT," +row['Cols']+ "," +index1+ ")"
        print "Tuple is(" +ivar2+ ",IADD," +ivar1+ "," +index2+ ")" 
        print "Tuple is(#,ACTUAL" +semantic_stack[-5]+ "SUBPARAMETER,"+var+","+ivar2+")"
        tuples.append("Tuple is(" +ivar1+ ",IMULT," +row['Cols']+ "," +index1+ ")")
        tuples.append("Tuple is(" +ivar2+ ",IADD," +ivar1+ "," +index2+ ")" )
        tuples.append("Tuple is(#,ACTUAL" +semantic_stack[-5]+ "SUBPARAMETER,"+var+","+ivar2+")")
    elif red == '57':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is("+semantic_stack[-3]+",LABEL,#,#)"
        tuples.append("Tuple is("+semantic_stack[-3]+",LABEL,#,#)")
    elif red == '58':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        print "Tuple is("+semantic_stack[-3]+",LABEL,#,#)"
        tuples.append("Tuple is("+semantic_stack[-3]+",LABEL,#,#)")
    elif red == '59':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        ivar1 = getloopintermed()
        print "Tuple is("+ivar1+",JUMP,#,#)"
        print "Tuple is("+semantic_stack[-3]+",LABEL,#,#)"
        tuples.append("Tuple is("+ivar1+",JUMP,#,#)")
        tuples.append("Tuple is("+semantic_stack[-3]+",LABEL,#,#)")
        semantic_stack[-3] = ivar1

        
    elif red == '60':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        bexp = semantic_stack[-3]
        if findtype(bexp) != "B":
            print "Error ! - Expected a boolean expression as IF condition"
        ivar1 = getloopintermed()
        print "Tuple is("+ivar1+",CJUMPF,"+bexp+",#)"
        tuples.append("Tuple is("+ivar1+",CJUMPF,"+bexp+",#)")
        semantic_stack[-5] = ivar1
    elif red == '61':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        #print "Tuple is("+semantic_stack[-3]+",JUMP,#,#)"
        #tuples.append("Tuple is("+semantic_stack[-3]+",JUMP,#,#)")
        global looplist
        #print looplist
        l = looplist.pop()
        print "Tuple is("+l+",JUMP,#,#)"
        tuples.append("Tuple is("+l+",JUMP,#,#)")
        global looplist1
        #print looplist1
        l = looplist1.pop()
        print "Tuple is("+l+",LABEL,#,#)"
        tuples.append("Tuple is("+l+",LABEL,#,#)")
    elif red == '62':          
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        bexp = semantic_stack[-3]
        if findtype(bexp) != "B":
            print "Error ! - Expected a boolean expression as while condition"
        print "Tuple is("+semantic_stack[-5]+",CJUMP,"+semantic_stack[-3]+",#)"
        global looplist1
        looplist1.append(semantic_stack[-5])
        tuples.append("Tuple is("+semantic_stack[-5]+",CJUMP,"+semantic_stack[-3]+",#)")
    elif red == '63': 
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        ivar1 = getloopintermed()
        ivar2 = getloopintermed()
        print "Tuple is("+ivar1+",LABEL,#,#)"
        tuples.append("Tuple is("+ivar1+",LABEL,#,#)")
        semantic_stack[-1] = ivar2
        global looplist
        looplist.append(ivar1)       
    elif red == '64':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-4]
        assignvar = semantic_stack[-2]
        vartype = findtype(var)
        assignvartype = findtype(assignvar)
        if vartype != assignvartype:
            ivar1 = ""
            if assignvartype == "I":
                ivar1 = getrealintermed()
                print "Tuple is("+ivar1+",CONVERTITOR,"+assignvar+",#)"
                tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+assignvar+",#)")
            elif assignvartype == "R":
                ivar1 = getintintermed()
                print "Tuple is("+ivar1+",CONVERTRTOI,"+assignvar+",#)"
                tuples.append("Tuple is("+ivar1+",CONVERTRTOI,"+assignvar+",#)")
            else:
                print "Error - Type mismatch while assigning value to " + var
            semantic_stack[-2] = ivar1 
            assignvar = ivar1
    
        if vartype == "I":
            ivar4 = getintintermed()
        elif vartype == "R":
            ivar4 = getrealintermed()
        print "Tuple is(" +var+ ",ASSIGN," +var+ "," +assignvar+ ")"
        tuples.append("Tuple is(" +var+ ",ASSIGN," +var+ "," +assignvar+ ")")
        semantic_stack[-4] = ivar4
    elif red == '65':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-6]
        assignvar = semantic_stack[-1]
        index1 = semantic_stack[-4]
        #index2 = semantic_stack[-5]
        if findtype(index1)!= "I":
            print "Error ! - Index value in the matrix is not an integer ."
        else:
            vartype = getstentry(var)['Type'][0]
            assignvartype = findtype(assignvar)
            if vartype != assignvartype:
                ivar1 = ""
                if assignvartype == "I":
                    ivar1 = getrealintermed()
                    print "Tuple is("+ivar1+",CONVERTITOR,"+assignvar+",#)"
                    tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+assignvar+",#)")
                elif assignvartype == "R":
                    ivar1 = getintintermed()
                    print "Tuple is("+ivar1+",CONVERTRTOI,"+assignvar+",#)"
                    tuples.append("Tuple is("+ivar1+",CONVERTRTOI,"+assignvar+",#)")
                else:
                    print "Error - Type mismatch while assigning value to " + var
                semantic_stack[-1] = ivar1 
                assignvar = ivar1
        
            if getstentry(var)['Type'] == "INTEGER":
                ivar4 = getintintermed()
            elif getstentry(var)['Type'] == "REAL":
                ivar4 = getrealintermed()
            print "Tuple is(" +ivar4+ ",SUBASSIGN," +var+ "," +index1+ ")"
            tuples.append("Tuple is(" +ivar4+ ",SUBASSIGN," +var+ "," +index1+ ")")
            semantic_stack[-6] = ivar4
                    
    elif red == '66':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-8]
        assignvar = semantic_stack[-1]
        index1 = semantic_stack[-6]
        index2 = semantic_stack[-4]
        if findtype(index1)!= "I" or findtype(index2)!= "I":
            print "Error ! - Index value in the matrix is not an integer ."
        else:
            vartype = getstentry(var)['Type'][0]
            assignvartype = findtype(assignvar)
            if vartype != assignvartype:
                ivar1 = ""
                if assignvartype == "I":
                    ivar1 = getrealintermed()
                    print "Tuple is("+ivar1+",CONVERTITOR,"+assignvar+",#)"
                    tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+assignvar+",#)")
                elif assignvartype == "R":
                    ivar1 = getintintermed()
                    print "Tuple is("+ivar1+",CONVERTRTOI,"+assignvar+",#)"
                    tuples.append("Tuple is("+ivar1+",CONVERTRTOI,"+assignvar+",#)")
                else:
                    print "Error - Type mismatch while assigning value to " + var
                semantic_stack[-1] = ivar1 
                assignvar = ivar1
        
            ivar2 = getintintermed()
            ivar3 = getintintermed()
            print "Tuple is(" +ivar2+ ",IMULT," +getstentry(var)['Cols']+ "," +index1+ ")"
            print "Tuple is(" +ivar3+ ",IADD," +ivar2+ "," +index2+ ")" 
            tuples.append("Tuple is(" +ivar2+ ",IMULT," +getstentry(var)['Cols']+ "," +index1+ ")")
            tuples.append("Tuple is(" +ivar3+ ",IADD," +ivar2+ "," +index2+ ")" )
            if getstentry(var)['Type'] == "INTEGER":
                ivar4 = getintintermed()
            elif getstentry(var)['Type'] == "REAL":
                ivar4 = getrealintermed()
            print "Tuple is(" +ivar4+ ",SUBASSIGN," +var+ "," +ivar2+ ")"
            tuples.append("Tuple is(" +ivar4+ ",SUBASSIGN," +var+ "," +ivar2+ ")")
            semantic_stack[-8] = ivar4
    elif red == '67':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-4]
        assignvar = semantic_stack[-2]
        vartype = findtype(var)
        assignvartype = findtype(assignvar)
        if vartype != assignvartype:
            ivar1 = ""
            if assignvartype == "I":
                ivar1 = getrealintermed()
                print "Tuple is("+ivar1+",CONVERTITOR,"+assignvar+",#)"
                tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+assignvar+",#)")
            elif assignvartype == "R":
                ivar1 = getintintermed()
                print "Tuple is("+ivar1+",CONVERTRTOI,"+assignvar+",#)"
                tuples.append("Tuple is("+ivar1+",CONVERTRTOI,"+assignvar+",#)")
            else:
                print "Error - Type mismatch while assigning value to " + var
            semantic_stack[-2] = ivar1 
            assignvar = ivar1
        print "Tuple is(" +var+ ",ASSIGN," +assignvar+ ",#)"
        tuples.append("Tuple is(" +var+ ",ASSIGN," +assignvar+ ",#)")
        semantic_stack[-4] = assignvar
    elif red == '68':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-7]
        assignvar = semantic_stack[-2]
        index1 = semantic_stack[-5]
        if findtype(index1)!= "I":
            print "Error ! - Index value in the matrix is not an integer ."
        else:
            vartype = getstentry(var)['Type'][0]
            assignvartype = findtype(assignvar)
            #print "****** var type is " + str(vartype)
            #print "****** assignvartype is " + str(assignvartype) 
            if vartype != assignvartype:
                ivar1 = ""
                if assignvartype == "I":
                    ivar1 = getrealintermed()
                    print "Tuple is("+ivar1+",CONVERTITOR,"+assignvar+",#)"
                    tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+assignvar+",#)")
                elif assignvartype == "R":
                    ivar1 = getintintermed()
                    print "Tuple is("+ivar1+",CONVERTRTOI,"+assignvar+",#)"
                    tuples.append("Tuple is("+ivar1+",CONVERTRTOI,"+assignvar+",#)")
                else:
                    print "Error - Type mismatch while assigning value to " + var
                semantic_stack[-2] = ivar1 
                assignvar = ivar1
        
            if getstentry(var)['Type'] == "INTEGER":
                ivar4 = getintintermed()
            elif getstentry(var)['Type'] == "REAL":
                ivar4 = getrealintermed()
            print "Tuple is(" +var+ ",SUBASSIGN," +assignvar+ "," +index1+ ")"
            tuples.append("Tuple is(" +var+ ",SUBASSIGN," +assignvar+ "," +index1+ ")")
            semantic_stack[-7] = assignvar

    elif red == '69':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var = semantic_stack[-9]
        assignvar = semantic_stack[-2]
        index1 = semantic_stack[-7]
        index2 = semantic_stack[-5]
        if findtype(index1)!= "I" or findtype(index2)!= "I":
            print "Error ! - Index value in the matrix is not an integer ."
        else:
            vartype = getstentry(var)['Type'][0]
            assignvartype = findtype(assignvar)
            if vartype != assignvartype:
                ivar1 = ""
                if assignvartype == "I":
                    ivar1 = getrealintermed()
                    print "Tuple is("+ivar1+",CONVERTITOR,"+assignvar+",#)"
                    tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+assignvar+",#)")
                elif assignvartype == "R":
                    ivar1 = getintintermed()
                    print "Tuple is("+ivar1+",CONVERTRTOI,"+assignvar+",#)"
                    tuples.append("Tuple is("+ivar1+",CONVERTRTOI,"+assignvar+",#)")
                else:
                    print "Error - Type mismatch while assigning value to " + var
                semantic_stack[-2] = ivar1 
                assignvar = ivar1
        
            ivar2 = getintintermed()
            ivar3 = getintintermed()
            print "Tuple is(" +ivar2+ ",IMULT," +getstentry(var)['Cols']+ "," +index1+ ")"
            print "Tuple is(" +ivar3+ ",IADD," +ivar2+ "," +index2+ ")" 
            tuples.append("Tuple is(" +ivar2+ ",IMULT," +getstentry(var)['Cols']+ "," +index1+ ")")
            tuples.append("Tuple is(" +ivar3+ ",IADD," +ivar2+ "," +index2+ ")" )
            if getstentry(var)['Type'] == "INTEGER":
                ivar4 = getintintermed()
            elif getstentry(var)['Type'] == "REAL":
                ivar4 = getrealintermed()
            print "Tuple is(" +var+ ",SUBASSIGN," +assignvar+ "," +ivar4+ ")"
            tuples.append("Tuple is(" +var+ ",SUBASSIGN," +assignvar+ "," +ivar4+ ")")
            semantic_stack[-9] = assignvar
                
    elif red == '70':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-3]
        var2 = semantic_stack[-1]
        if findtype(var1) != "B" or findtype(var2) != "B":
            print "Error ! - trying to OR operate a non boolean value."
        else:
            ivar1 = getboointermed()
            print "Tuple is("+ivar1+",OR,"+var1+","+var2+",)"
            tuples.append("Tuple is("+ivar1+",OR,"+var1+","+var2+",)")
            semantic_stack[-3] = ivar1
    elif red == '72':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-3]
        var2 = semantic_stack[-1]
        if findtype(var1) != "B" or findtype(var2) != "B":
            print "Error ! - trying to AND operate a non boolean value."
        else:
            ivar1 = getboointermed()
            print "Tuple is("+ivar1+",AND,"+var1+","+var2+",)"
            tuples.append("Tuple is("+ivar1+",AND,"+var1+","+var2+",)")
            semantic_stack[-3] = ivar1
    elif red == '74':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-1]
        if findtype(var1) != "B":
            print "Error ! - trying to negate a non boolean value."
        else:
            ivar1 = getboointermed()
            print "Tuple is("+ivar1+",NOT,"+var1+",#)"
            tuples.append("Tuple is("+ivar1+",NOT,"+var1+",#)")
            semantic_stack[-2] = ivar1
    elif red == '76':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-3]
        var2 = semantic_stack[-1]
        if findtype(var1) == "I" and findtype(var2) == "R":
            ivar1 = getrealintermed()
            print "Tuple is("+ivar1+",CONVERTITOR,"+var1+",#)"
            tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+var1+",#)")
            var1 = ivar1
        ivar2 = getboointermed()
        if findtype(var1) == "I":
            print "Tuple is("+ivar2+",ILT,"+var1+","+var2+")"
            tuples.append("Tuple is("+ivar2+",ILT,"+var1+","+var2+")")
        else:
            print "Tuple is("+ivar2+",RLT,"+var1+","+var2+")"   
            tuples.append("Tuple is("+ivar2+",RLT,"+var1+","+var2+")" )
        semantic_stack[-3] = ivar2
    elif red == '77':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-3]
        var2 = semantic_stack[-1]
        if findtype(var1) == "I" and findtype(var2) == "R":
            ivar1 = getrealintermed()
            print "Tuple is("+ivar1+",CONVERTITOR,"+var1+",#)"
            tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+var1+",#)")
            var1 = ivar1
        ivar2 = getboointermed()
        if findtype(var1) == "I":
            print "Tuple is("+ivar2+",ILE,"+var1+","+var2+")"
            tuples.append("Tuple is("+ivar2+",ILE,"+var1+","+var2+")")
        else:
            print "Tuple is("+ivar2+",RLE,"+var1+","+var2+")"   
            tuples.append("Tuple is("+ivar2+",RLE,"+var1+","+var2+")")
        semantic_stack[-3] = ivar2
    elif red == '78':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-3]
        var2 = semantic_stack[-1]
        if findtype(var1) == "I" and findtype(var2) == "R":
            ivar1 = getrealintermed()
            print "Tuple is("+ivar1+",CONVERTITOR,"+var1+",#)"
            tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+var1+",#)")
            var1 = ivar1
        ivar2 = getboointermed()
        if findtype(var1) == "I":
            print "Tuple is("+ivar2+",IGT,"+var1+","+var2+")"
            tuples.append("Tuple is("+ivar2+",IGT,"+var1+","+var2+")")
        else:
            print "Tuple is("+ivar2+",RGT,"+var1+","+var2+")"  
            tuples.append("Tuple is("+ivar2+",RGT,"+var1+","+var2+")" ) 
        semantic_stack[-3] = ivar2
    elif red == '79':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-3]
        var2 = semantic_stack[-1]
        if findtype(var1) == "I" and findtype(var2) == "R":
            ivar1 = getrealintermed()
            print "Tuple is("+ivar1+",CONVERTITOR,"+var1+",#)"
            tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+var1+",#)")
            var1 = ivar1
        ivar2 = getboointermed()
        if findtype(var1) == "I":
            print "Tuple is("+ivar2+",IGE,"+var1+","+var2+")"
            tuples.append("Tuple is("+ivar2+",IGE,"+var1+","+var2+")")
        else:
            print "Tuple is("+ivar2+",RGE,"+var1+","+var2+")"   
            tuples.append("Tuple is("+ivar2+",RGE,"+var1+","+var2+")" )
        semantic_stack[-3] = ivar2
    elif red == '80':
        # Check if Mixed mode arithmetic
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-3]
        var2 = semantic_stack[-1]
        if findtype(var1) != " " and findtype(var2) != " ":
            if findtype(var1) == "I" and findtype(var2) == "R":
                ivar1 = getrealintermed()
                print "Tuple is("+ivar1+",CONVERTITOR,"+var1+",#)"
                tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+var1+",#)")
                var1 = ivar1
            ivar2 = getboointermed()
            if findtype(var1) == "I":
                print "Tuple is("+ivar2+",IEQ,"+var1+","+var2+")"
                tuples.append("Tuple is("+ivar2+",IEQ,"+var1+","+var2+")")
            else:
                print "Tuple is("+ivar2+",REQ,"+var1+","+var2+")" 
                tuples.append("Tuple is("+ivar2+",REQ,"+var1+","+var2+")" )  
            semantic_stack[-3] = ivar2
    elif red == '81':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-3]
        var2 = semantic_stack[-1]
        if findtype(var1) == "I" and findtype(var2) == "R":
            ivar1 = getrealintermed()
            print "Tuple is("+ivar1+",CONVERTITOR,"+var1+",#)"
            tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+var1+",#)")
            var1 = ivar1
        ivar2 = getboointermed()
        if findtype(var1) == "I":
            print "Tuple is("+ivar2+",INE,"+var2+","+var1+")"
            tuples.append("Tuple is("+ivar2+",INE,"+var2+","+var1+")")
        else:
            print "Tuple is("+ivar2+",RNE,"+var2+","+var1+")"   
            tuples.append("Tuple is("+ivar2+",RNE,"+var2+","+var1+")"  )
        semantic_stack[-3] = ivar2
    elif red == '83':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-1]
        var2 = semantic_stack[-3]
        if findtype(var2) == "I" and findtype(var1) == "R":
            ivar1 = getrealintermed()
            print "Tuple is("+ivar1+",CONVERTITOR,"+var2+",#)"
            tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+var2+",#)")
            var2 = ivar1
        if findtype(var1) == "I" and findtype(var2) == "I":
            ivar2 = getintintermed()
            print "Tuple is("+ivar2+",IADD,"+var2+","+var1+")"
            tuples.append("Tuple is("+ivar2+",IADD,"+var2+","+var1+")")
        else:
            ivar2 = getrealintermed()
            print "Tuple is("+ivar2+",RADD,"+var2+","+var1+")"   
            tuples.append("Tuple is("+ivar2+",RADD,"+var2+","+var1+")")
        semantic_stack[-3] = ivar2
    elif red == '84':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-1]
        var2 = semantic_stack[-3]
        if findtype(var2) == "I" and findtype(var1) == "R":
            ivar1 = getrealintermed()
            print "Tuple is("+ivar1+",CONVERTITOR,"+var2+",#)"
            tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+var2+",#)")
            var2 = ivar1
        if findtype(var1) == "I" and findtype(var2) == "I":
            ivar2 = getintintermed()
            print "Tuple is("+ivar2+",ISUB,"+var2+","+var1+")"
            tuples.append("Tuple is("+ivar2+",ISUB,"+var2+","+var1+")")
        else:
            ivar2 = getrealintermed()
            print "Tuple is("+ivar2+",RSUB,"+var2+","+var1+")"  
            tuples.append("Tuple is("+ivar2+",RSUB,"+var2+","+var1+")")
        semantic_stack[-3] = ivar2 
    elif red == '85':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-1]
        var2 = "0"
        if findtype(var2) == "I" and findtype(var1) == "R":
            ivar1 = getrealintermed()
            print "Tuple is("+ivar1+",CONVERTITOR,"+var2+",#)"
            tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+var2+",#)")
            var2 = ivar1
        if findtype(var1) == "I" and findtype(var2) == "I":
            ivar2 = getintintermed()
            print "Tuple is("+ivar2+",ISUB,"+var2+","+var1+")"
            tuples.append("Tuple is("+ivar2+",ISUB,"+var2+","+var1+")")
        else:
            ivar2 = getrealintermed()
            print "Tuple is("+ivar2+",RSUB,"+var2+","+var1+")" 
            tuples.append("Tuple is("+ivar2+",RSUB,"+var2+","+var1+")") 
        semantic_stack[-2] = ivar2 
    elif red == '87':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        #check for mixed mode arith
        var1 = semantic_stack[-1]
        var2 = semantic_stack[-3]
        if findtype(var2) == "I" and findtype(var1) == "R":
            ivar1 = getrealintermed()
            print "Tuple is("+ivar1+",CONVERTITOR,"+var2+",#)"
            tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+var2+",#)")
            var2 = ivar1
        if findtype(var1) == "I" and findtype(var2) == "I":
            ivar2 = getintintermed()
            print "Tuple is("+ivar2+",IMUL,"+var2+","+var1+")"
            tuples.append("Tuple is("+ivar2+",IMUL,"+var2+","+var1+")")
        else:
            ivar2 = getrealintermed()
            print "Tuple is("+ivar2+",RMUL,"+var2+","+var1+")" 
            tuples.append("Tuple is("+ivar2+",RMUL,"+var2+","+var1+")")  
        semantic_stack[-3] = ivar2         
    elif red == '88':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        var1 = semantic_stack[-1]
        var2 = semantic_stack[-3]
        if findtype(var2) == "I" and findtype(var1) == "R":
            ivar1 = getrealintermed()
            print "Tuple is("+ivar1+",CONVERTITOR,"+var2+",#)"
            tuples.append("Tuple is("+ivar1+",CONVERTITOR,"+var2+",#)")
            var2 = ivar1
        if findtype(var1) == "I" and findtype(var2) == "I":
            ivar2 = getintintermed()
            print "Tuple is("+ivar2+",IDIV,"+var2+","+var1+")"
            tuples.append("Tuple is("+ivar2+",IDIV,"+var2+","+var1+")")
        else:
            ivar2 = getrealintermed()
            print "Tuple is("+ivar2+",RDIV,"+var2+","+var1+")"   
            tuples.append("Tuple is("+ivar2+",RDIV,"+var2+","+var1+")"  )
        semantic_stack[-3] = ivar2
    elif red == '90':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        semantic_stack[-3] = semantic_stack[-2]
    elif red == '91':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        #PERFORM ERROR CHECKING 
        # CHECK IF VAR IS IN THE SYMB TABLE 
        chk_flag = False
        var = semantic_stack[-6]
        i = semantic_stack[-4]
        j = semantic_stack[-2]
        succflag = False
        if in_proc_flag:
            if chklocsymtab(var):
                succflag = True
            elif chkglosymtab(var):
                succflag = True
        elif chkglosymtab(var):
            succflag = True
            
#        if chklocsymtab(var) or chkglosymtab(var):
        if succflag:
            #check for the shape to be matrix
            row = getstentry(var)
            if row['Shape'] == "matrix":
                #check for indices type to be integer
                if i[0] == "I" and i[1] == "$":
                    chk_flag = True
                elif i.isdigit():
                    chk_flag = True
                elif getstentry(i)['Type'] == "INTEGER":
                    chk_flag = True
        if chk_flag == True:
            ivar1 = getintintermed()
            ivar2 = getintintermed()
            print "Tuple is(" +ivar1+ ",IMULT," +row['Cols']+ "," +i+ ")"
            print "Tuple is(" +ivar2+ ",IADD," +ivar1+ "," +j+ ")" 
            tuples.append("Tuple is(" +ivar1+ ",IMULT," +row['Cols']+ "," +i+ ")")
            tuples.append("Tuple is(" +ivar2+ ",IADD," +ivar1+ "," +j+ ")" )
            if row['Type'] == "INTEGER":
                ivar3 = getintintermed()
            elif row['Type'] == "REAL":
                ivar3 = getrealintermed()
            print "Tuple is(" +ivar3+ ",SUBLOAD," +var+ "," +ivar2+ ")"
            tuples.append("Tuple is(" +ivar3+ ",SUBLOAD," +var+ "," +ivar2+ ")")
            semantic_stack[-6] = ivar3
    elif red == '92':
        if flags["12"] == "on":
            print "Semantic_ stack is " + str(semantic_stack)
        #PERFORM ERROR CHECKING 
        # CHECK IF VAR IS IN THE SYMB TABLE 
        chk_flag = False
        var = semantic_stack[-4]
        i = semantic_stack[-2]
        succflag = False
        if in_proc_flag:
            if chklocsymtab(var):
                succflag = True
            elif chkglosymtab(var):
                succflag = True
        elif chkglosymtab(var):
            succflag = True
           
        if succflag:
            #check for the shape to be matrix
            row = getstentry(var)
            if row['Shape'] == "vector":
                if i[0] == "I" and i[1] == "$":
                    chk_flag = True
                elif i.isdigit():
                    chk_flag = True
                elif getstentry(i)['Type'] == "INTEGER":
                    chk_flag = True
        if chk_flag == True:
            if row['Type'] == "INTEGER":
                ivar1 = getintintermed()
            elif row['Type'] == "REAL":
                ivar1 = getrealintermed()
            print "Tuple is(" +ivar1+ ",SUBLOAD," +var+ "," +i+ ")"
            tuples.append("Tuple is(" +ivar1+ ",SUBLOAD," +var+ "," +i+ ")")
            semantic_stack[-4] = ivar1

def pragmatics(tuples):
    print "Inside pragmatics"       
    datasegment = []
    bsssegment = []
    asmcode = []
    codingsection = []
    subpgmsection = []
    temp = []
    
    # push the initial contents of the ASM program
    code = "; Code generated by Pragmatics program"
    asmcode.append(code)
    asmcode.append("%include \"asm_io.inc\"")
    datasegment.append("segment .data")
    bsssegment.append("segment .bss")
    codingsection.append("segment .text")
    codingsection.append("        extern  printf")
    codingsection.append("        global  asm_main")
    codingsection.append("asm_main:")
    codingsection.append("        enter   0,0               ; setup routine")
    codingsection.append("        pusha")
    #for tuple1 in tuples:
        #print tuple1 
    ftuples = []
    t = []
    for tuple1 in tuples:
        #tuple1 = tuple1.lstrip("(")
        #print tuple1
        tuple1 = tuple1[tuple1.find("(")+1:-1]
        t = tuple1.split(",")
        ftuples.append(t)  
    #for t in ftuples:
    #    print t 
    pgmbeginflag = False
    pgmendflag = False
    # from the beginning of the tuples until ENDDECLARATIONS
    for t in ftuples:
        #print t[1]
        if t[1] == "PROGRAMBEGIN":
            pgmbeginflag = True
        elif t[1] == "ENDDECLARATIONS":
            pgmendflag = True
        elif pgmbeginflag == True and pgmendflag == False and t[1] == "MEMORY":
            bsssegment.append(t[0]+ "  resd "+t[2])
#    print bsssegment
#    for t in ftuples:
#        print t 
    # search for MAIN
    mainflag = False
    printflag = False
    procedurecallflag = False
    try:
        for t in ftuples:
            if mainflag == True:
                codingsection.append(";     "+str(t))
            if t[0] == "MAIN":
                mainflag = True
            
            elif mainflag == True and t[1] == "ASSIGN":
                if t[2].find("$") != -1:
                    t[2] = freereg(t[2])
                
                codingsection.append("        mov     dword ["+t[0]+"], "+t[2])
            elif mainflag == True and t[1] == "SUBASSIGN":
                iflag = False
                if t[2].find("$") != -1:
                    t[2] = freereg(t[2])
                    iflag = True
                if t[3].find("$") == -1 and t[3].isdigit() == False:
                    codingsection.append("        mov     eax, ["+t[3]+"]")
                elif t[3].find("$") != -1:
                    a = freereg(t[3])
                    codingsection.append("        mov     eax, "+a)
                else:
                    codingsection.append("        mov     eax, "+t[3])
                codingsection.append("        imul    eax, 4")
                if iflag == False and t[2].isdigit() == False:
                    if t[2][0] == "-":
                        codingsection.append("        mov     dword ["+t[0]+" + eax], "+t[2])
                    else:
                        a = getreg("temp") # get a free register and allocate
                        #print "inside Tuple is " +str(t)
                        codingsection.append("        mov     "+a+", ["+t[2]+"]")
                        codingsection.append("        mov     dword ["+t[0]+" + eax], "+a)
                        freereg("temp")
                else:
                    codingsection.append("        mov     dword ["+t[0]+" + eax], "+t[2])
            
            elif t[1] == "CALL" and t[2] == "printf" and mainflag == True :
                printflag = True
            elif mainflag == True and t[1] == "LABEL" and t[0].find("$") != -1:
                codingsection.append(t[0]+":") 
            elif mainflag == True and t[1] in ["ILT","IGT"]:
#                if t[2].find("$") != -1:
#                    freereg(t[2])
#                if t[3].find("$") != -1:
#                    freereg(t[3])
                if t[3].isdigit() == True:
                    b = t[3]
                elif t[3].find("$") != -1:
                    b = freereg(t[3])
                else:
                    b = "["+t[3]+"]"
                if t[2].find("$") != -1:
                    a = freereg(t[2])
                else:
                    a = "["+t[2]+"]"
                if b.isdigit() == True:
                    codingsection.append("        cmp   dword "+a+", "+b)
                else:
                    codingsection.append("        cmp        "+a+", "+b)
            elif mainflag == True and t[1] == "CJUMP":
                codingsection.append("        jg  "+t[0])
            elif mainflag == True and t[1] == "CJUMPF":
                codingsection.append("        jl  "+t[0])
            elif mainflag == True and t[1] == "JUMP":
                codingsection.append("        jmp   "+t[0])
            elif mainflag == True and t[1] == "ISUB" and t[3].find("$") == -1:
                codingsection.append("        mov     eax, "+t[2])
                codingsection.append("        sub    eax, ["+t[3]+"]")
                codingsection.append("        mov     "+getreg(t[0])+", eax") 
            elif mainflag == True and t[1] == "IADD" and t[3].find("$") == -1:
                print str(t)
                if t[3].isdigit() == True:
                    b = t[3]
                else:
                    b = "["+b+"]"
                if t[2].find("$") == -1 and t[2].isdigit() == False:
                    codingsection.append("        mov     eax, ["+t[2]+"]")
                else:
                    codingsection.append("        mov     eax, "+t[2])
                codingsection.append("        add    eax, "+b)
                codingsection.append("        mov     "+getreg(t[0])+", eax") 
            elif mainflag == True and t[1] == "SUBLOAD":
                print str(t)
                if t[3].find("$") != -1:
                    freereg(t[3])
                if t[3].find("$") == True:
                    codingsection.append("        mov     eax, "+getreg(t[3]))
                else:
                    if t[3].isdigit() == True:
                        codingsection.append("        mov     eax,  "+t[3])
                    else:
                        codingsection.append("        mov     eax, ["+t[3]+"]")
                codingsection.append("        imul    eax, 4")
                codingsection.append("        mov     eax, ["+t[2]+" + eax]")
                codingsection.append("        mov     "+getreg(t[0])+", eax")                   
            elif mainflag  == True and printflag == True and t[1] == "OUTPUTPARAMETER":
                if t[2].find(" ")!= -1:
                    outvar = getoutvarname()
                    datasegment.append(outvar+" db    "+t[2]+", 10, 0")
                    #codingsection.append("        mov     eax, "+outvar)
                    #codingsection.append("        call    print_string")
                    temp.append("        push    "+outvar)
                    temp.append("        call     printf")
                    temp.append("        add      esp, 8")
                else:
                    codingsection.append("        push     dword ["+t[2]+"]")
                    #codingsection.append("        call    print_string")
                    for line in temp:
                        codingsection.append(line)
                    temp = [] 
            elif mainflag  == True and printflag == True and t[1] == "OUTPUTSUBPARAMETER":
                codingsection.append("        mov     eax, "+t[3])
                codingsection.append("        imul     eax, 4")
                codingsection.append("        push     dword ["+t[2]+"+ eax]")
                if temp != []:
                    for line in temp:
                        codingsection.append(line)
                    temp = [] 
            elif mainflag == True and printflag == True and t[0] == "printf" and t[1] == "ENDOUTPARAMETERS":
    
                printflag = False
            elif mainflag == True and t[0] != "#" and t[1] == "CALL" and t[2] == "#":
                procedurecallflag = True
                label = getretlabelname()
                codingsection.append("        mov     esi, "+label)
                codingsection.append("        jmp     short "+t[0])    
                codingsection.append(label+":")
            elif mainflag == True and t[0] != "#" and t[1] == "ENDACTUALPARAMETERLIST":
                procedurecallflag = False
            elif mainflag == True and t[1] == "FLAG":
                global reg
                codingsection.append(";     "+str(reg)) 
            elif mainflag == True and t[1] == "ENDPROGRAM":
                mainflag = False
                codingsection.append("        popa")
                codingsection.append("        mov     eax, 0            ; return back to C")
                codingsection.append("        leave")
                codingsection.append("        ret")
        # handling for procedures to be appended after main 
        inprocflag = False
        procname = ""
        paramflag = False
        valueflag = False
        refflag = False
        defflag = True
        refstatus = {}
        regdict = {}
        for t in ftuples:
            if inprocflag == True:
                subpgmsection.append(";     "+str(t))
            if t[1] == "BEGINPROCEDURE":
                inprocflag = True
                procname = t[0]
                subpgmsection.append(t[0]+":")
            elif inprocflag == True and t[1] == "BEGINPARAMETERLIST":
                paramflag = True
            elif inprocflag == True and paramflag == True and t[1] == "FORMALvaluePARAMETER":
                #subpgmsection.append("        mov     ecx, ["+t[0]+"]")  
                valueflag = True
                regdict[t[0]] = "ecx"
            elif inprocflag == True and paramflag == True and t[1] == "FORMALreferencePARAMETER":
                refflag = True
                defflag = False
                refstatus[t[0]] = True
            elif inprocflag == True and t[1] == "ENDPARAMETERLIST":
                paramflag = False
            elif inprocflag == True and t[1] == "IADD" and t[3].find("$") == -1:
                #print str(t)
                global r
                if t[3].isdigit() == True:
                    b = t[3]
                if t[2].find("$") == -1 and t[2].isdigit() == False:
                    if t[2] not in refstatus:
                        subpgmsection.append("        mov     eax, "+r)
                    else:     
                        subpgmsection.append("        mov     eax, ["+t[2]+"]")
                else:
                    subpgmsection.append("        mov     eax, "+t[2])
                subpgmsection.append("        add    eax, "+b)
                subpgmsection.append("        mov     "+getreg(t[0])+", eax")             
            elif inprocflag == True and t[1] == "ISUB" and t[3].find("$") == -1:
                subpgmsection.append("        mov     eax, ["+t[2]+"]")
                subpgmsection.append("        sub    eax, "+t[3])
                subpgmsection.append("        mov     "+getreg(t[0])+", eax")             
            elif inprocflag == True and t[1] in ["ILT","IGT"]:
#                if t[2].find("$") != -1:
#                    freereg(t[2])
#                if t[3].find("$") != -1:
#                    freereg(t[3])
                if t[3].isdigit() == True:
                    b = t[3]
                elif t[3].find("$") != -1:
                    b = freereg(t[3])
                else:
                    b = "["+t[3]+"]"
                if t[2].find("$") != -1:
                    a = freereg(t[2])
                else:
                    a = "["+t[2]+"]"
                if b.isdigit() == True:
                    subpgmsection.append("        cmp   dword "+a+", "+b)
                else:
                    subpgmsection.append("        cmp        "+a+", "+b)            
            elif inprocflag == True and t[0] != "#" and t[1] == "CALL" and t[2] == "#":
                #procedurecallflag = True
                #label = getretlabelname()
                #subpgmsection.append("        mov     esi, "+label)
                subpgmsection.append("        jmp     short "+t[0])    
                #subpgmsection.append(label+":")            
            elif inprocflag == True and t[1] == "LABEL" and t[0].find("$") != -1:
                subpgmsection.append(t[0]+":")             
            elif inprocflag == True and t[1] == "ASSIGN":
                #print str(t)
                global r
                print t[0] in refstatus
                print valueflag
                print refflag
                if t[2].find("$") != -1:
                    t[2] = freereg(t[2])                
                if t[0] not in refstatus and valueflag == False:
                    r = getreg(t[0])
                    regdict[t[0]] = r
                    subpgmsection.append("        mov     "+r+", "+t[2])
                    
                elif valueflag == True:
                    subpgmsection.append("        mov     "+regdict[t[0]]+", "+t[2])
                elif refflag == True:
                    subpgmsection.append("        mov      dword ["+t[0]+"], "+t[2])
            elif t[1] == "CALL" and t[2] == "printf" and inprocflag == True :
                printflag = True
            elif inprocflag == True and t[1] == "CJUMPF":
                subpgmsection.append("        jl  "+t[0])
            elif inprocflag  == True and printflag == True and t[1] == "OUTPUTPARAMETER":
                if t[2].find(" ")!= -1:
                    outvar = getoutvarname()
                    datasegment.append(outvar+" db    "+t[2]+", 10, 0")
                    temp.append("        push    "+outvar)
                    temp.append("        call     printf")
                    temp.append("        add      esp, 8")
                else:
                    if t[2] not in refstatus:
                        subpgmsection.append("        push     "+regdict[t[2]])
                    elif valueflag == True:
                        subpgmsection.append("        push     "+regdict[t[2]]) 
                    elif refflag == True:
                        subpgmsection.append("        push      dword["+t[2]+"]")
                    for line in temp:
                        subpgmsection.append(line)
                    temp = []                 
            elif inprocflag == True and printflag == True and t[0] == "printf" and t[1] == "ENDOUTPARAMETERS":
                printflag = False   
            elif inprocflag == True and t[1] == "FLAG":
                global reg
                subpgmsection.append(";     "+str(reg))     
            elif inprocflag == True and t[1] == "ENDPROCEDURE" and t[0] == procname:
                subpgmsection.append("        jmp     esi ") 
                inprocflag = False
    except:
        #print "error"
        raise
    

    for data in asmcode:
        print data
    for data in datasegment:
        print data
    for data in bsssegment:
        print data
    for code in codingsection:
        print code  
    for code in subpgmsection:
        print code
    
    
    
                                               
if __name__ == '__main__':
    main()
    