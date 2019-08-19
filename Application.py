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

        #contains origin and translated sentence
        self.textDict = {}

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
        self.textDict.clear()

        self.erbFileManager.setAddress(address)
        self.erbFileManager.readFile()
        self.textDict = self.erbFileManager.getSentence()
    
    def saveFile(self):
        self.erbFileManager.saveFile(self.textDict)
        self.saved = True

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

    def clearAllTranslated(self):
        for key in self.textDict:
            self.textDict[key] = ""

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


    #save dictionary
    def saveDictionary(self):
        self.erbFileManager.saveDictionary(self.textDict)

    def loadFromDictionary(self, address):
        dictdata = self.erbFileManager.readDictionary(address)
        for key in self.textDict:
            if key in dictdata:
                self.textDict[key] = dictdata[key]


if __name__ == '__main__':
    a = Application()
    a.run()
