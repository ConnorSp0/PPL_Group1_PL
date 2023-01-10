DIGITS = "0123456789"      #Character Sets Comparisons
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
OSYMBOLS = "_*=+\.,/%&|>()[]{<}~!@#$^&\'\""
IDLIST = DIGITS + LETTERS + "_"

class Lexer:
    def __init__(self, text, ongoingMulti_):  #Constructor
        self.douBoolPass = None
        self.text = text
        self.pos = -1
        self.current_char = None
        self.ongoingMulti = ongoingMulti_
        self.advance()

    def advance(self):   #Reads Next Character
        self.lastpos = self.pos
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None #Return "None" if last character

    def StringChk(self): #String Checking
        endQt = 0
        stringTxt = ''
        self.advance()
        while self.current_char != None:  #Collects characters inside of double-quotations
            if self.current_char == "\"":
                endQt = 1
                self.tokens.append(['\"', '\"'])
                self.tokens.append([stringTxt, 'STRING'])  #Create tokens
                self.tokens.append(['\"', '\"'])
            else:
                stringTxt += self.current_char
            self.advance()
        if endQt == 0: 
            stringTxt = "\"" + stringTxt
            self.tokens.append([stringTxt, 'INVALID']) #No Closing double-quotations

    def CharChk(self): #Character Checking
        if self.current_char == "\'":      #Not yet fixed
            stringTxt = ''
            self.advance()
            while self.current_char != '\'':
                stringTxt += self.current_char
                self.advance()
            if len(stringTxt) == 1:
                self.tokens.append([stringTxt, 'CHAR'])
            else:
                self.tokens.append([stringTxt, 'INVALID'])
            if self.current_char == "'": self.tokens.append(["'", "'"])
            self.advance()
        else:
            self.tokens.append([self.current_char, 'CHAR'])
            self.advance()


        if self.current_char == '\'': self.tokens.append(['\'', '\'']) #Empty Character Declaration
        else: 
            if self.current_char != None: #Character Declared
                self.tokens.append([self.current_char, 'CHAR'])
                self.advance()
                if self.current_char == '\'': self.tokens.append(['\'', '\'']) #Closing single-quotation 


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
            self.tokens.append(['<', '<'])
            self.advance()
        elif self.current_char == ">": 
            self.tokens.append(['>', '>'])
            self.advance()
        elif self.current_char == "=":
            self.tokens.append(['=', '='])
            self.advance()
        elif self.current_char == "!":
            self.tokens.append(['!', 'UNRECOGNIZED'])
            self.advance()
        elif self.current_char == "/":
            self.tokens.append(['/', '/'])
            self.advance()
        elif self.current_char == "+":
            self.tokens.append(['+', '+'])
            self.advance()
        elif self.current_char == "-":
            self.tokens.append(['-', '-'])
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
                        self.tokens.append(['...', 'MCOMMENT_O'])
                        self.FMultiCmnt()
                    else:               #Single-Line Comment detected
                        self.tokens.append(['..', 'SCOMMENT'])
                        self.SinglCmnt()
                else:   #Single dot 
                    self.tokens.append(['.', 'UNRECOGNIZED'])

            elif self.douBoolPass == 1:  #Boolean Operation Creation
                self.douBoolPass = 0
                if self.current_char == "=":  #"Or Equal" to Boolean Operators
                    if lastChar == "<":
                        self.tokens.append(['<=', '<='])
                    elif lastChar == ">":
                        self.tokens.append(['>=', '>='])
                    elif lastChar == "=":
                        self.tokens.append(['==', '=='])
                    elif lastChar == "!":
                        self.tokens.append(['!=', '!='])
                    self.advance()
                else:
                    self.SingleOpe()    #Single Boolean Operators

            elif self.divPass == 1: #Division Operators
                self.divPass = 0
                if self.current_char == "/":
                    self.tokens.append(['//', '//'])
                    self.advance()
                else:
                    self.SingleOpe()

            elif self.addPass == 1:  #Addition Symbol Detected
                self.addPass = 0
                if lastChar == "+" and self.current_char == "=":      
                    self.tokens.append(['+=', '+=']) #Addition Assignment Operator
                    self.advance()
                else: self.SingleOpe()  #Addition Operator

            elif self.subPass  == 1: #Subtraction Symbol Detected
                self.subPass = 0
                if lastChar == "-" and self.current_char == "=": 
                    self.tokens.append(['-=', '-=']) #Subtraction Assignment Operator
                    self.advance()
                else: self.SingleOpe() #Subtraction Operator

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
            self.tokens.append([cmntTxt, 'COMMENT'])  #Makes Comment token
            self.advance()

    def FMultiCmnt(self): #Multi-Line Comment Checking
        try:
            self.current_char = self.text[self.pos + 2]   
        except IndexError:   #No succeeding Comments 
            self.ongoingMulti = 1   #Multi-line not closed
            self.advance()
        else:       
            self.pos += 2     #Starting Adjustments
            self.SMultiCmnt()   #Pass collected Comment

    def SMultiCmnt(self):  #Main Creation of multi-line Comments  
        cmntText = ''      
        end = 0
        max = len(self.text)
        try:
            while self.pos < max:  #Collects all characters
                if self.current_char == "." and self.text[self.pos + 1] == "." and self.text[self.pos + 2] == ".":  #Closed Multi-Line Comment 
                    if self.pos != 0 and cmntText !='': self.tokens.append([cmntText, 'COMMENT'])
                    self.tokens.append(['...', 'MCOMMENT_c'])            
                    self.pos += 2
                    end=1
                else:  
                    cmntText += self.current_char
                self.advance()
        except IndexError: #text reading almost finished
            while self.pos < max:  
                cmntText += self.current_char
                self.advance()
            self.tokens.append([cmntText, 'COMMENT'])
            self.ongoingMulti = 1   #Multi-Line C not closed
        else:
            if end != 1: #Multi-Line C not closed
                self.tokens.append([cmntText, 'COMMENT'])
                self.ongoingMulti = 1 
            else:       #Multi-Line closed
                self.ongoingMulti = 0
                print("Pos:", self.pos)

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
            elif self.douBoolPass == 1 or self.divPass == 1 or self.dotPass == 1 or self.addPass == 1 or self.subPass == 1:  #Probable Double Operator detected
                if self.dotPass ==1 and self.current_char in DIGITS: self.tokens.append(self.make_Number())
                else: self.DoubleOpeChk()
            elif self.current_char == '+':
                self.addPass = 1
                self.advance()
            elif self.current_char == '-':                           #Single Character Detection
                self.subPass = 1
                self.advance()
            elif self.current_char == '*':
                self.tokens.append(['*', '*'])
                self.advance()
            elif self.current_char == '/':    #Division Operator Detected
                self.divPass = 1
                self.advance()
            elif self.current_char == '%':
                self.tokens.append(['%', '%'])
                self.advance()
            elif self.current_char in '<>=!': #Boolean Operator Detected
                self.douBoolPass = 1
                self.advance()
            elif self.current_char == '.':    #Probable Comment Detected
                self.dotPass = 1
                self.advance()
            elif self.current_char == '^':
                self.tokens.append(['^', '^'])
                self.advance()
            elif self.current_char == '(':
                self.tokens.append(['(', '('])
                self.advance()
            elif self.current_char == ')':
                self.tokens.append([')', ')'])
                self.advance()
            elif self.current_char == '[':
                self.tokens.append(['[', '['])
                self.advance()
            elif self.current_char == ']':
                self.tokens.append([']', ']'])
                self.advance()
            elif self.current_char == ',':
                self.tokens.append([',', ','])
                self.advance()
            elif self.current_char == ';':
                self.tokens.append([';', ';'])
                self.advance()
            elif self.current_char == "\"":     #String Detected
                self.StringChk()
            elif self.current_char == "\'":     #Character Detected
                self.tokens.append(['\'', '\''])
                self.advance()
                self.CharChk()
            elif self.current_char in DIGITS:   #Digits Detected 
                self.tokens.append(self.make_Number())
            elif self.current_char in LETTERS:  #Letters Detected
                self.tokens.append(self.make_Word())
            elif self.current_char in OSYMBOLS: 
                self.tokens.append([self.current_char,'UNRECOGNIZED'])
                self.advance()
            else:
                self.advance()

        if self.douBoolPass == 1 or self.divPass == 1 or self.dotPass == 1 or self.addPass==1 or self.subPass==1: 
            self.DoubleOpeChk()#Unresolved Operator
        
        for i in self.tokens:   #Output Tokens
            print(f'{i[0]: <20}{i[1]}')

        return self.tokens, self.ongoingMulti   #Give Tokens to Object

    def make_Number(self):   #Integer or Float Creation
        num_str = ''
        dot_count = 0
        if self.dotPass ==1:
            self.pos -= 2
            self.advance()
            self.dotPass = 0
        while self.current_char != None and self.current_char in DIGITS + '.':  #Collection of Numerical Characters
            if self.current_char == '.':   #Float Detected
                dot_count += 1
                try:
                    if self.text[self.pos+1] == ".": break
                except IndexError: pass
            num_str += self.current_char
            self.advance()

        if dot_count == 0:   #Output
            return ([int(num_str), 'INTEGER'])
        elif dot_count == 1:
            return ([float(num_str), 'FLOAT'])
        else: 
            return ([num_str, 'INVALID'])

    def make_Identifier(self, key_str):  #Makes Identifiers
        invalid = 0
        while self.current_char != None and self.current_char not in " \t" :  #Terminates if space detected
            if self.current_char in OSYMBOLS and self.current_char != "_": #Checks invalid Characters
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
                    return (["at", 'LOGICAL'])
                else: return self.make_Identifier("at")
            elif self.current_char == 'y':
                self.advance()
                if self.current_char == None or self.current_char in " \t":
                    return (["ay", 'NOISE_WORD'])
                else: return self.make_Identifier("ay")
            else: return self.make_Identifier("a")

        elif self.current_char == 'o':   #oh Logical Operator
            self.advance()
            if self.current_char == 'h':
                self.advance()
                if self.current_char == None or self.current_char in " \t":
                    return (["oh", 'LOGICAL'])
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
                                return (["hindi", 'LOGICAL'])
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
                                    return (["habang", 'KEYWORD'])
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
                    if self.current_char == None or self.current_char in " \t":  #edi Keyword
                        return (["edi", 'KEYWORD'])
                    elif self.current_char == 'k':
                        self.advance()
                        if self.current_char == 'u':
                            self.advance()
                            if self.current_char == 'n':
                                self.advance()
                                if self.current_char == 'g':
                                    self.advance()
                                    if self.current_char == None or self.current_char in " \t":   #edikung Keyword
                                        return (["edikung", 'KEYWORD'])
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
                                    if self.current_char == None or self.current_char in " \t":   #ilimbag Keyword
                                        return (["ilimbag", 'KEYWORD'])
                                    elif self.current_char == 's':
                                        self.advance()
                                        if self.current_char == None or self.current_char in " \t":   #ilimbags Keyword
                                            return (["ilimbags", 'KEYWORD'])
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
                                    return (["ilabas", 'RESERVED_WORD'])
                                else: return self.make_Identifier("ilabas")
                            else: return self.make_Identifier("ilaba")
                        else: return self.make_Identifier("ilab")
                    else: return self.make_Identifier("ila")          
                else: return self.make_Identifier("il")
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
                                if self.current_char == None or self.current_char in " \t":  #lagyan Keyword
                                    return (["lagyan", 'KEYWORD'])
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
                                                return (["labasmuna", 'RESERVED_WORD'])
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
                                    return (["lutang", 'RESERVED_WORD'])
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
                                    return (["numero", 'RESERVED_WORD'])
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
                                    return (["salita", 'RESERVED_WORD'])
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
                                return (["subok", 'RESERVED_WORD'])
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
                                    return (["simula", 'NOISE_WORD'])
                                else: return self.make_Identifier("simula")
                            else: return self.make_Identifier("simul")
                        else: return self.make_Identifier("simu")
                    else: return self.make_Identifier("sim")
                if self.current_char == 'r':
                    self.advance()
                    if self.current_char == 'a':
                        self.advance()
                        if self.current_char == None or self.current_char in " \t":    #sira Reserved Word
                            return (["sira", 'RESERVED_WORD'])
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
                                             return (["karakter", 'RESERVED_WORD'])
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
                                    return (["kabtol", 'RESERVED_WORD'])
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
                                                        return (["kaunaunahan", 'NOISE_WORD'])
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
                                                                return (["kaduluduluhan", 'NOISE_WORD'])
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
                        if self.current_char == None or self.current_char in " \t":   #kung Reserved Word
                            return (["kung", 'RESERVED_WORD'])
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
                                return (["klase", 'RESERVED_WORD'])
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
                        return (["bul", 'RESERVED_WORD'])
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
                            if self.current_char == None or self.current_char in " \t":    #totoo Reserved Word
                                return (["totoo", 'RESERVED_WORD'])
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
                                return (["tuloy", 'RESERVED_WORD'])
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
                        if self.current_char == None or self.current_char in " \t":    #mali Reserved Word
                            return (["mali", 'RESERVED_WORD'])
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
                                            return (["pindutan", 'RESERVED_WORD'])
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
                                    return (["puwera", 'RESERVED_WORD'])
                                else: return self.make_Identifier("puwera")
                            else: return self.make_Identifier("puwer")
                        else: return self.make_Identifier("puwe")
                    else: return self.make_Identifier("puw")
                elif self.current_char == 'n': 
                    self.advance()
                    if self.current_char == 'a': 
                        self.advance()
                        if self.current_char == None or self.current_char in " \t":   #puna Noise Word
                            return (["puna", 'NOISE_WORD'])
                        else: return self.make_Identifier("puna")
                    else: return self.make_Identifier("pun")          
                else: return self.make_Identifier("pu") 
            elif self.current_char == 'a': 
                self.advance()
                if self.current_char == 'l': 
                    self.advance()    
                    if self.current_char == None or self.current_char in " \t":     #pal Reserved Word
                        return (["pal", 'RESERVED_WORD'])
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
                            return (["wala", 'RESERVED_WORD'])
                        else: return self.make_Identifier("wala")   
                    else: return self.make_Identifier("wal")
                elif self.current_char == 'k':
                    self.advance()
                    if self.current_char == 'a':
                        self.advance()
                        if self.current_char == 's':
                            self.advance()
                            if self.current_char == None or self.current_char in " \t":    #wakas Noise Word
                                return (["wakas", 'NOISE_WORD'])
                            else: return self.make_Identifier("wakas")
                        else: return self.make_Identifier("waka")
                    else: return self.make_Identifier("wak")
                else: return self.make_Identifier("wa")
            else: return self.make_Identifier("w")   

        else: return self.make_Identifier("")
        
def run(text, multiLine):         #Starts Program
    lexer = Lexer(text, multiLine)
    result = lexer.make_Tokens()

    return result      #Give Tokens to Object