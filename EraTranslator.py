from Translator.BaiduTranslator import *
from Translator.BaiduAPITranslator import *
from Translator.OpenaiTranslator import *

from Config import config
import re
from functools import partial
import traceback

DEBUG = False

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
        
        stripMark = config.get("StripMark", "value")
        stripMark = '^{0}+|{0}+$'.format(stripMark)
        self.stripFormat = re.compile(stripMark)
        
        finalReplacePattern = config.items("ReplacePunctuation")
        self.finalReplacement = {}
        for item in finalReplacePattern:
            self.finalReplacement[item[0]] = re.compile(item[1])

        self.name = ["灵梦", "魔理沙", "八云紫", "红美玲", "AA", "BB", "CC"]
        self.place = ["正門", "納屋", "大浴場"]
        self.placeFind = ["正门", "仓库", "大浴场"]
        self.itemReplace = ["苹果", "橘子", "香蕉", "鸭梨"]

        translator = config.get("Translator", "value")
        if translator == "BaiduAPI":
            self.translator = BaiduAPITranslator()
        elif translator == "OpenAI":
            self.translator = OpenAiTranslator()
        else:
            self.translator = BaiduTranslator()

        #setting params function
        self.setTranslateParams = self.translator.setParams
        self.stopTranslate = self.translator.stopTranslate
        
        #re related
        self.percentString = re.compile("%[^%]*%")
        #have target text between %%
        self.insideOutPattern = re.compile("%[^%]*\"[^%]*\"[^%^\*^\)]*%")

    
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
        if DEBUG:
            print("splitSentence input", [text])
        result = self.splitFormat.search(text)
        
        #nothing match
        if not result:
            return [text]
            
        res = []
        for i in result.group(*range(1, self.splitFormat.groups + 1)):
            if i and self.ignoreFormat.search(i) == None:
                tmp = self.stripFormat.sub("", i)
                tmplist = self.splitSentence(tmp)
                for t in tmplist:
                    sub = self.subSplitFormat.findall(t)
                    if len(sub) > 0:
                        res.extend(sub)
                    else:
                        res.append(t)
        if DEBUG:
            print("splitSentence", res)
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
        
        #sometimes substring not in mapping.
        #why? race condition?
        if substring not in self.waitingQueue[origin]["mapping"]:
            return
        
        try:
            mapping = self.waitingQueue[origin]["mapping"].pop(substring)
        except Exception as error:
            print("Recover Format Name Error")
            print(substring, self.waitingQueue[origin])
            traceback.print_exc()
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
            self.waitingQueue.pop(origin, None)
        
    
    def translate(self, text, updateMethod):
        if not text:
            return
        
        # print("input", [text])
        text = text.strip("\n\r")
            
        if self.insideOutPattern.search(text) != None:
            text = self.insideOut(text)
            
        #duplicate?
        if text in self.waitingQueue:
            return
        
        #origin: {result:{sub:result}, mapping:{sub:map}, recall:}
        self.waitingQueue[text] = {}
        self.waitingQueue[text]["result"] = {}
        self.waitingQueue[text]["mapping"] = {}
        self.waitingQueue[text]["recall"] = updateMethod
        
        origin = text
        origin = self.stripFormat.sub("", origin)
        if DEBUG:
            print("Origin", origin)
        
        # group = self.splitSentence(origin.strip(self.stripMark))
        group = self.splitSentence(origin)
        if DEBUG:
            print("Group", group)
        waitingList = []
        for sub in group:
            wait, mapping = self.removeFormatName(sub)
            if DEBUG:
                print("removeFormatName", wait, mapping)
            if not wait:
                continue
                
            self.waitingQueue[text]["mapping"][sub] = mapping
            waitingList.append((wait, sub))
            
        if DEBUG:
            print("waitingList", waitingList)
            print("waitingQueue", self.waitingQueue)
        #start after all finished
        for item in waitingList:
            self.translator.addTranslate(item[0], partial(self.recoverFormatName, substring = item[1] , origin = text))
            # self.recoverFormatName(item[0], item[1], origin)
            
    
if __name__ == '__main__':
    a = EraTranslator()
    text = 'ほら小野寺くんっ、教えた通りに頑張って%CSTR:9%をイかせてみてっ%UNICODE(0x2665)%」'
    # text, mapping = a.removeFormatName(text)
    # print(text, mapping)
    # text = a.recoverFormatName(text, mapping)
    # print(text)
    a.translate(text, print)
    time.sleep(20)
