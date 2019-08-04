import tkinter as tk
from functools import partial
class AutoTranslate():
    """the translate window"""
    def __init__(self, master, core = None):
        self.frame = tk.Toplevel(master, padx = 10, pady = 10) #real window
        self.frame.protocol("WM_DELETE_WINDOW", self.closeWindow)
        
        #only keep the close button on this window
        self.frame.attributes('-toolwindow', 1)

        self.master = master
        self.core = core
        #self.core.editorWindow = self
        
        self.frame.title("Auto Translate")
        #init position
        x = 600
        y = 350
        self.frame.geometry("165x240+%d+%d" % (x, y))
        self.frame.resizable(width=False, height=False)
        
        self.createTranslateWindowWidgets()

    def closeWindow(self):
        self.frame.destroy()
        self.master.autoTranslateWindowClosed()

    def createTranslateWindowWidgets(self):
        settingFrame = tk.LabelFrame(self.frame, padx = 10, pady = 10)
        settingFrame['text'] = '自动翻译模块'
        settingFrame.pack(side = 'left', fill = 'both', expand = 1)

        entrySetting = {'width':5, 'justify':tk.RIGHT}
        labelSetting = {'justify':tk.RIGHT}

        cooldownLable = tk.Label(settingFrame, text = '翻译间隔:', **labelSetting)
        cooldownLable.grid(row = 0, column = 0, sticky=tk.E)

        self.cooldownTimeText = tk.Entry (settingFrame, **entrySetting)
        self.cooldownTimeText.insert(tk.END, '2')
        self.cooldownTimeText.grid(row = 0, column = 1)
        
        retryTimeLable = tk.Label(settingFrame, text = '重试时间:', **labelSetting)
        retryTimeLable.grid(row = 1, column = 0, sticky=tk.E)

        self.retryDelayTimeText = tk.Entry (settingFrame, **entrySetting)
        self.retryDelayTimeText.insert(tk.END, '5')
        self.retryDelayTimeText.grid(row = 1, column = 1)

        retryLable = tk.Label(settingFrame, text = '最大重试次数:', **labelSetting)
        retryLable.grid(row = 2, column = 0, sticky=tk.E)

        self.retryTimeText = tk.Entry (settingFrame, **entrySetting)
        self.retryTimeText.insert(tk.END, '5')
        self.retryTimeText.grid(row = 2, column = 1)
        
        
        fromLable = tk.Label(settingFrame, text = '开始行:', **labelSetting)
        fromLable.grid(row = 3, column = 0, sticky=tk.E)

        self.fromText = tk.Entry (settingFrame, **entrySetting)
        self.fromText.insert(tk.END, '1')
        self.fromText.grid(row = 3, column = 1)
        
        toLable = tk.Label(settingFrame, text = '结束行:', **labelSetting)
        toLable.grid(row = 4, column = 0, sticky=tk.E)

        if self.core:
            length = len(self.core.getOriginList())
        else:
            length = 0

        self.toText = tk.Entry (settingFrame, **entrySetting)
        self.toText.insert(tk.END, length)
        self.toText.grid(row = 4, column = 1)
        
        buttonSetting = { }
        
        startButton = tk.Button(settingFrame, text = '开始', command = self.startTranslate)
        startButton.grid(row = 5, columnspan = 2, sticky=tk.N+tk.E+tk.S+tk.W, **buttonSetting)
        
        stopButton = tk.Button(settingFrame, text = '停止', command = self.stopTranslate)
        stopButton.grid(row = 6, columnspan = 2, sticky=tk.N+tk.E+tk.S+tk.W, **buttonSetting)

    def startTranslate(self):
        sleep = self.cooldownTimeText.get()
        delay = self.retryDelayTimeText.get()
        time = self.retryTimeText.get()
        fromLine = self.fromText.get()
        toLine = self.toText.get()
        try:
            sleep = float(sleep)
            delay = float(delay)
            time = float(time)
            fromLine = int(fromLine) - 1 #line number is start from 1
            toLine = int(toLine)
        except:
            print("Type Error: At Least One Input Is Not Correct")
            return
            
        if fromLine < 0:
            fromLine = 0
            
        if fromLine > toLine:
            print("Error: Start Line Is Larger Than Finish Line")
        targetList = self.core.getOriginList()
        if toLine> len(targetList):
            print("Error: Finish Line Number Does Not Exist.")
            
        self.core.setTranslateParams(sleepTime = sleep, retryDelayTime = delay, retryTimes = time)
            
        for k in targetList[fromLine:toLine]:
            if self.core.getTextDictValue(k) == '':
                def updateMethod(text, o = k):
                    self.core.setTranslatedText(o, text)
                    self.master.setTranslation(targetList.index(o), text)
                self.core.translate(k, updateMethod)
        
        
    def stopTranslate(self):
        self.core.stopTranslate()
        
        
if __name__ == '__main__':
    tkRoot = tk.Tk()
    trans = AutoTranslate(master = tkRoot)
    tkRoot.mainloop()
