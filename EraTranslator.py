from BaiduTranslator import *
from BaiduAPITranslator import *
import Config
import re

#main program
class EraTranslator:
    def __init__(self):
        self.name = ["灵梦", "魔理沙", "八云紫", "红美玲", "AA", "BB", "CC"]
        self.place = ["正門", "納屋", "大浴場"]
        self.placeFind = ["正门", "仓库", "大浴场"]

        translator = Config.get("Translator", "value")
        if translator == "BaiduAPI":
            self.translator = BaiduAPITranslator()
        else:
            self.translator = BaiduTranslator()

        #setting params function
        self.setTranslateParams = self.translator.setParams
        self.stopTranslate = self.translator.stopTranslate

        #re related
        #0020-007f english and punctuation, 3000-303f japanese punc, ff00-ff0f full size punc
        self.noJapanese = re.compile("^[\s\u0020-\u007f\u3000-\u303f\uff00-\uff0f]+$", re.U)
        self.percentString = re.compile("%[^%]*%")
        self.threeFunction = re.compile("\\\@.*#.*\\\@")
        self.insideOutPattern = re.compile("%[^%]*\"?[^%]*\"?[^%]*%")
        self.threeStart = re.compile("(\\\@).*\?")

        self.bracketsPattern = re.compile("{[^{^}]*}")
    
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
        p["mark1"] =  header
        p["mark2"] = '#'
        p["mark3"] = "\\@"

        for k in p:
            text = text.replace(p[k], "\n{}\n".format(k))
            # text = text.replace(p[k], k)
        
        return text, p
    
    def removeFormatName(self, text):
        #if text.startswith('%') and text.endswith('%'):
        #if text.startswith('%"'):
        if self.noJapanese.search(text) != None:
            return None, {}
        
        if self.insideOutPattern.search(text) != None:
            text = self.insideOut(text)

        mapping = {}

        if self.threeFunction.search(text) != None:
            text, mapping = self.threeFunctionHandle(text)

        #replace {} pattern
        result = self.bracketsPattern.findall(text)
        replaceNumber = 723
        for number in result:
            replaceStr = str(replaceNumber)
            replaceNumber += 1

            text = text.replace(number, replaceStr)
            mapping[replaceStr] = number

        #replace %% pattern
        nameKey = 0
        placeKey = 0
        result = self.percentString.findall(text)
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
        print(text)
        #real percentage mark
        if '%' in text:
            text = text.replace('%', '\%')

        for k in mapping:
            if k in self.place:
                text = text.replace(self.placeFind[self.place.index(k)], mapping[k])
            else:
                text = text.replace(k, mapping[k])
        text = text.replace('\n', '') + '\n'
        print(text)
        return text

    def translate(self, text, updateMethod):
        text, tmpMap = self.removeFormatName(text)
        print(text)
        print(tmpMap)
        if text:
            self.translator.addTranslate(text, lambda x: updateMethod(self.recoverFormatName(x, tmpMap)))
    
if __name__ == '__main__':
    a = EraTranslator()
    # text = "それは彼女が心の奥底でそれを望んでいたわけではない\@ABL:触手中毒 >= 3 ? …こともないが…何はともあれそうではない # …\@ことなのだ。"
    text = "「ほんと、やらしいんだから……\@ COND('発情期') && BASE:欲求不満 >= 50 ? ♪ # \@」"
    # text, mapping = a.removeFormatName(text)
    # print(text, mapping)
    # text = a.recoverFormatName(text, mapping)
    # print(text)
    a.translate(text, print)
    time.sleep(10)