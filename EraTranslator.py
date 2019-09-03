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
        subSplitPattern = config.getPattern("SubSplitPattern")
        namePattern = config.getPattern("NamePattern")
        placePattern = config.getPattern("PlacePattern")
        numberPattern = config.getPattern("NumberPattern")
        ignorePattern = config.getPattern("IgnorePattern")
        self.splitFormat = re.compile(splitPattern)
        self.subSplitFormat = re.compile(subSplitPattern)
        self.nameFormat = re.compile(namePattern)
        self.placeFormat = re.compile(placePattern)
        self.numberFormat = re.compile(numberPattern)
        self.ignoreFormat = re.compile(ignorePattern, re.U)
        
        self.stripMark = config.get("StripMark", "value")
        
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
        #have target text between %%
        self.insideOutPattern = re.compile("%[^%]*\"[^%]*\"[^%^\*]*%")

    
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
        # print("splitSentence input", [text])
        result = self.splitFormat.search(text)
        
        #nothing match
        if not result:
            return [text]
            
        res = []
        for i in result.group(*range(1, self.splitFormat.groups + 1)):
            if i and self.ignoreFormat.search(i) == None:
                tmp = i.strip(" 「」")
                sub = self.subSplitFormat.findall(tmp)
                if len(sub) > 0:
                    res.extend(sub)
                else:
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

    # import pysnooper
    # @pysnooper.snoop()
    def recoverFormatName(self, translated, substring, origin):
        #real percentage mark
        if '%' in translated:
            translated = translated.replace('%', '\%')
        # translated.translate(str.maketrans("《》", "<>"))
        
        # print(translated, substring)
        # print("recoverFormatName", self.waitingQueue)
        
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
            translated = self.finalReplacement[key].sub(key, translated)
            
        #final return
        if not self.waitingQueue[origin]["mapping"]:
            self.waitingQueue[origin]["recall"](translated)
        
    
    def translate(self, text, updateMethod):
        if not text:
            return
        
        # print("input", [text])
        text = text.strip("\n\r")
            
        if self.insideOutPattern.search(text) != None:
            text = self.insideOut(text)
        origin = text
        # print("origin", origin)
        
        #origin: {result:{sub:result}, mapping:{sub:map}, recall:}
        self.waitingQueue[origin] = {}
        self.waitingQueue[origin]["result"] = {}
        self.waitingQueue[origin]["mapping"] = {}
        self.waitingQueue[origin]["recall"] = updateMethod
        
        group = self.splitSentence(origin.strip(self.stripMark))
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
    text = "精液経験＋{S}(%CALLNAME:ASSI%)"
    # text, mapping = a.removeFormatName(text)
    # print(text, mapping)
    # text = a.recoverFormatName(text, mapping)
    # print(text)
    a.translate(text, print)
    time.sleep(10)