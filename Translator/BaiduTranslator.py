import requests
import json
import time
import threading
import re
# import js2py
# import execjs
from pyjsTranslated import pyjsTranslated
import os

from Translator.AbstractTranslator import *

class BaiduTranslator(AbstractTranslator):
    def __init__(self):
        super().__init__()

        self.linkAddress = 'https://fanyi.baidu.com/v2transapi'
        
        self.baidu_url = "https://www.baidu.com/"
        self.root_url = "https://fanyi.baidu.com/"
        self.lang_url = "https://fanyi.baidu.com/langdetect"
        self.trans_url = "https://fanyi.baidu.com/v2transapi"
        self.data = {
            'from': 'jp',# 输入的语言
            'to': 'zh', # 需要输出的语言
            'query': None, # 需要翻译的词或句子
            'transtype': 'translang', # 常量
            'simple_means_flag': '3',# 常量
            'sign': None, # 由query生成的一个数字
            'token': None,# 常量
        }
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        }

        self.session = requests.session()
        self.session.headers = self.headers
        self.session.get(self.baidu_url)

        token, self.gtk = self.get_token_gtk()
        self.data['token'] = token

        # self.signFunction = js2py.EvalJs()
        # with open('baidu.js', encoding='utf8') as f:
            # js_data = f.read()
            # js_data = re.sub("window\[l\]",'"'+gtk+'"',js_data)
            # self.signFunction.execute(js_data)
            #self.signFunction = execjs.compile(js_data)

    def get_token_gtk(self):
        '''获取token和gtk(用于合成Sign)'''
        resp = self.session.get(self.root_url)
        html_str = resp.content.decode()
        token = re.findall(r"token: '(.*?)'", html_str)[0]
        gtk = re.findall(r"window.gtk = '(.*?)'", html_str)[0]
        return token,gtk
        
    def generate_sign(self, text):
        """生成sign"""
        # sign = self.signFunction.e(text)
        #sign = self.signFunction.call("e", text)
        sign = pyjsTranslated.e(text, self.gtk)
        return sign

    #https://zhuanlan.zhihu.com/p/46111212
    def translate(self, word):
        self.data['query'] = word
        self.data['sign'] = self.generate_sign(word)
        try:
            r = self.session.post(self.linkAddress, data=self.data, headers=self.headers).text
        except:
            print("Connection Error. Wait 5 seconds.")
            time.sleep(5)
            return 'error'
            
        # print(r.encode('utf-8').decode('unicode_escape'))

        try:
            r = json.loads(r)
        except:
            print("Json Load Error.")
            print("Content: ", r)
            return 'error'
        
        # try:
            # return r["trans_result"]["data"][0]['dst']
        # except:
            # print("Sign Error: ", r)
            # print('sign', self.data['sign'])
            # return 'error'
        
        if "trans_result" not in r:
            print("key error: ", r)
            print('sign', self.data['sign'])
            return 'error'
        
        trans_result = r["trans_result"]["data"]
        res = []
        for i in range(len(trans_result)):
            res.append(trans_result[i]["dst"])
        return '\n'.join(res)
        

# os.environ["EXECJS_RUNTIME"] = "Node"

if __name__ == '__main__':
    baidu = BaiduTranslator()
    baidu.startTranslator()
    a = "わ、私のことが嫌いになったの"
    baidu.addTranslate(a, print)
    input()

    #sign test
    # print(execjs.get().name)
    # signFunction = js2py.EvalJs()
    # with open('baidu.js', encoding='utf8') as f:
           # js_data = f.read()
           # signFunction.execute(js_data)
           # execjsSign = execjs.compile(js_data)
    # word = "「・・正気なの！？ 灵梦が何を考えているのかわかんないよ・・でも、そうまで言うなら努力するよ」"
    # print(execjsSign.call('e',word, gtk))
    # print(signFunction.e(word, gtk))
    # print(pyjsTranslated.e(word, gtk))
    