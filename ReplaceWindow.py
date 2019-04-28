import tkinter as tk
from functools import partial
class ReplaceWindow(tk.Frame):
    """the replacement window"""
    def __init__(self, master = None, core = None):
        super().__init__(master)
        self.frame = tk.Toplevel(master) #real window

        self.core = core
        #self.core.editorWindow = self
        
        self.frame.title("Find & Replace")
        x = 600
        y = 150
        self.frame.geometry("450x300+%d+%d" % (x, y))
        self.frame.minsize(450, 300)
        
        self.createEditWindowWidgets()

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
        text = self.findText.get(1.0, tk.END)
        dir = self.direction.get()
        currentPosition = self.master.getCurrentSelection()
        
        self.core.findNext(text, currentPosition, dir == 0)

    def replaceValue(self):
        text = self.findText.get(1.0, tk.END)
        backward = self.direction.get()

    def replaceAll(self, text, target):
        pass