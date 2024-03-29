import os

DIGITS = "0123456789"      #Character Sets Comparisons
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
OSYMBOLS = "_*=+\.,/%&|>()[]{<}~!@#$^&\'\""
OPE = "-*+,//%()^"
ROPERATORS = ['<=', '>=', '<', '>', '!=', '==']
IDLIST = DIGITS + LETTERS + "_"

dirPath = os.path.dirname(os.path.realpath(__file__))
outputPath = dirPath + '/Symbol_Table.txt'            
fileStart = False

class Lexer:
    def __init__(self, text, ongoingMulti_):  #Constructor
        self.douBoolPass = None
        self.text = text
        self.pos = -1
        self.current_char = None
        self.ongoingMulti = ongoingMulti_
        self.outfile = ''
        self.advance()
       
        

    def advance(self):   #Reads Next Character
        self.lastpos = self.pos
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None #Return "None" if last character

    def writeSymbolTable(self, lexeme):   #Output File Creation
        global fileStart
        start = ["LEXEME", "TOKEN"]
        if fileStart == False:
            outfile = open(outputPath, "w") 
            outfile.write(f'{start[0]: <40}{start[1]}\n')  
            outfile.write('=======================================================================\n')  
            fileStart = True
        else: outfile = open(outputPath, "a") 
        outfile.write(f'{lexeme[0]: <40}{lexeme[1]}\n')  
        outfile.close()
        return

    
    def StringChk(self): #String Checking
        endQt = 0
        stringTxt = '\"'
        self.advance()
        while self.current_char != None:  #Collects characters 
            if self.current_char == "\"":    #End Quotation Detected
                endQt = 1
                stringTxt += "\""
                self.writeSymbolTable([stringTxt, 'STRING']) 
                self.advance()
                break
            else:
                stringTxt += self.current_char
            self.advance()
        if endQt == 0:      #No end Quotation
            self.writeSymbolTable([stringTxt, 'INVALID']) #No Closing double-quotations

    def CharChk(self): #Character Checking
        endQt = 0
        stringTxt = '\''
        self.advance()
        while self.current_char != None:
            if self.current_char == '\'':
                endQt = 1
                stringTxt += '\''
                if len(stringTxt) == 3 or len(stringTxt) == 2:           #1 Character
                    self.writeSymbolTable([stringTxt, 'CHARACTER'])
                    self.advance()
                    return
                else: 
                    self.writeSymbolTable([stringTxt, 'INVALID'])
            else:
                stringTxt += self.current_char
            self.advance()
        if endQt == 0: 
            self.writeSymbolTable([stringTxt, 'INVALID']) #No Closing single-quotation

    def SingleOpe(self): #Single-Digit Operation Checking
        singleCharPos = 0                                                      
        if self.lastpos == len(self.text)-1: self.current_char = self.text[self.lastpos]  #If One character only or last character reached 
        else:
            singleCharPos = self.pos - 1
            self.current_char = self.text[singleCharPos]
            while self.current_char in ' \t':  #Goes back to the symbol
                singleCharPos -= 1
                self.current_char = self.text[singleCharPos]
        self.pos = singleCharPos
        if self.current_char == "<":  #Single Operators token creation
            self.writeSymbolTable(['<', '<'])
            self.advance()
        elif self.current_char == ">": 
            self.writeSymbolTable(['>', '>'])
            self.advance()
        elif self.current_char == "=":
            self.writeSymbolTable(['=', '='])
            self.advance()
        elif self.current_char == "!":
            self.writeSymbolTable(['!', 'UNRECOGNIZED'])
            self.advance()
        elif self.current_char == "/":
            self.writeSymbolTable(['/', '/'])
            self.advance()

    def DoubleOpeChk(self):  #Double-Digit Operation Checking
        try:
            lastChar = self.text[self.pos - 1]  
        except IndexError:   #One-Digit Operator
            self.SingleOpe()
        else:
            if self.dotPass == 1:    #Comments Creation
                self.dotPass = 0
                if self.current_char == ".":
                    lastChar = self.text[self.pos + 1]
                    if lastChar == ".":  #Multi-Line Comment detected
                        self.writeSymbolTable(['...', 'MCOMMENT_O'])
                        self.FMultiCmnt()
                    else:               #Single-Line Comment detected
                        self.writeSymbolTable(['..', 'SCOMMENT'])
                        self.SinglCmnt()
                else:   #Single dot 
                    self.writeSymbolTable(['.', 'UNRECOGNIZED'])

            elif self.douBoolPass == 1:  #Boolean Operation Creation
                self.douBoolPass = 0
                if self.current_char == "=":  #"Or Equal" to Boolean Operators
                    if lastChar == "<":
                        self.writeSymbolTable(['<=', '<='])
                    elif lastChar == ">":
                        self.writeSymbolTable(['>=', '>='])
                    elif lastChar == "=":
                        self.writeSymbolTable(['==', '=='])
                    elif lastChar == "!":
                        self.writeSymbolTable(['!=', '!='])
                    self.advance()
                else:
                    self.SingleOpe()    #Single Boolean Operators

            elif self.divPass == 1: #Division Operators
                self.divPass = 0
                if self.current_char == "/":
                    self.writeSymbolTable(['//', '//'])
                    self.advance()
                else:
                    self.SingleOpe()

            
    def SinglCmnt(self):   #Single-Line Comment Checking
        max = len(self.text)
        cmntTxt = ''
        if (self.pos + 1) == max - 1:  #No Comment inputted
            self.advance()
        else:
            self.advance()
            while self.pos < max:      #Collects Succeeding Characters
                cmntTxt += self.current_char
                self.advance()
            self.writeSymbolTable([cmntTxt, 'COMMENT'])  #Makes Comment token
            self.advance()

    def FMultiCmnt(self): #Multi-Line Comment Checking
        try:
            self.current_char = self.text[self.pos + 2]   
        except IndexError:   #No succeeding Comments 
            self.ongoingMulti = 1   #Multi-line not closed
            self.advance()
            self.advance()
        else:       
            self.pos += 1     #Starting Adjustments
            self.advance()
            self.SMultiCmnt()   #Pass collected Comment
            

    def SMultiCmnt(self):  #Main Creation of multi-line Comments  
        cmntText = ''      
        end = 0
        max = len(self.text)
        try:
            while self.pos < max:  #Collects all characters
                if self.current_char == "." and self.text[self.pos + 1] == "." and self.text[self.pos + 2] == ".":  #Closed Multi-Line Comment 
                    if self.pos != 0 and cmntText !='': self.writeSymbolTable([cmntText, 'COMMENT'])
                    self.writeSymbolTable(['...', 'MCOMMENT_C'])            
                    self.pos += 2
                    end=1
                else:  
                    cmntText += self.current_char
                self.advance()
        except IndexError: #text reading almost finished
            while self.pos < max:  
                cmntText += self.current_char
                self.advance()
            self.writeSymbolTable([cmntText, 'COMMENT'])
            self.ongoingMulti = 1   #Multi-Line C not closed
        else:
            if end != 1: #Multi-Line C not closed
                self.writeSymbolTable([cmntText, 'COMMENT'])
                self.ongoingMulti = 1 
            else:       #Multi-Line closed
                self.ongoingMulti = 0
    
    def make_Invalid(self):
        strTxt = ""
        try:
            while self.current_char not in " \t":   #Collects Group of Uncrecognized
                strTxt += self.current_char
                self.advance()
        except TypeError: pass    #Detects end of line
        self.writeSymbolTable([strTxt,'UNRECOGNIZED'])

    def make_Tokens(self):   #Creates Tokens
        self.tokens = []
        self.douBoolPass = 0  #Declaration of needed Variables
        self.divPass = 0
        self.dotPass = 0
        self.addPass = 0
        self.subPass = 0

        while self.current_char != None: #Loops until end of text
            if self.ongoingMulti == 1:  #Multi-Line C not closed
                self.SMultiCmnt()
                self.advance()
            elif self.current_char in ' \t': #Spaces detected
                self.advance()
            elif self.douBoolPass == 1 or self.divPass == 1 or self.dotPass == 1:  #Probable Double Operator detected
                if self.dotPass ==1 and self.current_char in DIGITS: self.writeSymbolTable(self.make_Number())
                else: self.DoubleOpeChk()
            elif self.current_char == '+':
                self.writeSymbolTable(['+', '+'])
                self.advance()
            elif self.current_char == '-':  
                self.writeSymbolTable(['-', '-'])    #Single Character Detection
                self.advance()
            elif self.current_char == '*':
                self.writeSymbolTable(['*', '*'])
                self.advance()
            elif self.current_char == '/':      #Division Operator Detected
                self.divPass = 1
                self.advance()
            elif self.current_char == '%':
                self.writeSymbolTable(['%', '%'])
                self.advance()
            elif self.current_char in '<>=!': #Boolean Operator Detected
                self.douBoolPass = 1
                self.advance()
            elif self.current_char == '.':    #Probable Comment Detected
                self.dotPass = 1
                self.advance()
            elif self.current_char == '^':
                self.writeSymbolTable(['^', '^'])
                self.advance()
            elif self.current_char == '(':
                self.writeSymbolTable(['(', '('])
                self.advance()
            elif self.current_char == ')':
                self.writeSymbolTable([')', ')'])
                self.advance()
            elif self.current_char == '[':
                self.writeSymbolTable(['[', '['])
                self.advance()
            elif self.current_char == ']':
                self.writeSymbolTable([']', ']'])
                self.advance()
            elif self.current_char == ',':
                self.writeSymbolTable([',', ','])
                self.advance()
            elif self.current_char == ';':
                self.writeSymbolTable([';', ';'])
                self.advance()
            elif self.current_char == "\"":     #String Detected
                self.StringChk()
            elif self.current_char == "\'":     #Character Detected
                self.CharChk()
            elif self.current_char in DIGITS:   #Digits Detected 
                self.writeSymbolTable(self.make_Number())
            elif self.current_char in LETTERS:  #Letters Detected
                self.writeSymbolTable(self.make_Word())
            elif self.current_char in OSYMBOLS: 
                self.make_Invalid()
            else:
                self.make_Invalid()

        if self.douBoolPass == 1 or self.divPass == 1 or self.dotPass == 1 or self.addPass==1 or self.subPass==1: 
            self.DoubleOpeChk()#Unresolved Operator
        
        return self.ongoingMulti   #Give Tokens to Object

    def make_Number(self):   #Integer or Float Creation
        num_str = ""
        dot_count = 0
        is_Invalid = False
        if self.dotPass ==1:
            self.pos -= 2
            self.advance()
            self.dotPass = 0
        while self.current_char != None and self.current_char not in ' \n\t':  #Collection of Numerical Characters
            if not(self.current_char in DIGITS or self.current_char == '.'):    #Check if not Digits or '.'
                if self.current_char in OPE  + ";[": break
                is_Invalid = True
            if self.current_char == '.':   #Float Detected
                dot_count += 1
                try: 
                    if self.text[self.pos+1] == ".": break
                except IndexError: pass
            
            num_str += self.current_char
            self.advance()
        if dot_count == 0 and is_Invalid == False:   #Output
            return [int(num_str), 'INTEGER']
        elif dot_count == 1 and is_Invalid == False:
            return [float(num_str), 'FLOAT']
        else: 
            return ([num_str, 'INVALID'])

    def make_Identifier(self, key_str):  #Makes Identifiers
        invalid = 0
        while self.current_char != None and self.current_char not in " \t;" :  #Terminates if space detected
            if self.current_char in OSYMBOLS and self.current_char != "_": #Checks invalid Characters
                if self.current_char in "()[],=" or self.current_char in ROPERATORS or self.current_char in OPE: break
                invalid = 1 
                if self.current_char in "\'\"":   #Character or String start indication
                    invalid=0
                    break
                elif self.current_char ==".":  
                    try:
                        if self.text[self.pos+1] == ".": break  #Comment indication
                    except IndexError: pass 
            key_str += self.current_char  #Collects Characters
            self.advance()
        
        if invalid ==0: return ([key_str, 'ID']) #Output
        else: return ([key_str, 'INVALID']) 

    def make_Word(self):  #Built-in Function Checking

        if self.current_char == 'a':     #at Logical Operator and ay Noise Word
            self.advance()
            if self.current_char == 't':
                self.advance()
                if self.current_char == None or self.current_char in " \t":
                    return (["at", 'at'])
                else: return self.make_Identifier("at")
            elif self.current_char == 'y':
                self.advance()
                if self.current_char == None or self.current_char in " \t":
                    return (["ay", 'ay'])
                else: return self.make_Identifier("ay")
            else: return self.make_Identifier("a")

        elif self.current_char == 'o':   #oh Logical Operator
            self.advance()
            if self.current_char == 'h':
                self.advance()
                if self.current_char == None or self.current_char in " \t":
                    return (["oh", 'oh'])
                else: return self.make_Identifier("oh")
            else: return self.make_Identifier("o")

        elif self.current_char == 'h':         #hindi Logical Operator 
            self.advance()
            if self.current_char == 'i':
                self.advance()
                if self.current_char == 'n':
                    self.advance()
                    if self.current_char == 'd':
                        self.advance()
                        if self.current_char == 'i':
                            self.advance()
                            if self.current_char == None or self.current_char in " \t":
                                return (["hindi", 'hindi'])
                            else: return self.make_Identifier("hindi")
                        else:  return self.make_Identifier("hind")
                    else: return self.make_Identifier("hin")
                else:return self.make_Identifier("hi")
            elif self.current_char == 'a':
                self.advance()
                if self.current_char == 'b':
                    self.advance()
                    if self.current_char == 'a':
                        self.advance()
                        if self.current_char == 'n':
                            self.advance()
                            if self.current_char == 'g':
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":   #habang Keyword
                                    return (["habang", 'habang'])
                                else: return self.make_Identifier("habang")
                            else: return self.make_Identifier("haban")
                        else: return self.make_Identifier("haba")
                    else: return self.make_Identifier("hab")
                else: return self.make_Identifier("ha")
            else: return self.make_Identifier("h")
        
        elif self.current_char == 'e':
            self.advance()
            if self.current_char == 'd':
                self.advance()
                if self.current_char == 'i':
                    self.advance()
                    if self.current_char == None or self.current_char in " \t[" :  #edi Keyword
                        return (["edi", 'edi'])
                    elif self.current_char == 'k':
                        self.advance()
                        if self.current_char == 'u':
                            self.advance()
                            if self.current_char == 'n':
                                self.advance()
                                if self.current_char == 'g':
                                    self.advance()
                                    if self.current_char == None or self.current_char in " \t":   #edikung Keyword
                                        return (["edikung", 'edikung'])
                                    else:
                                        return self.make_Identifier("edikung")
                                else:
                                    return self.make_Identifier("edikun")
                            else:
                                return self.make_Identifier("ediku")
                        else:
                            return self.make_Identifier("edik")
                    else:
                        return self.make_Identifier("edi")
                else:
                    return self.make_Identifier("ed")
            else:
                return self.make_Identifier("e")

        elif self.current_char == 'i': 
            self.advance()
            if self.current_char == 'l':
                self.advance()
                if self.current_char == 'i':
                    self.advance()
                    if self.current_char == 'm':
                        self.advance()
                        if self.current_char == 'b':
                            self.advance()
                            if self.current_char == 'a':
                                self.advance()
                                if self.current_char == 'g':
                                    self.advance()
                                    if self.current_char == None or self.current_char in " \t(":   #ilimbag Keyword
                                        return (["ilimbag", 'ilimbag'])
                                    elif self.current_char == 's':
                                        self.advance()
                                        if self.current_char == None or self.current_char in " \t(":   #ilimbags Keyword
                                            return (["ilimbags", 'ilimbags'])
                                        else: return self.make_Identifier("ilimbags")
                                    else: return self.make_Identifier("ilimbag")
                                else: return self.make_Identifier("ilimba")
                            else: return self.make_Identifier("ilimb")
                        else: return self.make_Identifier("ilim")    
                    else: return self.make_Identifier("ili")
                elif self.current_char == 'a': 
                    self.advance()
                    if self.current_char == 'b': 
                        self.advance()
                        if self.current_char == 'a': 
                            self.advance()
                            if self.current_char == 's': 
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":   #ilabas Reserved Word
                                    return (["ilabas", 'ilabas'])
                                else: return self.make_Identifier("ilabas")
                            else: return self.make_Identifier("ilaba")
                        else: return self.make_Identifier("ilab")
                    else: return self.make_Identifier("ila")          
                else: return self.make_Identifier("il")
            elif self.current_char == 'k':
                self.advance()
                if self.current_char == 'o':
                    self.advance()
                    if self.current_char == 't':
                        self.advance()
                        if self.current_char == None or self.current_char in " \t(":   #ilimbag Keyword
                            return (["ikot", 'ikot'])
                        else: return self.make_Identifier("ikot")
                    else: return self.make_Identifier("iko")       
                else: return self.make_Identifier("ik")
            else: return self.make_Identifier("i")

        elif self.current_char == 'l':
            self.advance()
            if self.current_char == 'a':
                self.advance()
                if self.current_char == 'g':
                    self.advance()
                    if self.current_char == 'y':
                        self.advance()
                        if self.current_char == 'a':
                            self.advance()
                            if self.current_char == 'n':
                                self.advance()
                                if self.current_char == None or self.current_char in " \t();":  #lagyan Keyword
                                    return (["lagyan", 'lagyan'])
                                else: return self.make_Identifier("lagyan")
                            else: return self.make_Identifier("lagya")
                        else: return self.make_Identifier("lagy")
                    else: return self.make_Identifier("lag")
                elif self.current_char == 'b': 
                    self.advance()
                    if self.current_char == 'a': 
                        self.advance()
                        if self.current_char == 's': 
                            self.advance()
                            if self.current_char == 'm': 
                                self.advance()
                                if self.current_char == 'u': 
                                    self.advance()
                                    if self.current_char == 'n': 
                                        self.advance()
                                        if self.current_char == 'a': 
                                            self.advance()
                                            if self.current_char == None or self.current_char in " \t":   #labasmuna Reserved Word
                                                return (["labasmuna", 'labasmuna'])
                                            else: return self.make_Identifier("labasmuna")
                                        else: return self.make_Identifier("labasmun")
                                    else: return self.make_Identifier("labasmu")
                                else: return self.make_Identifier("labasm")
                            else: return self.make_Identifier("labas")
                        else: return self.make_Identifier("laba")
                    else: return self.make_Identifier("lab")          
                else: return self.make_Identifier("la")
            elif self.current_char == 'u':  
                self.advance()
                if self.current_char == 't':
                    self.advance()
                    if self.current_char == 'a':
                        self.advance()
                        if self.current_char == 'n':
                            self.advance()
                            if self.current_char == 'g':
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":   #lutang Reserved Word
                                    return (["lutang", 'lutang'])
                                else: return self.make_Identifier("lutang")
                            else: return self.make_Identifier("lutan")
                        else: return self.make_Identifier("luta")
                    else: return self.make_Identifier("lut")
                else: return self.make_Identifier("lu")         
            else: return self.make_Identifier("l")

        elif self.current_char == 'n':
            self.advance()
            if self.current_char == 'u':
                self.advance()
                if self.current_char == 'm':
                    self.advance()
                    if self.current_char == 'e':
                        self.advance()
                        if self.current_char == 'r':
                            self.advance()
                            if self.current_char == 'o':
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":   #numero Reserved Word
                                    return (["numero", 'numero'])
                                else: return self.make_Identifier("numero")
                            else: return self.make_Identifier("numer")
                        else: return self.make_Identifier("nume")
                    else: return self.make_Identifier("num")
                else: return self.make_Identifier("nu")
            else: return self.make_Identifier("n")

        elif self.current_char == 's':
            self.advance()
            if self.current_char == 'a':
                self.advance()
                if self.current_char == 'l':
                    self.advance()
                    if self.current_char == 'i':
                        self.advance()
                        if self.current_char == 't':
                            self.advance()
                            if self.current_char == 'a':
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":    #salita Reserved Word
                                    return (["salita", 'salita'])
                                else: return self.make_Identifier("salita")
                            else: return self.make_Identifier("salit")
                        else: return self.make_Identifier("sali")
                    else: return self.make_Identifier("sal")
                else: return self.make_Identifier("sa")
            elif self.current_char == 'u':
                self.advance()
                if self.current_char == 'b':
                    self.advance()
                    if self.current_char == 'o':
                        self.advance()
                        if self.current_char == 'k':
                            self.advance()
                            if self.current_char == None or self.current_char in " \t":   #subok Reserved Word
                                return (["subok", 'subok'])
                            else: return self.make_Identifier("subok")
                        else: return self.make_Identifier("subo")
                    else: return self.make_Identifier("sub")
                else: return self.make_Identifier("su")   
            elif self.current_char == 'i':
                self.advance()
                if self.current_char == 'm':
                    self.advance()
                    if self.current_char == 'u':
                        self.advance()
                        if self.current_char == 'l':
                            self.advance()
                            if self.current_char == 'a':
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":   #simula Noise Word
                                    return (["simula", 'simula'])
                                else: return self.make_Identifier("simula")
                            else: return self.make_Identifier("simul")
                        else: return self.make_Identifier("simu")
                    else: return self.make_Identifier("sim")
                if self.current_char == 'r':
                    self.advance()
                    if self.current_char == 'a':
                        self.advance()
                        if self.current_char == None or self.current_char in " \t":    #sira Reserved Word
                            return (["sira", 'sira'])
                        else: return self.make_Identifier("sira")
                    else: return self.make_Identifier("sir")
                else: return self.make_Identifier("si")
            else: return self.make_Identifier("s")

        elif self.current_char == 'k': 
            self.advance()
            if self.current_char == 'a':   
                self.advance()
                if self.current_char == 'r':
                    self.advance()
                    if self.current_char == 'a':
                        self.advance()
                        if self.current_char == 'k':
                            self.advance()
                            if self.current_char == 't':
                                self.advance()
                                if self.current_char == 'e':
                                    self.advance()
                                    if self.current_char == 'r':
                                        self.advance()
                                        if self.current_char == None or self.current_char in " \t":  #karakter Reserved Word
                                             return (["karakter", 'karakter'])
                                        else: return self.make_Identifier("karakter")
                                    else: return self.make_Identifier("karakte")
                                else: return self.make_Identifier("karakt")
                            else: return self.make_Identifier("karak")
                        else: return self.make_Identifier("kara")
                    else: return self.make_Identifier("kar")
                elif self.current_char == 'b': 
                    self.advance()
                    if self.current_char == 't': 
                        self.advance()
                        if self.current_char == 'o': 
                            self.advance()
                            if self.current_char == 'l': 
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":  #kabtol Reserved Word
                                    return (["kabtol", 'kabtol'])
                                else: return self.make_Identifier("kabtol")
                            else: return self.make_Identifier("kabto")
                        else: return self.make_Identifier("kabt")
                    else: return self.make_Identifier("kab")
                elif self.current_char == 'u': 
                    self.advance()
                    if self.current_char == 'n': 
                        self.advance()
                        if self.current_char == 'a': 
                            self.advance()
                            if self.current_char == 'u': 
                                self.advance()
                                if self.current_char == 'n': 
                                    self.advance()
                                    if self.current_char == 'a': 
                                        self.advance()
                                        if self.current_char == 'h': 
                                            self.advance()
                                            if self.current_char == 'a': 
                                                self.advance()
                                                if self.current_char == 'n': 
                                                    self.advance()
                                                    if self.current_char == None or self.current_char in " \t":   #kaunaunahan Noise Word
                                                        return (["kaunaunahan", 'kaunaunahan'])
                                                    else: return self.make_Identifier("kaunaunahan")
                                                else: return self.make_Identifier("kaunaunaha") 
                                            else: return self.make_Identifier("kaunaunah")       
                                        else: return self.make_Identifier("kaunauna")             
                                    else: return self.make_Identifier("kaunaun")                
                                else: return self.make_Identifier("kaunau")
                            else: return self.make_Identifier("kauna")
                        else: return self.make_Identifier("kaun")
                    else: return self.make_Identifier("kau")
                elif self.current_char == 'd': 
                    self.advance()
                    if self.current_char == 'u': 
                        self.advance()
                        if self.current_char == 'l': 
                            self.advance()
                            if self.current_char == 'u': 
                                self.advance()
                                if self.current_char == 'd': 
                                    self.advance()
                                    if self.current_char == 'u': 
                                        self.advance()
                                        if self.current_char == 'l': 
                                            self.advance()
                                            if self.current_char == 'u': 
                                                self.advance()
                                                if self.current_char == 'h': 
                                                    self.advance()
                                                    if self.current_char == 'a': 
                                                        self.advance()
                                                        if self.current_char == 'n': 
                                                            self.advance()
                                                            if self.current_char == None or self.current_char in " \t":  #kaduluduluhan Noise Word
                                                                return (["kaduluduluhan", 'kaduluduluhan'])
                                                            else: return self.make_Identifier("kaduluduluhan")    
                                                        else: return self.make_Identifier("kaduluduluha")
                                                    else: return self.make_Identifier("kaduluduluh")
                                                else: return self.make_Identifier("kaduludulu") 
                                            else: return self.make_Identifier("kaduludul")       
                                        else: return self.make_Identifier("kaduludu")             
                                    else: return self.make_Identifier("kadulud")                
                                else: return self.make_Identifier("kadulu")
                            else: return self.make_Identifier("kadul")
                        else: return self.make_Identifier("kadu")
                    else: return self.make_Identifier("kad")
                else: return self.make_Identifier("ka")
            elif self.current_char == 'u': 
                self.advance()
                if self.current_char == 'n': 
                    self.advance()
                    if self.current_char == 'g': 
                        self.advance()
                        if self.current_char == None or self.current_char in " \t" :   #kung Reserved Word
                            return (["kung", 'kung'])
                        else: return self.make_Identifier("kung")  
                    else: return self.make_Identifier("kun")          
                else: return self.make_Identifier("ku")
            elif self.current_char == 'l': 
                self.advance()
                if self.current_char == 'a': 
                    self.advance()
                    if self.current_char == 's': 
                        self.advance()
                        if self.current_char == 'e': 
                            self.advance()
                            if self.current_char == None or self.current_char in " \t":    #klase Reserved Word
                                return (["klase", 'klase'])
                            else: return self.make_Identifier("klase")  
                        else: return self.make_Identifier("klas")          
                    else: return self.make_Identifier("kla")
                else: return self.make_Identifier("kl")
            else: return self.make_Identifier("k")

        elif self.current_char == 'b':
            self.advance()
            if self.current_char == 'u':
                self.advance()
                if self.current_char == 'l':
                    self.advance()
                    if self.current_char == None or self.current_char in " \t":   #bul Reserved Word
                        return (["bul", 'bul'])
                    else: return self.make_Identifier("bul")
                else: return self.make_Identifier("bu")
            else: return self.make_Identifier("b")

        elif self.current_char == 't':
            self.advance()
            if self.current_char == 'o':
                self.advance()
                if self.current_char == 't':
                    self.advance()
                    if self.current_char == 'o':
                        self.advance()
                        if self.current_char == 'o':
                            self.advance()
                            if self.current_char == None or self.current_char in " \t;)":    #totoo Reserved Word
                                return (["totoo", 'totoo'])
                            else: return self.make_Identifier("totoo")
                        else: return self.make_Identifier("toto")
                    else: return self.make_Identifier("tot")
                else: return self.make_Identifier("to")
            elif self.current_char == 'u': 
                self.advance()
                if self.current_char == 'l': 
                    self.advance()
                    if self.current_char == 'o': 
                        self.advance()
                        if self.current_char == 'y': 
                            self.advance()
                            if self.current_char == None or self.current_char in " \t":    #tuloy Reserved Word
                                return (["tuloy", 'tuloy'])
                            else: return self.make_Identifier("tuloy")
                        else: return self.make_Identifier("tulo")
                    else: return self.make_Identifier("tul")          
                else: return self.make_Identifier("tu")
            else: return self.make_Identifier("t")

        elif self.current_char == 'm':
            self.advance()
            if self.current_char == 'a':
                self.advance()
                if self.current_char == 'l':
                    self.advance()
                    if self.current_char == 'i':
                        self.advance()
                        if self.current_char == None or self.current_char in " \t);":    #mali Reserved Word
                            return (["mali", 'mali'])
                        else: return self.make_Identifier("mali")
                    else: return self.make_Identifier("mal")
                else: return self.make_Identifier("ma")
            else: return self.make_Identifier("m")

        elif self.current_char == 'p': 
            self.advance()
            if self.current_char == 'i': 
                self.advance()
                if self.current_char == 'n': 
                    self.advance()
                    if self.current_char == 'd': 
                        self.advance()
                        if self.current_char == 'u': 
                            self.advance()
                            if self.current_char == 't': 
                                self.advance()
                                if self.current_char == 'a': 
                                    self.advance()
                                    if self.current_char == 'n': 
                                        self.advance()
                                        if self.current_char == None or self.current_char in " \t":   #pindutan Reserved Word
                                            return (["pindutan", 'pindutan'])
                                        else: return self.make_Identifier("pindutan")
                                    else: return self.make_Identifier("pinduta")
                                else: return self.make_Identifier("pindut")
                            else: return self.make_Identifier("pindu")
                        else: return self.make_Identifier("pind")
                    else: return self.make_Identifier("pin")          
                else: return self.make_Identifier("pi")
            elif self.current_char == 'u': 
                self.advance()
                if self.current_char == 'w': 
                    self.advance()
                    if self.current_char == 'e': 
                        self.advance()
                        if self.current_char == 'r': 
                            self.advance()
                            if self.current_char == 'a': 
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":  #puwera Reserved Word
                                    return (["puwera", 'puwera'])
                                else: return self.make_Identifier("puwera")
                            else: return self.make_Identifier("puwer")
                        else: return self.make_Identifier("puwe")
                    else: return self.make_Identifier("puw")
                elif self.current_char == 'n': 
                    self.advance()
                    if self.current_char == 'a': 
                        self.advance()
                        if self.current_char == None or self.current_char in " \t":   #puna Noise Word
                            return (["puna", 'puna'])
                        else: return self.make_Identifier("puna")
                    else: return self.make_Identifier("pun")          
                else: return self.make_Identifier("pu") 
            elif self.current_char == 'a': 
                self.advance()
                if self.current_char == 'l': 
                    self.advance()    
                    if self.current_char == None or self.current_char in " \t":     #pal Reserved Word
                        return (["pal", 'pal'])
                    else: return self.make_Identifier("pal")  
                else: return self.make_Identifier("pa") 
            else: return self.make_Identifier("p")

        elif self.current_char == 'w': 
            self.advance()
            if self.current_char == 'a': 
                self.advance()
                if self.current_char == 'l': 
                    self.advance()
                    if self.current_char == 'a': 
                        self.advance()
                        if self.current_char == None or self.current_char in " \t":    #wala Reserved Word
                            return (["wala", 'wala'])
                        else: return self.make_Identifier("wala")   
                    else: return self.make_Identifier("wal")
                elif self.current_char == 'k':
                    self.advance()
                    if self.current_char == 'a':
                        self.advance()
                        if self.current_char == 's':
                            self.advance()
                            if self.current_char == None or self.current_char in " \t":    #wakas Noise Word
                                return (["wakas", 'wakas'])
                            else: return self.make_Identifier("wakas")
                        else: return self.make_Identifier("waka")
                    else: return self.make_Identifier("wak")
                else: return self.make_Identifier("wa")
            else: return self.make_Identifier("w")   

        else: return self.make_Identifier("")
        
def run(text, multiLine):         #Starts Program
    lexer = Lexer(text, multiLine)
    list = lexer.make_Tokens()

    return list     #Give Tokens to Object