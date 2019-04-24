import tkinter as tk
from tkinter import filedialog
from tkExtensions import *
from ErbFileManager import *
from EraTranslator import *
from Editor import *
import Config

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
        return self.textDict.keys()

    def getTranslatedList(self):
        return self.textDict.values()

    def getTextDictValue(self, origin):
        return self.textDict[origin]

class MainList(tk.Frame):
    def __init__(self, master=None, core=None):
        super().__init__(master)
        self.core = core
        self.core.listWindow = self

        self.editor = None
        
        #window settings
        self.master.title("ERA Translate Helper         Create by Mammothrider")
        self.master.geometry("500x800+30+30")
        
        #create base widgets
        self.createWidgets()
    
    def createWidgets(self):
        textArea = tk.Frame(self.master)
        textArea.pack(side = 'left', fill = 'both', expand = 1)
        buttonArea = tk.Frame(self.master)
        buttonArea.pack(side = 'left', fill = 'y', expand = 0)

        self.numberList = tk.Listbox(textArea, activestyle = 'none', bg = self.master['bg'], width = 2)
        self.numberList.pack(side = 'left', fill = 'y', )

        self.originList = tk.Listbox(textArea, activestyle = 'none')
        self.originList.pack(side = 'left', fill = 'both', expand = 1)
        #no highlight color. just no need
        self.originList['highlightcolor'] = self.master['bg']
        
        #originScroll = AutoScrollbar(textArea, command = self.originList.yview)
        #originScroll.pack(side = 'left', fill = 'y', expand = 0)
        #self.originList['yscrollcommand'] = originScroll.set
        
        self.translateList = tk.Listbox(textArea, activestyle = 'none')
        self.translateList.pack(side = 'left', fill = 'both', expand = 1)
        #same
        self.translateList['highlightcolor'] = self.master['bg']
        
        #one scroll for two listbox
        def yview(*args):
            """ scroll both listboxes together """
            self.translateList.yview(*args)
            self.originList.yview(*args)
            self.numberList.yview(*args)
        def OnMouseWheel(event):
            dis = -1 if event.delta > 0 else 1
            self.originList.yview("scroll", dis,"units")
            self.translateList.yview("scroll", dis,"units")
            self.numberList.yview("scroll", dis,"units")
            # this prevents default bindings from firing, which
            # would end up scrolling the widget twice
            return "break"
        self.scroll = AutoScrollbar(textArea)
        self.scroll.pack(side = 'left', fill = 'y', expand = 0)
        self.scroll['command'] = yview
        self.translateList['yscrollcommand'] = self.scroll.set
        self.originList['yscrollcommand'] = self.scroll.set
        self.numberList['yscrollcommand'] = self.scroll.set
        self.originList.bind("<MouseWheel>", OnMouseWheel)
        self.translateList.bind("<MouseWheel>", OnMouseWheel)
        self.numberList.bind("<MouseWheel>", OnMouseWheel)

        #button
        openButton = tk.Button(buttonArea, text = 'Open File', height = 2, width = 10, command = self.openButton)
        openButton.pack(side = 'top', padx = 30, pady = 15)
        
        saveButton = tk.Button(buttonArea, text = 'Save File', height = 2, width = 10, command = self.saveButton)
        saveButton.pack(side = 'top', padx = 30, pady = 15)
        
        editButton = tk.Button(buttonArea, text = 'Edit', height = 2, width = 10, command = self.openEditorWindow)
        editButton.pack(side = 'top', padx = 30, pady = 15)

        translateButton = tk.Button(buttonArea, text = 'Translate', height = 2, width = 10, command = self.transAllText)
        translateButton.pack(side = 'top', padx = 30, pady = 15)

        encodeButton = tk.Button(buttonArea, text = 'Encode', height = 2, width = 10, command = self.encodeFolder)
        encodeButton.pack(side = 'top', padx = 30, pady = 15)

        #list bind
        self.originList.bind('<Double-Button-1>', self.openEditorWindow)
        self.translateList.bind('<Double-Button-1>', self.openEditorWindow)

    def openButton(self):
        allowType = [('ERB', '*.ERB')]
        dlg = filedialog.Open(self, filetypes = allowType)
        file = dlg.show()
        if file != '' and self.core:
            #clear all
            self.originList.delete(0, 'end')
            self.translateList.delete(0, 'end')
            
            self.core.openFile(file)
            self.refreshList()

    def encodeFolder(self):
        folder = filedialog.askdirectory()
        if folder != '' and self.core:
            self.core.encodeFolder(folder)
            
    def saveButton(self):
        self.core.saveFile()

    def openEditorWindow(self, event = None):
        if not self.editor:
            self.editor = Editor(self, self.core)
        else:
            self.editor.frame.deiconify()

        index = self.getCurrentSelection()

        try:
            self.editor.setOriginText(self.originList.get(index))
            self.editor.setTranslatedText(self.translateList.get(index))
        except:
            print(self.editor)

    def editorWindowClosed(self):
        self.editor = None

    def transAllText(self):
        for k in self.origin:
            if self.core.getTextDictValue(k) == '':
                def updateMethod(text, o = k):
                    self.core.setTranslatedText(o, text)
                    self.setTranslation(self.origin.index(o), text)
                self.core.translate(k, updateMethod)

    def getOriginPosition(self, ori):
        try:
            return self.origin.index(ori)
        except:
            print(self.origin)
            raise ValueError("Not Found In Origin")

    #no outside call. select on other window cause selection change to zero
    def getCurrentSelection(self):
        #get current selection index
        index = self.originList.curselection()
        if len(index) == 0:
            index = self.translateList.curselection()

        #if still none, return
        if len(index) == 0:
            return 0
        index = index[0]
        self.originList.selection_set(index)
        return index

    def refreshList(self):
        index = self.getCurrentSelection()

        self.refreshOriginList()
        self.refreshTranslationList()

        self.originList.selection_set(index)

    def refreshOriginList(self):
        self.origin = list(self.core.getOriginList())
        self.originList.delete(0, 'end')
        for s in self.origin:
            self.originList.insert('end', s)

        l = len(self.origin)
        x = 0
        while l > 0:
            x += 1
            l = int(l/10)
        self.numberList['width'] = x
        self.numberList.delete(0, 'end')

        for i in range(len(self.origin)):
            self.numberList.insert('end', i + 1)
    
    def refreshTranslationList(self):
        trans = self.core.getTranslatedList()
        self.translateList.delete(0, 'end')
        for s in trans:
            self.translateList.insert('end', s)
        
    def setTranslation(self, position, sentence):
        self.translateList.insert(position, sentence)
        self.translateList.delete(position + 1)

    def movePreviousItem(self, index = None):
        if not index:
            index = self.getCurrentSelection()
        if index > 0:
            self.originList.selection_clear(index)
            self.originList.selection_set(index - 1)
        else:
            return

        self.openEditorWindow()

    def moveNextItem(self, index = None):
        if not index:
            index = self.getCurrentSelection()

        print("Index: ", index)

        if index < self.originList.size() - 1:
            self.originList.selection_clear(index)
            self.originList.selection_set(index + 1)
        else:
            return

        self.openEditorWindow()

if __name__ == '__main__':
    a = Application()
    a.run()
