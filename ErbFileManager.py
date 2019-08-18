from Config import config
import os
import re
#file manager
class ErbFileManager:
    def __init__(self):
        self.mark = config.get('mark', 'value')
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

    def saveDictionary(self, translated):
        if not self.address:
            print("No File Selected")
            return

        filename = os.path.basename(self.address)
        folder = self.address.split("ERB")[0] + "dict/"
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, filename.rsplit(".")[0] + "_dict.txt")
        print("保存字典文件：", filename)
        # addr, filename = os.path.split(self.address)
        if not os.path.exists('my_folder'):
            os.makedirs('my_folder')
        
        with open(filename, "w", encoding='utf_8_sig') as file:
            for key in translated:
                if key and translated[key]:
                    file.write("{}\t{}\n".format(key, translated[key]))

    def readDictionary(self, address):
        res = {}

        with open(address, "r", encoding='utf_8_sig') as file:
            content = file.readlines()
            for line in content:
                text = line.strip().split("\t")
                if len(text) == 2:
                    res[text[0]] = text[1]
        print(res)
        return res

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