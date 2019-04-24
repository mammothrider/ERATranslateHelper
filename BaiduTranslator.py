import requests
import json
import execjs
import Config
import time
import threading
import js2py
import re

class BaiduTranslator:
    def __init__(self):
        self.linkAddress = 'https://fanyi.baidu.com/v2transapi'

        self.translateQueue = []
        
        self.baidu_url = "https://www.baidu.com/"
        self.root_url = "https://fanyi.baidu.com/"
        self.lang_url = "https://fanyi.baidu.com/langdetect"
        self.trans_url = "https://fanyi.baidu.com/v2transapi"
        self.data = {
            'from': 'jp',# 输入的语言
            'to': 'zh', # 需要输出的语言
            'query': None, # 需要翻译的词或句子
            'transtype': 'realtime', # 常量
            'simple_means_flag': '3',# 常量
            'sign': None, # 由query生成的一个数字
            'token': None,# 常量
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }

        self.session = requests.session()
        self.session.headers = self.headers
        self.session.get(self.baidu_url)

        token, gtk = self.get_token_gtk()
        self.data['token'] = token

        self.signFunction = js2py.EvalJs()
        with open('baidu.js', encoding='utf8') as f:
            js_data = f.read()
            js_data = re.sub("window\[l\]",'"'+gtk+'"',js_data)
            self.signFunction.execute(js_data)

    def get_token_gtk(self):
        '''获取token和gtk(用于合成Sign)'''
        self.session.get(self.root_url)
        resp = self.session.get(self.root_url)
        html_str = resp.content.decode()
        token = re.findall(r"token: '(.*?)'", html_str)[0]
        gtk = re.findall(r"window.gtk = '(.*?)'", html_str)[0]
        print('gtk: ', gtk)
        return token,gtk
        
    def generate_sign(self, text):
        """生成sign"""
        # 1. 准备js编译环境
        sign = self.signFunction.e(text)
        return sign

    #https://zhuanlan.zhihu.com/p/46111212
    def translate(self, word, data):
        data['query'] = word
        #data['sign'] = self.signFunction.call('e',word)
        data['sign'] = self.generate_sign(word)
        try:
            r = self.session.post(self.linkAddress, data=data, headers=self.headers).text
        except:
            time.sleep(5)
            return ''
        r = json.loads(r)
        
        try:
            return r["trans_result"]["data"][0]['dst']
        except:
            print(r)
            print('sign', data['sign'])
            return ''
        
    def checkAndTranslate(self):
        while True:
            if len(self.translateQueue) > 0:
                next = self.translateQueue.pop()
                next[1](self.translate(next[0], self.data))
                time.sleep(0.2)
            else:
                time.sleep(1)
        
    def startLazyTranslator(self):
        translateThread = threading.Thread(target = self.checkAndTranslate)
        translateThread.setDaemon(True)
        translateThread.start()

    def addTranslate(self, text, updateMethod):
        #print('called')
        self.translateQueue.append((text, updateMethod))

if __name__ == '__main__':
    baidu = BaiduTranslator()
    baidu.startLazyTranslator()
    a = "わ、私のことが嫌いになったの"
    baidu.addTranslate(a, print)
    time.sleep(10)
    