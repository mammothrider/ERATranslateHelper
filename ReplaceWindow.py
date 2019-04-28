import tkinter as tk
from functools import partial
class ReplaceWindow(tk.Frame):
    """the replacement window"""
    def __init__(self, master = None, core = None):
        super().__init__(master)
        self.frame = tk.Toplevel(master) #real window
        self.frame.protocol("WM_DELETE_WINDOW", self.closeWindow)

        self.core = core
        #self.core.editorWindow = self
        
        self.frame.title("Find & Replace")
        x = 600
        y = 150
        self.frame.geometry("450x300+%d+%d" % (x, y))
        self.frame.minsize(450, 300)
        
        self.createEditWindowWidgets()

    def closeWindow(self):
        self.frame.destroy()
        self.master.replaceWindowClosed()
        self.destroy()

    def createEditWindowWidgets(self):
        contentArea = tk.Frame(self.frame)
        contentArea.pack(side = 'left', fill = 'both', expand = 1)
        #frame for buttons
        buttonArea = tk.Frame(self.frame)
        buttonArea.pack(side = 'left', fill = 'y', expand = 0)
        
        self.findText = tk.Text(contentArea, height = 1, width = 5)
        self.findText.pack(side = 'top', fill = 'both', expand = 1, pady = 5)

        self.replaceText = tk.Text(contentArea, height = 1, width = 5)
        self.replaceText.pack(side = 'top', fill = 'both', expand = 1, pady = 5)

        self.direction = tk.IntVar() 
        directionButton = tk.Checkbutton(contentArea, text = "Backward Direction", height = 1, width = 20, variable = self.direction)
        directionButton.pack(side = 'top', expand = 0, pady = 5)

        findButton = tk.Button(buttonArea, text = "Find", height = 2, width = 10)
        findButton.pack(side = 'top', padx = 10, pady = 15, expand = 0)
        findButton['command'] = self.findValue

        replaceButton = tk.Button(buttonArea, text = "Replace", height = 2, width = 10)
        replaceButton.pack(side = 'top', padx = 10, pady = 15, expand = 0)
        replaceButton['command'] = self.replaceValue

        replaceAllButton = tk.Button(buttonArea, text = "Replace All", height = 2, width = 10)
        replaceAllButton.pack(side = 'top', padx = 10, pady = 15, expand = 0)
        replaceAllButton['command'] = self.replaceAll

    def findValue(self):
        text = self.findText.get(1.0, tk.END).strip()
        if text == '':
            return

        dir = self.direction.get()
        currentPosition = self.master.getCurrentSelection()
        
        next = self.core.findNext( currentPosition, text, dir == 0)
        if next != currentPosition:
            self.master.moveToItem(next)

    def replaceValue(self):
        text = self.findText.get(1.0, tk.END).strip()
        if text == '':
            return
        rep = self.replaceText.get(1.0, tk.END).strip()

        dir = self.direction.get()
        currentPosition = self.master.getCurrentSelection()
        
        #replace data
        self.core.replaceText(currentPosition, text, rep)
        
        #rebuild list and goto current position
        self.master.refreshList()

    def replaceAll(self):
        text = self.findText.get(1.0, tk.END).strip()
        if text == '':
            return
        rep = self.replaceText.get(1.0, tk.END).strip()

        currentPosition = self.master.getCurrentSelection()
        
        #replace data
        while True:
            self.core.replaceText(currentPosition, text, rep)
            next = self.core.findNext(currentPosition, text, True)
            if next == currentPosition:
                break

            currentPosition = next

        #rebuild list and goto current position    
        self.master.refreshList()