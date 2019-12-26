import tkinter as tk
from UI.tkExtensions import *
class Editor(tk.Frame):
    def __init__(self, master=None, core=None):
        super().__init__(master)
        self.frame = tk.Toplevel(master)

        #add close event
        self.frame.protocol("WM_DELETE_WINDOW", self.closeWindow)

        self.core = core
        #self.core.editorWindow = self
        
        self.frame.title("Editor")
        x = 600
        y = 50
        self.frame.geometry("450x500+%d+%d" % (x, y))
        self.frame.minsize(450, 500)
        
        self.createEditWindowWidgets()

    def closeWindow(self):
        self.frame.destroy()
        self.master.editorWindowClosed()
        self.destroy()
  
    def createEditWindowWidgets(self):
        #frame for buttons
        buttonArea = tk.Frame(self.frame)
        buttonArea.pack(side = 'top', fill = 'x', expand = 0)
        contentArea = tk.Frame(self.frame)
        contentArea.pack(side = 'top', fill = 'both', expand = 1)
        
        #add buttons
        prev = tk.Button(buttonArea, text = '<<', height = 2, width = 10)
        prev.pack(side = 'left', padx = 10, pady = 15, expand = 1)
        prev['command'] = self.previousItem

        save = tk.Button(buttonArea, text = '保存', height = 2, width = 10)
        save.pack(side = 'left', padx = 10, pady = 15, expand = 1)
        save['command'] = self.saveTranslated

        next = tk.Button(buttonArea, text = '>>', height = 2, width = 10)
        next.pack(side = 'left', padx = 10, pady = 15, expand = 1)
        next['command'] = self.nextItem

        #add context area
        #origin frame -- should be readonly
        padx = 5
        pady = 5
        originFrame = tk.Frame(contentArea)
        originFrame.pack(side = 'top', padx = padx, pady = pady, fill = 'both', expand = 1)
        
        self.origin = tk.Text(originFrame, height = 3, width = 10)
        self.origin.pack(side = 'left', fill = 'both', expand = 1)
        
        originScroll = AutoScrollbar(originFrame, command = self.origin.yview)
        originScroll.pack(side = 'right', fill = 'y', expand = 0)
        self.origin['yscrollcommand'] = originScroll.set
        
        #for web translate
        webFrame = tk.Frame(contentArea)
        webFrame.pack(side = 'top', padx = padx, pady = pady, fill = 'both', expand = 1)
        
        webFrame.rowconfigure(0, weight = 1)
        webFrame.rowconfigure(1, weight = 1)
        webFrame.rowconfigure(2, weight = 1)
        webFrame.rowconfigure(3, weight = 1)
        webFrame.rowconfigure(4, weight = 1)
        webFrame.rowconfigure(5, weight = 1)
        
        webFrame.columnconfigure(0, weight = 0)
        webFrame.columnconfigure(1, weight = 1)

        copy = tk.Button(webFrame, text = '复制原文', height = 2, width = 7, command = self.copyButton)
        copy.grid(row = 0, rowspan = 2, column = 0, ipadx = 10, padx = 10)

        trans = tk.Button(webFrame, text = '翻译', height = 2, width = 7, command = self.translateButton)
        trans.grid(row = 2, rowspan = 2, column = 0, ipadx = 10, padx = 10)
        
        paste = tk.Button(webFrame, text = '复制译文', height = 2, width = 7, command = self.pasteButton)
        paste.grid(row = 4, rowspan = 2, column = 0, ipadx = 10, padx = 10)

        self.web = tk.Text(webFrame, height = 2)
        self.web.grid(row = 0, rowspan = 3, column = 1, sticky=tk.N+tk.E+tk.S+tk.W)

        self.webTranslate = tk.Text(webFrame, height = 2)
        self.webTranslate.grid(row = 3, rowspan = 3, column = 1, sticky=tk.N+tk.E+tk.S+tk.W)
        
        #webScroll = AutoScrollbar(webFrame, command = self.web.yview)
        #webScroll.grid(row = 0, rowspan = 2, column = 2, sticky=tk.N+tk.E+tk.S+tk.W)
        #self.web['yscrollcommand'] = webScroll.set
        
        #trans frame
        transFrame = tk.Frame(contentArea)
        transFrame.pack(side = 'top', padx = padx, pady = pady, fill = 'both', expand = 1)
        
        self.translate = tk.Text(transFrame, height = 3, width = 10)
        self.translate.pack(side = 'left', fill = 'both', expand = 1)
        
        transScroll = AutoScrollbar(transFrame, command = self.translate.yview)
        transScroll.pack(side = 'right', fill = 'y', expand = 0)
        self.translate['yscrollcommand'] = transScroll.set

        #set undo
        self.web['undo'] = True
        self.translate['undo'] = True

    def setOriginText(self, text):
        self.origin.config(state=tk.NORMAL)
        self.origin.delete('1.0', tk.END)
        self.origin.insert(tk.END, text)
        self.origin.config(state=tk.DISABLED)

    def setTranslatedText(self, text):
        self.translate.delete('1.0', tk.END)
        self.translate.insert('1.0', text)

    def setWebTranslatedText(self, text):
        self.webTranslate.delete('1.0', tk.END)
        self.webTranslate.insert('1.0', text)

    def copyButton(self):
        text = self.origin.get('1.0', tk.END).strip()
        self.web.delete('1.0', tk.END)
        self.web.insert(tk.END, text)

    def translateButton(self):
        self.core.translate(self.web.get('1.0', tk.END).strip(), self.setWebTranslatedText)
        
    def pasteButton(self):
        text = self.webTranslate.get('1.0', tk.END).strip()
        self.translate.delete('1.0', tk.END)
        self.translate.insert(tk.END, text)

    def previousItem(self):
        index = self.master.getOriginPosition(self.origin.get('1.0', tk.END).strip())
        self.master.movePreviousItem(index)

    def nextItem(self):
        index = self.master.getOriginPosition(self.origin.get('1.0', tk.END).strip())
        self.master.moveNextItem(index)

    def saveTranslated(self):
        self.core.setTranslatedText(self.origin.get('1.0', tk.END).strip(), self.translate.get('1.0', tk.END).strip())
        self.master.setTranslation(self.master.getOriginPosition(self.origin.get('1.0', tk.END).strip()), \
                                self.translate.get('1.0', tk.END).strip())
                                
if __name__ == '__main__':
    tkRoot = tk.Tk()
    app = Editor(master = tkRoot)
    app.mainloop()