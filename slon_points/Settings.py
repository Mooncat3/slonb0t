import json

TIMEOUT = 'timeout'
ATTENTIONS = 'attentions'
MODE = 'emojimode'
NORM = 'norm'
MAXMESSES = 'maxmesses'
BUFFERMAX = 'buffermax'
BUFFERDELAY = 'bufferdelay'
FORGET = 'forget'
ENTERTAIN = 'entertain'


def get_set(set: str):
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as e:
        try:
            data = json.loads(e.read())
            return data[set]
        except:
            if set == FORGET:
                return 1800.0
            elif set == BUFFERDELAY:
                return 2.0
            elif set == BUFFERMAX:
                return 3
            elif set == MAXMESSES:
                return 3
            elif set == NORM:
                return 10
            elif set == MODE:
                return "all"
            elif set == ATTENTIONS:
                return 3
            elif set == TIMEOUT:
                return 300
            elif set == ENTERTAIN:
                return True
            else:
                return None


def change_set(set: str, newvalue):
    try:
        with open('data/settings.txt', 'r', encoding='utf-8') as b:
            data = json.loads(b.read())
    except:
        data = {ENTERTAIN: True, BUFFERDELAY: 2.0, BUFFERMAX: 3, MAXMESSES: 3, NORM: 10.0, MODE: "skip", ATTENTIONS: 3,
                FORGET: 1800.0}
    if set == ENTERTAIN:
        if newvalue == 0:
            data[set] = False
        elif newvalue == 1:
            data[set] = True
        else:
            return "!entertain [0,1]"
    elif set == MODE:
        if newvalue == 'all' or newvalue == 'skip' or newvalue == 'skip_with':
            data[set] = newvalue
        else:
            return "!mode [all,skip,skip_with]"
    else:
        data[set] = newvalue
    with open('data/settings.txt', 'w', encoding='utf-8') as b:
        try:
            b.write(json.dumps(data))
            strer = ""
            for e in data.keys():
                strer += f"{e}: {data[e]}"
                if e != list(data.keys())[len(list(data.keys())) - 1]:
                    strer += ", "
            return strer
        except:
            return f"Ошибка сохранения"


def get_mod():
    return get_set(MODE)


def get_norm():
    return get_set(NORM)


def get_forget_kd():
    return get_set(FORGET)


def get_max_messes():
    return get_set(MAXMESSES)


def get_attentions():
    return get_set(ATTENTIONS)


def get_timeout():
    return get_set(TIMEOUT)


def get_bufer_timeout():
    return get_set(BUFFERDELAY)


def get_bufer_max():
    return get_set(BUFFERMAX)


def get_entertain():
    return get_set(ENTERTAIN)
