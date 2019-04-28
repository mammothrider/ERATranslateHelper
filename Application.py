import tkinter as tk
from ErbFileManager import *
from EraTranslator import *
from MainList import *
import Config

import pysnooper

class Application:
    
    def __init__(self, core=None):
        self.tkRoot = tk.Tk()
        self.core = core
        self.app = MainList(master = self.tkRoot, core = self)

        #origin line number in file
        self.originLineNumber = {}
        self.origin = []

        #contains origin and translated sentence
        self.textDict = {}

        #translated mark
        self.mark = Config.get('mark', 'value')

        self.eraTranslator = EraTranslator()
        self.erbFileManager = ErbFileManager()
        
        #define function
        self.translate = self.eraTranslator.translate
        self.encodeFolder = self.erbFileManager.encodeFolder
    
    def run(self):
        self.app.mainloop()

    def openFile(self, address):
        #init
        self.originLineNumber.clear()
        self.textDict.clear()

        self.erbFileManager.setAddress(address)
        content = self.erbFileManager.readFile()
        self.getSentence(content)

    #get sentence from file
    def getSentence(self, content):
        #printList = [ "PRINTFORMW", "PRINTFORML", "PRINTFORM", "PRINTL", "PRINTW", "PRINT", "DATAFORM"]

        for i in range(len(content)):
            text = content[i].strip()
            if text.startswith("PRINT") or text.startswith("DATA"):
                #remove print command
                tmpList = text.split(' ')
                #check first word
                #if tmpList[0] not in printList:
                #    continue

                #not empty line
                if len(tmpList) > 1:
                    #find marker
                    translated = ''
                    origin = ''
                    #check translated info
                    if i < len(content) - 1:
                        nextList = content[i + 1].strip().split(' ')
                    
                    if self.mark in nextList:
                        translated = ' '.join(tmpList[1:])
                        origin = ' '.join(nextList[1:]).strip()
                    else:
                        origin = ' '.join(tmpList[1:]).strip()

                    #check dict existance
                    if origin not in self.originLineNumber:
                       self.originLineNumber[origin] = []
                    self.originLineNumber[origin] += [i]

                    #add to translate list
                    self.textDict[origin] = translated
        print("Total: ", len(self.textDict))
    
    def saveFile(self):
        try:
            for k in self.textDict:
                #have content
                if self.textDict[k] != '':
                    #translated text + mark + origin
                    trans = self.textDict[k]
                    #for multiple line have same content
                    for line in self.originLineNumber[k]:
                        self.erbFileManager.replaceContent(line, k, trans)
                #replace with origin text
                else:
                    for line in self.originLineNumber[k]:
                        self.erbFileManager.replaceContent(line, k, k)
            self.erbFileManager.writeFile()
        except:
            print(self.textDict)
            print(self.originLineNumber)

    #set translate text dict
    def setTranslatedText(self, o, t):
        if o in self.textDict:
            self.textDict[o] = t
        else:
            print(o, " Not Found")
             
    def getOriginList(self):
        return list(self.textDict.keys())

    def getTranslatedList(self):
        return list(self.textDict.values())

    def getTextDictValue(self, origin):
        return self.textDict[origin]

    ########################
    ### find and replace ###
    ########################
    #@pysnooper.snoop()
    def findNext(self, current, text, dir):
        values = self.getTranslatedList()
        length = len(values)
        i = current + 1 if dir else current - 1
        while i != current:
            if i >= length or i < 0:
                i = (i + length)%length

            if text in values[i]:
                return i

            i = i + 1 if dir else i - 1
        return current

    def replaceText(self, current, text, rep):
        keys = self.getOriginList()
        values = self.getTranslatedList()
        ori = keys[current]
        tra = self.getTextDictValue(ori)
        if text in tra:
            tra = tra.replace(text, rep)
        self.setTranslatedText(ori, tra)


if __name__ == '__main__':
    a = Application()
    a.run()
