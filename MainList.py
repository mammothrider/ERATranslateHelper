import tkinter as tk
from tkinter import filedialog
from tkExtensions import *
from Editor import *
from ReplaceWindow import *
class MainList(tk.Frame):
    def __init__(self, master=None, core=None):
        super().__init__(master)
        self.core = core
        self.core.listWindow = self

        self.editor = None
        self.replaceWindow = None

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
        self.numberList['justify'] = tk.RIGHT

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

        replaceButton = tk.Button(buttonArea, text = 'Replace', height = 2, width = 10, command = self.openReplaceWindow)
        replaceButton.pack(side = 'top', padx = 30, pady = 15)

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

        self.editor.setOriginText(self.originList.get(index))
        self.editor.setTranslatedText(self.translateList.get(index))

    def openReplaceWindow(self):
        if not self.replaceWindow:
            self.replaceWindow = ReplaceWindow(self, self.core)
        #enlarge window
        else:
            self.replaceWindow.frame.deiconify()

    def editorWindowClosed(self):
        self.editor = None

    def replaceWindowClosed(self):
        self.replaceWindow = None

    def transAllText(self):
        for k in self.origin:
            if self.core.getTextDictValue(k) == '':
                def updateMethod(text, o = k):
                    self.core.setTranslatedText(o, text)
                    self.setTranslation(self.origin.index(o), text)
                self.core.translate(k, updateMethod)

    #due to no same key in dict
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
        x, y = self.scroll.get()

        self.refreshOriginList()
        self.refreshTranslationList()

        self.moveToItem(index)
        self.scroll.set(x, y)

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

    def moveToItem(self, index):
        self.originList.selection_clear(0, 'end')
        self.translateList.selection_clear(0, 'end')

        if index and index > -1 and index < self.originList.size():
            self.originList.selection_set(index)
            self.originList.see(index)
            self.translateList.see(index)
            self.numberList.see(index)
        else:
            return

    def movePreviousItem(self, index = None):
        if not index:
            index = self.getCurrentSelection()
            
        self.moveToItem(index - 1)
        self.openEditorWindow()

    def moveNextItem(self, index = None):
        if not index:
            index = self.getCurrentSelection()

        self.moveToItem(index + 1)
        self.openEditorWindow()