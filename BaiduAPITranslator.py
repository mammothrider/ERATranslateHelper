import requests
import json
from Config import config
import time
import hashlib
from AbstractTranslator import *

class BaiduAPITranslator(AbstractTranslator):
    def __init__(self):
        super().__init__()
    
        self.translate_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        
        self.appid = config.get("BaiduAPI", "appid")
        self.password = config.get("BaiduAPI", "password")
        
        self.data = {
            'from': 'jp',# 输入的语言
            'to': 'zh', # 需要输出的语言
            'q': None, # 需要翻译的词或句子
            'appid': self.appid,
            'sign': None, # 由query生成的一个数字
            'salt': None,
        }
        
        self.session = requests.session()
        
    def generate_sign(self, word):
        """
        按照 appid+q+salt+密钥 的顺序拼接得到字符串1。
        对字符串1做md5，得到32位小写的sign
        """
        self.data["salt"] = str(int(time.time()))
        sign = self.appid + word + self.data["salt"] + self.password
        # print(sign)
        md5 = hashlib.md5()
        md5.update(sign.encode(encoding='utf-8'))
        sign = md5.hexdigest()
        # print(sign)
        return sign
        
    def translate(self, word):
        self.data['q'] = word
        self.data['sign'] = self.generate_sign(word)
        try:
            r = self.session.post(self.translate_url, data=self.data).text
        except:
            print("Connection Error. Wait 5 seconds.")
            time.sleep(5)
            return 'error'

        try:
            r = json.loads(r)
        except:
            print("Json Load Error.")
            print("Content: ", r)
            return 'error'
        
        if "trans_result" not in r:
            print("Key Error: ", r)
            print('sign', self.data['sign'])
            return 'error'
        
        trans_result = r["trans_result"]
        res = []
        for i in range(len(trans_result)):
            res.append(trans_result[i]["dst"])
        return '\n'.join(res)
    

if __name__ == '__main__':
    baidu = BaiduAPITranslator()
    baidu.startTranslator()
    a = "わ、私のことが嫌いになったの"
    baidu.addTranslate(a, print)
    a = "私のことが嫌いになったの"
    baidu.addTranslate(a, print)
    input()