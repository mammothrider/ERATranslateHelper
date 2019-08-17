import configparser
import os

class Config:
    config = None
    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read("config.ini", encoding="utf_8_sig")
        if not self.config.sections():
            raise ValueError("No config file or file is empty.")

    def get(self, section, key):
        return self.config.get(section, key)
        
    def options(self, section):
        return self.config.options(section)
        
    def items(self, section):
        return self.config.items(section)
        
    def getPattern(self, section):
        items = self.config.items(section)
        if items:
            value = [item[1] for item in items]
            pattern = "|".join(value)
            return pattern
        return None
    
config = Config()

def test(section, text):
    import re
    p = config.getPattern(section)
    print(p)
    testPattern = re.compile(p, re.U)
    element = testPattern.groups
    print(element)
    res = testPattern.search(text)
    if res:
        print(res.group(*range(element +1)))

if __name__ == '__main__':
    #con = Config()
    # print(config.get("mark", "value"))
    # print(config.options("TranslatePattern"))
    # print(config.items("TranslatePattern"))
    # print(config.getPattern("TranslatePattern"))
    # section = "TranslatePattern"
    # a = "DATAFORM ……　どうしますか？"
    # test(section, a)

    section = "NamePattern"
    # print(config.items(section))
    # a = "「ほんと、やらしいんだから……\@ COND('発情期') && BASE:欲求不満 >= 50 ? ♪ # \@ことも」"
    a = "%CALLNAME:ARG%は%NAME(0)%に膝枕をしている。"
    test(section, a)