from BaiduTranslator import *
import re

#main program
class EraTranslator:
    def __init__(self):
        self.name = ["灵梦", "魔理沙", "八云紫", "红美玲", "AA", "BB", "CC"]
        self.place = ["正門", "納屋", "大浴場"]
        self.placeFind = ["正门", "仓库", "大浴场"]

        self.translator = BaiduTranslator()
        self.translator.startLazyTranslator()

        self.percentString = re.compile("%[^%]*%")
        self.threeFunction = re.compile("\\\@.*#.*\\\@")
        self.insideOutPattern = re.compile("%[^%]*\"?[^%]*\"?[^%]*%")
        self.threeStart = re.compile("(\\\@).*\?")
    
    def insideOut(self, text):
        text = text.replace('%"', '')
        text = text.replace('"%', '')
        text = text.replace('+"', '%')
        text = text.replace('"+', '%')
        return text

    def threeFunctionHandle(self, text):
        p = {}
        three = self.threeFunction.search(text)
        if three:
            three = three[0]
        else:
            return text, p

        header = self.threeStart.match(three)[0]
        p["xx"] =  header
        #p["**"] = '#'
        p["yy"] = r"\@"

        for k in p:
            text = text.replace(p[k], k)
        
        return text, p
    
    def removeFormatName(self, text):
        #if text.startswith('%') and text.endswith('%'):
        #if text.startswith('%"'):
        if self.insideOutPattern.search(text) != None:
            text = self.insideOut(text)

        if self.threeFunction.search(text) != None:
            return self.threeFunctionHandle(text)
            
        mapping = {}
        result = self.percentString.findall(text)
        
        nameKey = 0
        placeKey = 0
        for name in result:
            if name.find("PLACE") != -1:
                text = text.replace(name, self.place[placeKey])
                mapping[self.place[placeKey]] = name
                
                placeKey = (placeKey + 1) % len(self.place)
            else:
                text = text.replace(name, self.name[nameKey])
                mapping[self.name[nameKey]] = name
                
                nameKey = (nameKey + 1) % len(self.name)

        text = text.strip()
        return text, mapping

    def recoverFormatName(self, text, mapping):
        #real percentage mark
        if '%' in text:
            text = text.replace('%', '\%')

        for k in mapping:
            if k in self.place:
                text = text.replace(self.placeFind[self.place.index(k)], mapping[k])
            else:
                text = text.replace(k, mapping[k])
        return text

    def translate(self, text, updateMethod):
        text, tmpMap = self.removeFormatName(text)
        self.translator.addTranslate(text, lambda x: updateMethod(self.recoverFormatName(x, tmpMap)))
    
if __name__ == '__main__':
    a = EraTranslator()
    text = "「私が、きっとなんとかするわ。……当然でしょう？　%CALLNAME:MASTER%は、%CALLNAME:奴隶%のものなんだから」"
    text, mapping = a.removeFormatName(text)
    print(text, mapping)
    text = a.recoverFormatName(text, mapping)
    print(text)