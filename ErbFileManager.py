from Config import config
import os
import re
#file manager
class ErbFileManager:
    def __init__(self):
        self.mark = config.get('mark', 'value')
        #origin line number in file
        self.originLineNumber = {}
        #re get pattern
        translatePattern = config.getPattern("TranslatePattern")
        ignorePattern = config.getPattern("IgnorePattern")
        self.obtain = re.compile(translatePattern)
        self.ignore = re.compile(ignorePattern, re.U)

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
            self.originLineNumber.clear()
        except:
            try:
                file.close()
                file = open(address, "r", encoding='Shift-JIS')
                self.content = file.readlines()
            except:
                print("Can't Open File", address)
                file.close()
                return []
        
        print("Open File", address)

        file.close()
        if self.content:
            self.content[0] = self.content[0].strip('\ufeff')
        return self.content
        
    #get sentence from file
    def getSentence(self):
        textDict = {}
        for i in range(len(self.content)):
            text = self.obtain.search(self.content[i])
            if not text:
                continue

            text = list(filter(None, text.groups()))[0].strip()
            # print("text", text)
            if self.hasMark(i) or self.ignore.search(self.content[i]) == None:
                #check translated info
                nextList = []
                if i < len(self.content) - 1:
                    nextList = self.content[i + 1].strip().split(' ')
                # print("nextList", nextList)
                translated = ""
                if self.mark in nextList:
                    translated = text
                    origin = ' '.join(nextList[1:]).strip()
                else:
                    origin = text
                # print("origin", origin)
                # print("translated", translated)
                #check dict existance
                if origin not in self.originLineNumber:
                    self.originLineNumber[origin] = []
                self.originLineNumber[origin] += [i]

                #add to translate list
                textDict[origin] = translated
        print("Total: ", len(textDict))
        return textDict
        
    def saveFile(self, textDict):
        for k in textDict:
            #have content
            if textDict[k] != '':
                #translated text + mark + origin
                trans = textDict[k]
                #for multiple line have same content
                for line in self.originLineNumber[k]:
                    self.replaceContent(line, k, trans)
            #replace with origin text
            else:
                for line in self.originLineNumber[k]:
                    self.replaceContent(line, k, "")
        self.writeFile()
        
    def writeFile(self, address = None):
        if not address:
            address = self.address
        if not address:
            raise ValueError("address is None")
            
        with open(address, "w", encoding='utf_8_sig') as file:
            for line in self.content:
                if line != "removed":
                    file.write(line)
            print("File Saved", address)

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

    def hasMark(self, lineNumber):
        if lineNumber + 1 < len(self.content):
            text = self.content[lineNumber + 1].strip()
            return text.startswith(self.mark)
        return False

    def replaceContent(self, lineNumber, origin, trans):
        text = self.content[lineNumber]
        nextMark = self.hasMark(lineNumber)

        #split with space, to handle exist translate part
        if origin not in self.content[lineNumber] \
            and (nextMark and origin not in self.content[lineNumber + 1]):
            raise ValueError("Error: {} not found in line {}".format(origin, lineNumber))
        
        emptylength = len(text) - len(text.lstrip())
        space = text[:emptylength]
        if trans != "":
            backup = ''.join([space, self.mark, ' ', origin, '\n'])
            
            result = self.obtain.search(self.content[lineNumber])
            if result == None:
                return
                
            result = result.groups()
            result = next((x for x in result if x is not None), None)
            # print(result, trans)
            
            if result == None or result == trans:
                return
                
            self.content[lineNumber] = self.content[lineNumber].split('\n')[0]
            self.content[lineNumber] = self.content[lineNumber].replace(result, trans) + '\n'
                    
            # print([self.content[lineNumber]])
            
            #has mark
            if nextMark:
                self.content[lineNumber + 1] = backup
            else:
                self.content[lineNumber] += backup
        #delete translation
        else:
            result = self.obtain.search(self.content[lineNumber])
            if result == None:
                return
                
            result = result.groups()
            result = next((x for x in result if x is not None), None)
            if result != None and result != origin:
                self.content[lineNumber] = self.content[lineNumber].split('\n')[0]
                self.content[lineNumber] = self.content[lineNumber].replace(result, origin) + '\n'
                
            if nextMark:
                self.content[lineNumber + 1] = "removed"

if __name__ == '__main__':
    a = ErbFileManager()
    add = r"COMF400.ERB"
    a.setAddress(add)
    a.openFile()
    print(a.content)