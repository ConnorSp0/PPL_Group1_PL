import os

class Parser:
    def __init__(self, ):
        self.current_Token = "Start"
        self.previous_Token = "Start"
        self.proceed = 1
        self.dataType = ['numero', 'lutang', 'karakter', 'salita', 'bul']
        self.constant = ['INTEGER', 'FLOAT', 'CHARACTER', 'STRING', 'totoo', 'mali']
        self.number = ['INTEGER', 'FLOAT']
        self.boolean = ['mali', 'totoo']
        self.id = ['ID']
        self.arithmetic = ['+', '-', '*', '/', '%', '//']
        self.conditional = ['kung', 'edikung', 'edi']
        self.relational = ['<=', '>=', '<', '>', '!=', '==']
        self.invalid = ['UNRECOGNIZED', 'INVALID']
        self.comment = ['COMMENT', 'SCOMMENT', 'MCOMMENT_O', 'MCOMMENT_C']
        self.LoopNumberings = "0123456"
        self.kungPass= 0
        self.edikungPass = 0
        self.invalidBracket = 0
        self.opnBracket = ""
        self.Forpass = 0
        self.inputTemp = 0
        self.inputEnd = 0
        self.outputEnd = 0
        self.commapass = 0

        dirPath = os.path.dirname(os.path.realpath(__file__))
        self.inputPath = dirPath + '/Symbol_Table.txt'              
        self.outputPath= dirPath + '/Parse_Table.txt' 
        self.file = open(self.inputPath, 'r')
        self.startParse()
        for i in range(0,2): self.Read_token()


    # Reads Token
    def Read_token(self):
        self.previous_Token = self.current_Token
        self.current_Token = self.file.readline()
        self.readString()
        self.current_Token = self.current_Token.strip()
    def readString(self):
        token = ""
        for i in range(len(self.current_Token)-1,-1,-1):
            if self.current_Token[i] in " \t": break
            token = self.current_Token[i] + token
        self.current_Token = token

    def startParse(self):
        file = open(self.outputPath ,'w')
        file.write("PARSE TABLE\n")
        file.write("================================================================================\n")
        file.close()

    def writeParse(self):
        file = open(self.outputPath ,'a')
        file.write(f'{self.current_Token}\n')
        file.close()

    def writeAccept(self):
        file = open(self.outputPath ,'a')
        file.write(f'ACCEPTED\n')
        file.close()

    def writeNoTerminator(self):
        file = open(self.outputPath, 'a')
        file.write(f'Syntax Error. No Terminator detected\n')
        file.close()
   
 
    #Main Function
    def mainFunction(self):
        self.Read_token()
        while len(self.current_Token) != 0:         #Checks the end of Symbol Table
            if self.current_Token in self.invalid:
                self.matchInvalid()
            elif self.current_Token == "klase":
                self.matchClass()
            elif self.current_Token == "pal":
                self.matchFunc()
            elif self.current_Token == "habang":
                self.matchWhile()
            elif self.current_Token == "ikot":
                self.matchForLoop()
            elif self.current_Token == "lagyan" or self.current_Token == "ilimbag":
                if self.current_Token == "lagyan": self.inputTemp = 1
                self.writeParse()
                self.Read_token()
                self.checkOpenParen()
                self.IOfirst()
                self.inputTemp = 0
            elif self.current_Token in self.dataType:
                self.matchDataType()
            elif self.current_Token in self.id:
                self.matchIdentifier()
            elif self.current_Token in self.conditional:
                self.matchConditional()
            elif self.current_Token == ']':
                self.matchClosingBracket()
            elif self.current_Token == ';':
                self.writeParse()
            elif self.current_Token in self.comment:
                self.writeParse()
                if self.current_Token == "SCOMMENT":
                    self.Read_token()
                    if self.current_Token == "COMMENT":
                        self.writeParse()
                        self.writeAccept()
                    else: self.proceed == 0
                elif self.current_Token == "MCOMMENT_C":
                    self.writeAccept()

            else: 
                file = open(self.outputPath, 'a')
                file.write(f'{self.current_Token}\n')
                file.write(f'Syntax Error. Invalid use of \'{self.current_Token}\'.\n')
                file.close()
            if self.proceed == 1: self.Read_token()
            self.proceed = 1
        self.chkBrackets()

    def matchInvalid(self):
        file = open(self.outputPath ,'a')
        file.write(f"Syntax Error. Invalid Input Detected\n")
        file.close()
        exit(0)
    
    def writeIDmissing(self):
        file = open(self.outputPath, 'a')
        file.write(f'Syntax Error. Identifier missing.\n')
        file.close()
        exit(0)

    def checkOpenParen(self):
        if self.current_Token == "(":
            self.writeParse()
            self.Read_token()
        else:
            file = open(self.outputPath, 'a')
            file.write(f'Syntax Error. Parentheses expected after \'{self.previous_Token}\' function.\n')
            file.close()
            exit(0)

    def checkCloseParen(self):
        if self.current_Token == ")":
            self.writeParse()
            self.Read_token()
        else:
            file = open(self.outputPath, 'a')
            file.write(f'Syntax Error. Closing Parenthesis expected after \'{self.previous_Token}\'.\n')
            file.close()
            exit(0)

    def checkExpression(self):
        while self.current_Token in self.arithmetic:
            self.writeParse()
            self.Read_token()
            if self.current_Token in self.number or self.current_Token in self.id:
                self.writeParse()
                self.Read_token()
            else:
                file = open(self.outputPath, 'a')
                file.write(f'Syntax Error. \'{self.current_Token}\' is an invalid Arithmetic Operand.\n')
                file.close()
                exit(0)

    def checkTerminator(self):
        if self.current_Token == ";":
            self.writeParse()
            self.writeAccept()
        else:
            file = open(self.outputPath, 'a')
            file.write(f'Syntax Error. Terminator expected after \'{self.previous_Token}\'.\n')
            file.close()
            exit(0)

    def IOfirst(self):
        self.matchIO()
        self.commapass = 0
        if self.inputTemp == 1:
            if self.inputEnd == 0:
                self.checkCloseParen()
                self.checkTerminator()
            self.inputTemp = 0
            self.inputEnd=0
        else:
            if self.outputEnd == 0:
                if self.current_Token == ')' :
                    self.checkCloseParen()
                    self.checkTerminator()
                else:
                    self.writeInvalidIO()
            self.outputEnd = 0
    
    def matchIO(self):
        if self.current_Token in self.number or self.current_Token in self.id:
            self.writeParse()
            self.Read_token()
            if self.current_Token in self.arithmetic:
                self.checkExpression()
            elif self.current_Token == "," and self.inputTemp == 0:
                self.nextInput()
        elif self.current_Token in self.constant:
            self.writeParse()
            self.Read_token()
            if self.current_Token == "," and self.inputTemp == 0:
                self.nextInput()
            elif self.inputTemp == 1 or (self.inputTemp == 0 and self.current_Token == ")"):
                self.checkCloseParen()
                self.checkTerminator()
                if self.inputTemp == 1: self.inputEnd = 1
                else: self.outputEnd = 1
            else:self.writeInvalidIO()
        elif self.current_Token == ")":
            if self.inputTemp == 1:
                if self.current_Token == ")":
                    self.checkCloseParen()
                    self.checkTerminator()
                    self.inputEnd = 1
                else:self.writeInvalidIO()
            else:
                file = open(self.outputPath, 'a')
                if self.commapass == 1: file.write(f'Syntax Error. Another arguement expected after \',\'.\n')
                else: file.write(f'Syntax Error. Argument must be inputted inside Output Statement.\n')
                file.close()
                exit(0)
        else:
            file = open(self.outputPath, 'a')
            if self.inputTemp == 0:file.write(f'Syntax Error. Argument expected after \'{self.previous_Token}\'.\n')
            else: file.write(f'Syntax Error. Invalid use of \'{self.current_Token}\'.\n')
            file.close()
            exit(0)
                
    def nextInput(self):
        self.commapass= 1
        self.writeParse()
        self.Read_token()
        self.matchIO()


    def writeInvalidIO(self):
        file = open(self.outputPath, 'a')
        if self.current_Token == "":
            if self.inputTemp==1: file.write(f'Syntax Error. Invalid Input Statement.\n')
            else: file.write(f'Syntax Error. Invalid Output Statement.\n')
        else:
            if self.inputTemp==1: file.write(f'Syntax Error. Invalid use of \'{self.current_Token}\' in Input Statement.\n')
            else: file.write(f'Syntax Error. Invalid use of \'{self.current_Token}\' in Output Statement.\n')
        file.close()
        exit(0)

    def matchForLoop(self):
        self.writeParse()
        self.Read_token()
        dpass= 0
        self.checkOpenParen()
        if self.current_Token == "numero" or self.current_Token == "lutang":
            self.writeParse()
            self.Read_token()
            dpass = 1
        if self.current_Token in self.id:
            self.writeParse()
            self.Read_token()
            if self.current_Token == "=":
                self.writeParse()
                self.Read_token()
                if self.current_Token in self.number or self.current_Token in self.id:
                    self.writeParse()
                    self.Read_token()
                    if self.current_Token == ",":
                        self.writeParse()
                        self.Read_token()
                        if self.current_Token in self.id:
                            self.chkCondition()
                            self.Forpass = 0
                            if self.current_Token == ')':
                                self.writeParse()
                                self.Read_token()
                                self.chkOpeningBracket()
                                self.opnBracket += str(5)
                            else:
                                file = open(self.outputPath, 'a')
                                file.write(f'Syntax Error. Parenthesis not closed.\n')
                                file.close()
                                exit(0)
                        else:
                            file = open(self.outputPath, 'a')
                            file.write(f'Syntax Error. Identifer should be used as first operand.\n')
                            file.close()
                            exit(0)
                    else:
                        file = open(self.outputPath, 'a')
                        file.write(f'Syntax Error. Delimeter \',\' missing.\n')
                        file.close()
                        exit(0)
                else:
                    file = open(self.outputPath, 'a')
                    file.write(f'Syntax Error. Wrong constant assigned: numerical constant expected.\n')
                    file.close()
                    exit(0)
            else:
                file = open(self.outputPath, 'a')
                file.write(f'Syntax Error. Identifier not initialized.\n')
                file.close()
                exit(0)
        else:
            file = open(self.outputPath, 'a')
            if dpass == 1: file.write(f'Syntax Error. Numerical variables missing.\n')
            else: file.write(f'Syntax Error. \'for loop\' Initialization missing.\n')
            file.close()
            exit(0)

    def matchClass(self):
        self.writeParse()
        self.Read_token()
        self.opnBracket += str(0)
        if self.current_Token == "ID":
            self.writeParse()
            self.Read_token()
            self.chkOpeningBracket()
        else: self.writeIDmissing()
    
    def matchFunc(self):
        self.writeParse()
        self.Read_token()
        if self.current_Token == "ID":
            self.writeParse()
            self.Read_token()
            if self.current_Token == "(":
                self.writeParse()
                self.Read_token()
                if self.current_Token in self.dataType:
                    while self.current_Token in self.dataType:
                        self.writeParse()
                        self.Read_token()
                        if self.current_Token in self.id:
                            self.writeParse()
                            self.Read_token()
                            if self.current_Token == ",":
                                self.writeParse()
                                self.Read_token()
                                if self.current_Token != self.dataType:
                                    file = open(self.outputPath, 'a')
                                    file.write(f'Syntax Error. Parameter Declaration expected.\n')
                                    file.close()
                                    exit(0)
                            else: break
                        else:self.writeIDmissing()
                    if self.current_Token == ')':
                        self.writeParse()
                        self.Read_token()
                        self.chkOpeningBracket()
                        self.opnBracket += str(1)
                    else:
                        file = open(self.outputPath, 'a')
                        file.write(f'Syntax Error. Closing Parenthesis missing.\n')
                        file.close()
                        exit(0)
                else:
                    file = open(self.outputPath, 'a')
                    file.write(f'Syntax Error. Parameter Expected.\n')
                    file.close()
                    exit(0)    
            else: self.checkOpenParen()
        else: self.writeIDmissing()

    def matchWhile(self):
        self.writeParse()
        self.Read_token()
        self.chkCondition()
        self.chkOpeningBracket()
        self.opnBracket += str(6)


    def chkCondition(self):
        if (self.current_Token in self.id or self.current_Token in self.number or self.current_Token in self.boolean) or self.Forpass == 1:
            self.writeParse()
            self.Read_token()
            if self.current_Token in self.relational:
                self.writeParse()
                self.Read_token()
                if self.current_Token in self.id or self.current_Token in self.number or self.current_Token in self.boolean:
                    self.writeParse()
                    self.Read_token()
                else:
                    file = open(self.outputPath, 'a')
                    file.write(f'{self.current_Token}\n')
                    file.write(f'Syntax Error. Condition Error: invalid right operand.\n')
                    file.close()
                    self.Read_token()
                    self.invalidBracket = 1
                    exit(0)
            else:
                file = open(self.outputPath, 'a')
                file.write(f'{self.current_Token}\n')
                file.write(f'Syntax Error. Condition Error: relational operator missing.\n')
                file.close()
                self.Read_token()
                self.invalidBracket = 1
                exit(0)
        else:
            file = open(self.outputPath, 'a')
            file.write(f'{self.current_Token}\n')
            file.write(f'Syntax Error. Condition Error: missing valid left operand.\n')
            file.close()
            self.Read_token()
            self.invalidBracket = 1
            exit(0)
    
    def chkOpeningBracket(self):
        if self.current_Token == '[':
            self.writeParse()
        else:
            file = open(self.outputPath, 'a')
            file.write(f'Syntax Error. Code Block opening missing.\n')
            file.close()
            exit(0)

    def matchConditional(self):
        self.writeParse()
        self.Read_token()
        if self.previous_Token == 'kung':
            self.chkCondition()
            self.chkOpeningBracket()
            self.opnBracket += str(2)
        elif self.previous_Token == 'edikung':
            file = open(self.outputPath, 'a')
            file.write(f'Syntax Error. A valid \'if statement\' or \'elif statement\' expected before an \'elif statement\'.\n')
            file.close()
            exit(0)
        elif self.previous_Token == 'edi':
            file = open(self.outputPath, 'a')
            file.write(f'Syntax Error. Valid \'if statement\' or \'elif statement\'  missing or not yet closed before an \'else statement\'.\n')
            file.close()
            exit(0)
    
    def matchClosingBracket(self):
        self.writeParse()
        if len(self.opnBracket) > 0:
            self.writeAccept()
            self.Read_token()
            if self.current_Token == 'edikung':
                if self.opnBracket[len(self.opnBracket)-1] == "2" or self.opnBracket[len(self.opnBracket)-1] == "3":
                    self.opnBracket = self.opnBracket[:-1]
                    self.writeParse()
                    self.Read_token()
                    self.chkCondition()
                    self.chkOpeningBracket()
                    self.opnBracket += str(3)
                else:
                    file = open(self.outputPath, 'a')
                    file.write(f'Syntax Error. Valid \'if statement\' or \'elif statement\' missing or not yet closed.\n')
                    file.close()
                    exit(0)
            elif self.current_Token == 'edi':
                if self.opnBracket[len(self.opnBracket)-1] == "2" or self.opnBracket[len(self.opnBracket)-1] == "3" :
                    self.opnBracket = self.opnBracket[:-1]
                    self.writeParse()
                    self.Read_token()
                    self.chkOpeningBracket()
                    self.opnBracket += str(4)
                else:
                    file = open(self.outputPath, 'a')
                    file.write(f'Syntax Error. Valid \'elif statement\' missing or not yet closed.\n')
                    file.close()
                    exit(0)
            elif self.opnBracket[len(self.opnBracket)-1] in self.LoopNumberings: 
                self.opnBracket = self.opnBracket[:-1]
                self.proceed = 0
            else:
                file = open(self.outputPath, 'a')
                file.write(f"Syntax Error. Invalid use of \']\'.\n")
                file.close()
                exit(0)
        else:
            file = open(self.outputPath, 'a')
            file.write(f"Syntax Error. Invalid use of \'{self.previous_Token}\'. No code blocks created to be closed.\n")
            file.close()
            exit(0)

    def chkBrackets(self):
        if len(self.opnBracket) > 0:
            file = open(self.outputPath, 'a')
            if self.opnBracket > 1: file.write(f"Syntax Error. {self.opnBracket} Square Bracket not closed.\n")
            else: file.write(f"Syntax Error. {self.opnBracket} Square Brackets not closed.\n")
            file.close() 
            exit(0)

    def matchIDcont(self, condition):
        self.writeParse()
        self.Read_token()
        if (self.current_Token in self.constant and self.current_Token == condition) or self.current_Token in self.id or (condition == self.constant and self.current_Token != "lagyan"):
            self.writeParse()
            self.Read_token()
            if self.current_Token == ";":
                self.checkTerminator()
            elif self.current_Token in self.arithmetic:
                if condition in self.number or condition == self.constant and (self.previous_Token in self.number or self.previous_Token in self.id):
                    self.checkExpression()
                else:
                    file = open(self.outputPath, 'a')
                    file.write(f'Syntax Error. \'{self.previous_Token}\' is an invalid Arithmetic Operand.\n')
                    file.close()
                    exit(0)
            else:self.checkTerminator()
        elif self.current_Token == "lagyan": self.proceed = 0
        else:
            file = open(self.outputPath, 'a')
            file.write(f'Syntax Error. \'{condition}\' expected instead of \'{self.current_Token}\'.\n')
            file.close()
            exit(0)
    
    def writeInvalidDec(self):
        file = open(self.outputPath, 'a')
        file.write(f'Syntax Error. Invalid Variable Declaration.\n')
        file.close()
        exit(0)
        
    def matchIdentifier(self):
        self.writeParse()
        self.Read_token()
        if self.current_Token == '=':
            self.matchIDcont(self.constant)
        elif self.current_Token == ';':
            self.writeParse()
            file = open(self.outputPath, 'a')
            file.write(f'Syntax Error. Invalid use of Identifier.\n')
            file.close()
            exit(0)
        else:
            file = open(self.outputPath, 'a')
            file.write(f'Syntax Error. Invalid use of Identifier.\n')
            file.close()
            self.proceed = 0
            exit(0)

    def matchDataType(self):
        index = self.dataType.index(self.current_Token)
        self.writeParse()
        self.Read_token()
        if len(self.current_Token) != 0:
            if self.current_Token in self.id:
                self.writeParse()
                self.Read_token()
                if self.current_Token == '=':
                    self.matchIDcont(self.constant[index])
                else:self.checkTerminator()
            else: self.writeInvalidDec()
        else:self.writeInvalidDec()

def start():
    parser = Parser()
    parser.mainFunction()

if __name__ == "__main__":
    import os
    start()








