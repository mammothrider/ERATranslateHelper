import configparser
import os


config = None
def init():
    global config
    config = configparser.RawConfigParser()
    config.read("config.ini")
    if not config.sections:
        raise ValueError("No config file or file is empty.")

def get(section, key):
    global config
    if not config:
        init()
    return config.get(section, key)

if __name__ == '__main__':
    #con = Config()
    print(get("token", "value"))
    print(get("cookie", "value"))