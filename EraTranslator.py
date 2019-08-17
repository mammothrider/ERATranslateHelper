from BaiduTranslator import *
from BaiduAPITranslator import *
from Config import config
import re
from functools import partial

#main program
class EraTranslator:
    def __init__(self):
        self.waitingQueue = {}
        self.matchingQueue = {}
    
        splitPattern = config.getPattern("SplitPattern")
        namePattern = config.getPattern("NamePattern")
        placePattern = config.getPattern("PlacePattern")
        numberPattern = config.getPattern("NumberPattern")
        ignorePattern = config.getPattern("IgnorePattern")
        self.splitFormat = re.compile(splitPattern)
        self.nameFormat = re.compile(namePattern)
        self.placeFormat = re.compile(placePattern)
        self.numberFormat = re.compile(numberPattern)
        self.ignoreFormat = re.compile(ignorePattern, re.U)
        
        finalReplacePattern = config.items("ReplacePunctuation")
        self.finalReplacement = {}
        for item in finalReplacePattern:
            self.finalReplacement[item[0]] = re.compile(item[1])

        self.name = ["灵梦", "魔理沙", "八云紫", "红美玲", "AA", "BB", "CC"]
        self.place = ["正門", "納屋", "大浴場"]
        self.placeFind = ["正门", "仓库", "大浴场"]
        self.itemReplace = ["AA", "BB", "CC", "DD", "EE"]

        translator = config.get("Translator", "value")
        if translator == "BaiduAPI":
            self.translator = BaiduAPITranslator()
        else:
            self.translator = BaiduTranslator()

        #setting params function
        self.setTranslateParams = self.translator.setParams
        self.stopTranslate = self.translator.stopTranslate
        
        #re related
        self.percentString = re.compile("%[^%]*%")
        self.insideOutPattern = re.compile("%[^%]*\"?[^%]*\"?[^%]*%")

    
    def insideOut(self, text):
        text = text.replace('%"', '')
        text = text.replace('"%', '')
        text = text.replace('+"', '%')
        text = text.replace('"+', '%')
        return text
        
    def getMarker(self):
        self.markCounter += 1
        if self.markCounter > 1000000000:
            self.markCounter = 0
        return self.markCounter

    def splitSentence(self, text):
        result = self.splitFormat.search(text)
        
        #nothing match
        if not result:
            return [text]
            
        res = []
        for i in result.group(*range(1, self.splitFormat.groups + 1)):
            if i and self.ignoreFormat.search(i) == None:
                tmp = i.strip("「」")
                res.append(tmp)
        # print("splitSentence", res)
        return res

    def removeFormatName(self, text):
        mapping = {}

        #replace {} pattern
        result = self.numberFormat.findall(text)
        replaceNumber = 723
        for number in result:
            replaceStr = str(replaceNumber)
            replaceNumber += 1

            text = text.replace(number, replaceStr)
            mapping[replaceStr] = number

        #replace name
        count = 0
        result = self.nameFormat.findall(text)
        for name in result:
            text = text.replace(name, self.name[count])
            mapping[self.name[count]] = name
            
            count = (count + 1) % len(self.name)
            
        #replace place
        count = 0
        result = self.placeFormat.findall(text)
        for place in result:
            text = text.replace(place, self.place[count])
            mapping[self.place[count]] = place
            
            count = (count + 1) % len(self.place)

        #replace %% pattern
        nameKey = 0
        result = self.percentString.findall(text)
        for name in result:
            text = text.replace(name, self.itemReplace[nameKey])
            mapping[self.itemReplace[nameKey]] = name
            
            nameKey = (nameKey + 1) % len(self.itemReplace)

        text = text.strip()
        return text, mapping

    def recoverFormatName(self, translated, substring, origin):
        #real percentage mark
        if '%' in translated:
            translated = translated.replace('%', '\%')
        
        # print(translated, substring)
        # print(self.waitingQueue)
        
        try:
            mapping = self.waitingQueue[origin]["mapping"].pop(substring)
        except Exception as e:
            print("Recover Format Name", e)
            mapping = {}
            
        for k in mapping:
            if k in self.place:
                translated = translated.replace(self.placeFind[self.place.index(k)], mapping[k])
            else:
                translated = translated.replace(k, mapping[k])

        self.waitingQueue[origin]["result"][substring] = translated
        
        #mapping is none, means all is recovered
        mapping = self.waitingQueue[origin]["result"]
        translated = origin
        for k in mapping:
            translated = translated.replace(k, mapping[k])
            
        for key in self.finalReplacement:
            result = self.finalReplacement[key].sub(key, translated)
            
        print(translated, self.waitingQueue[origin]["recall"])
        self.waitingQueue[origin]["recall"](translated)
        

    def translate(self, text, updateMethod):
        if not text:
            return
            
        if self.insideOutPattern.search(text) != None:
            text = self.insideOut(text)
        origin = text
        
        #origin: {result:{sub:result}, mapping:{sub:map}, recall:}
        self.waitingQueue[origin] = {}
        self.waitingQueue[origin]["result"] = {}
        self.waitingQueue[origin]["mapping"] = {}
        self.waitingQueue[origin]["recall"] = updateMethod
        
        group = self.splitSentence(text)
        waitingList = []
        for sub in group:
            wait, mapping = self.removeFormatName(sub)
            # print("removeFormatName", wait, mapping)
            if not wait:
                continue
                
            self.waitingQueue[origin]["mapping"][sub] = mapping
            waitingList.append((wait, sub))
            
        # print("waitingList", waitingList)
        # print("waitingQueue", self.waitingQueue)
        #start after all finished
        for item in waitingList:
            self.translator.addTranslate(item[0], partial(self.recoverFormatName, substring = item[1] , origin = origin))
            # self.recoverFormatName(item[0], item[1], origin)
            
    
if __name__ == '__main__':
    a = EraTranslator()
    # text = "それは彼女が心の奥底でそれを望んでいたわけではない\@ABL:触手中毒 >= 3 ? …こともないが…何はともあれそうではない # …\@ことなのだ。"
    # text = "「ほんと、やらしいんだから……\@ COND('発情期') && BASE:欲求不満 >= 50 ? ♪ # \@」"
    text = "%CALLNAME:ARG%は%NAME(0)%に膝枕をしている。"
    # text, mapping = a.removeFormatName(text)
    # print(text, mapping)
    # text = a.recoverFormatName(text, mapping)
    # print(text)
    a.translate(text, print)
    time.sleep(10)