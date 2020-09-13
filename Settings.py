import json


def get_timeout() -> float:
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as e:
        try:
            data = json.loads(e.read())
            return data['timeout']
        except:
            return 300

def get_attentions() -> float:
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as e:
        try:
            data = json.loads(e.read())
            return data['attentions']
        except:
            return 3

def get_mod() -> str:
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as e:
        try:
            data = json.loads(e.read())
            return data['emojymod']
        except:
            return "all"

def get_norm() -> float:
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as e:
        try:
            data = json.loads(e.read())
            return data['norm']
        except:
            return 2.0

def get_max_messes() -> float:
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as e:
        try:
            data = json.loads(e.read())
            return data['maxmesses']
        except:
            return 3


def get_bufer_max() -> float:
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as e:
        try:
            data = json.loads(e.read())
            return data['buffermax']
        except:
            return 5


def get_bufer_timeout() -> float:
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as e:
        try:
            data = json.loads(e.read())
            return data['bufferdelay']
        except:
            return 1.0