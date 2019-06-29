import Config
import os
#file manager
class ErbFileManager:
    def __init__(self):
        self.mark = Config.get('mark', 'value')
        #self.coding = 'UTF-8'

    def setAddress(self, address):
        self.address = address
    
    def encodeFolder(self, address = None):
        if address is None:
            address = self.address

        if address is None:
            raise ValueError("No Address!")

        #get all file/folder name
        pathDir = os.listdir(address)
        for s in pathDir:
            #join name and address
            newDir = os.path.join(address,s)     
            if os.path.isfile(newDir):
                self.readFile(newDir)
                self.writeFile(newDir)
            else:
                self.encodeFolder(newDir)


    def readFile(self, address = None):
        if address is None:
            address = self.address

        if address is None:
            raise ValueError("No Address!")
        
        try:
            file = open(address, "r", encoding='utf_8_sig')
            self.content = file.readlines()
        except:
            file.close()
            file = open(address, "r", encoding='Shift-JIS')
            self.content = file.readlines()
        
        #self.getSentence(self.content)
        file.close()
        if self.content:
            self.content[0] = self.content[0].strip('\ufeff')
        return self.content
        
    def writeFile(self, address = None):
        if not address:
            address = self.address
        if not address:
            raise ValueError("address is None")
            
        with open(address, "w", encoding='utf_8_sig') as file:
            for line in self.content:
                if line != "removed":
                    file.write(line)

    def replaceContent(self, lineNumber, origin, trans):
        def hasMark():
            if lineNumber + 1 < len(self.content):
                text = self.content[lineNumber + 1].strip()
                return text.startswith(self.mark)
            return False

        text = self.content[lineNumber]
        nextMark = hasMark()

        #split with space, to handle exist translate part
        if origin not in self.content[lineNumber] \
            and (nextMark and origin not in self.content[lineNumber + 1]):
            raise ValueError("Error: {} not found in line {}".format(origin, lineNumber))
        
        index = text.find("PRINT")
        if index < 0:
            index = text.find("DATA")
        space = text[:index]
        printIndex = text.find(' ', index)
        backup = ''
        if origin != trans:
            backup = ''.join([space, self.mark, ' ', origin, '\n'])
            #has mark
            if nextMark:
                self.content[lineNumber + 1] = backup
                self.content[lineNumber] = ''.join([text[:printIndex], ' ', trans, '\n'])
            else:
                self.content[lineNumber] = ''.join([text[:printIndex], ' ', trans, '\n', backup])
        #delete translation
        else:
            self.content[lineNumber] = ''.join([text[:printIndex], ' ', origin, '\n'])
            if nextMark:
                self.content[lineNumber + 1] = "removed"

if __name__ == '__main__':
    a = ErbFileManager()
    add = r"COMF400.ERB"
    a.setAddress(add)
    a.openFile()
    print(a.content)