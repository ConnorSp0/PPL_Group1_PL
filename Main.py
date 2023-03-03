import Lexer_Klak, os, Syntax
from tkinter import filedialog

dirPath = os.path.dirname(os.path.realpath(__file__))
outputPath = dirPath + '/Symbol_Table.txt'  #Output File

def Start(): #Starts Program
    inputPath = filedialog.askopenfilename(initialdir=dirPath, title="Choose Klak File",   #Klak File Choosing
                                     filetypes=(("Klak File","*.klk"),))
    try:
        file = open(inputPath, 'r')
    except IOError as error:
        print(f"Error: {error}")
        print("Klak File does not exist")
        exit(0)
    else:
        print("=================================")
        ongoingMulti = 0
        line = file.readline() 
        while line  != "":                  #Reads File per Line
            line = line.replace("\n","")
            tempList = Lexer_Klak.run(line, ongoingMulti)    
            ongoingMulti = tempList
            line = file.readline()
        file.close()
        outfile = open(outputPath, "a")  #Write ending design
        outfile.close()
        print("\n_Klak Lexer Process Complete_")
        print("=================================")  #Ending Design
        # Runs Syntax Analyzer
        Syntax.start()
        print("\n_Klak Syntax Analyzer Process Complete_")
        print("=================================")  #Ending Design

Start()  #Starts Program