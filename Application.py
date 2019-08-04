import tkinter as tk
from ErbFileManager import *
from EraTranslator import *
from MainList import *
from Config import config

#import pysnooper

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

        #re get pattern
        translatePattern = config.getPattern("TranslatePattern")
        ignorePattern = config.getPattern("IgnorePattern")
        self.obtain = re.compile(translatePattern)
        self.ignore = re.compile(ignorePattern, re.U)

        #saved mark
        self.saved = True

        #translated mark
        self.mark = config.get('mark', 'value')

        self.eraTranslator = EraTranslator()
        self.erbFileManager = ErbFileManager()
        
        #define function
        self.translate = self.eraTranslator.translate
        self.encodeFolder = self.erbFileManager.encodeFolder
        self.setTranslateParams = self.eraTranslator.setTranslateParams
        self.stopTranslate = self.eraTranslator.stopTranslate

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
            text = self.obtain.search(content[i])
            if not text:
                continue

            text = list(filter(None, text.groups()))[0]
            if self.ignore.search(content[i]) == None:
                #check translated info
                if i < len(content) - 1:
                    nextList = content[i + 1].strip().split(' ')

                translated = None
                if self.mark in nextList:
                    translated = text
                    origin = ' '.join(nextList[1:]).strip()
                else:
                    origin = text

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
            
            #set saved marker
            self.saved = True
        except:
            print(self.textDict)
            print(self.originLineNumber)

    #set translate text dict
    def setTranslatedText(self, o, t):
        if o in self.textDict:
            if self.textDict[o] != t:
                self.textDict[o] = t
                self.saved = False
        else:
            print(o, " Not Found")
             
    def getOriginList(self):
        return list(self.textDict.keys())

    def getTranslatedList(self):
        return list(self.textDict.values())

    def getTextDictValue(self, origin):
        return self.textDict[origin]

    def isEverythingSaved(self):
        return self.saved

    ########################
    ### find and replace ###
    ########################
    #@pysnooper.snoop()
    def findNext(self, current, text, dir):
        ori = self.getOriginList()
        trans = self.getTranslatedList()
        length = len(trans)

        i = current + 1 if dir else current - 1
        i = (i + length)%length
        
        while i != current:
            if text in ori[i]:
                return i
            elif text in trans[i]:
                return i

            i = i + 1 if dir else i - 1
            if i >= length or i < 0:
                i = (i + length)%length
        
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
