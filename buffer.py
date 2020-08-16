import time
import json
import subprocess
import sys

global tttime
timec: time
timee: time
times: time
timer: time
max: int
dopbol: bool
recept: bool

users = {}

def get_bufer_timeout() -> float:
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as e:
        try:
            data = json.loads(e.read())
            return data['buferdelay']
        except:
            return 1.0

def get_user_timeout() -> float:
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as e:
        try:
            data = json.loads(e.read())
            return data['usertimeout']
        except:
            return 3.0

def get_timeout(abr: str) -> time:
    if abr == "c":
        return 1.0
    if abr == "e":
        return 2.0
    if abr == "s":
        return 1.0
    if abr == "r":
        return 5.0

def parse_file(t, me) -> str:
    try:
        with open(file='data/sendmess.txt', mode='r', encoding='utf-8') as e:
            tad = json.loads(e.read())
    except:
        tad = []
    with open(file='data/sendmess.txt', mode='w', encoding='utf-8') as e:
        tad.append({"timeout": t, "mes": me})
        e.write(json.dumps(tad))
    return str(len(tad) - 1)

def start_buffer_thread():
    tttime = time.time()
    timec = 0.0
    timee = 0.0
    times = 0.0
    timer = 0.0
    dopbol = True
    recept = False
    max = 0.0
    while True:
        time.sleep(1)
        if max < timec:
            max = timec
        if max < timee:
            max = timee
        if max < times:
            max = times
        if max < timer:
            max = timer
        if time.time() - (tttime + max) > 2.5:
            with open(file='data/sendmess.txt', mode='w', encoding='utf-8') as e:
                e.write("[]")
            tttime = time.time()
            timec = 0.0
            timee = 0.0
            times = 0.0
            timer = 0.0
            recept = False
        with open(file='data/buffer.txt', mode='r', encoding='utf-8') as e:
            try:
                dat = json.loads(e.read())
            except:
                dat = []
            for res in dat:
                if not res['bufered']:
                    res['bufered'] = True
                    if res['nickname'] in users and not res['vip']:
                        if time.time() - users[res['nickname']]['time'] < get_user_timeout() and res['type'] != "r":
                            users[res['nickname']]['time'] = time.time()
                            if not users[res['nickname']]['got']:
                                users[res['nickname']]['got'] = True
                                leng = parse_file(timer, "{} WeirdChamp STOP SPAM".format(res['nickname']))
                                timer = timer + get_bufer_timeout()
                                tttime = time.time()
                                subprocess.Popen([sys.executable, 'singlemessthread.py', leng])
                        else:
                            users[res['nickname']] = {"time": time.time(), "got": False}
                            leng = parse_file(timer, str.replace(res['message'], "\n", " "))
                            if res['type'] != "r":
                                timer = timer + get_bufer_timeout()
                                tttime = time.time()
                                subprocess.Popen([sys.executable, 'singlemessthread.py', leng])
                            else:
                                if not recept:
                                    if dopbol:
                                        dopbol = False
                                        timer = timer + get_bufer_timeout()
                                        tttime = time.time()
                                        subprocess.Popen([sys.executable, 'singlemessthread.py', leng])
                                    else:
                                        recept = True
                                        dopbol = True
                                        timer = timer + 2.0
                                        tttime = time.time()
                                        subprocess.Popen([sys.executable, 'singlemessthread.py', leng])
                    else:
                        if res['vip']:
                            leng = parse_file(0.0, str.replace(res['message'], "\n", " "))
                        else:
                            users[res['nickname']] = {"time": time.time(), "got": False}
                            leng = parse_file(timer, str.replace(res['message'], "\n", " "))
                        if res['type'] != "r":
                            timer = timer + get_bufer_timeout()
                            tttime = time.time()
                            subprocess.Popen([sys.executable, 'singlemessthread.py', leng])
                        else:
                            if not recept:
                                if dopbol:
                                    dopbol = False
                                    timer = timer + get_bufer_timeout()
                                    tttime = time.time()
                                    subprocess.Popen([sys.executable, 'singlemessthread.py', leng])
                                else:
                                    recept = True
                                    dopbol = True
                                    timer = timer + 2.0
                                    tttime = time.time()
                                    subprocess.Popen([sys.executable, 'singlemessthread.py', leng])
                    """
                    if res['type'] == "r" and timer < get_timeout(res['type']) + 2.0:
                        if dopbol:
                            dopbol = False
                        else:
                            dopbol = True
                            timer = timer + 2.0
                        try:
                            with open(file='data/sendmess.txt', mode='r', encoding='utf-8') as e:
                                tad = json.loads(e.read())
                        except:
                            tad = []
                        with open(file='data/sendmess.txt', mode='w', encoding='utf-8') as e:
                            tad.append({"timeout": timer, "mes": str.replace(res['message'], "\n", " ")})
                            e.write(json.dumps(tad))
                        timer = timer + get_timeout(res['type'])
                        tttime = time.time()
                        subprocess.Popen([sys.executable, 'singlemessthread.py', str(len(tad)-1)])
                    if res['type'] == "c":
                        try:
                            with open(file='data/sendmess.txt', mode='r', encoding='utf-8') as e:
                                tad = json.loads(e.read())
                        except:
                            tad = []
                        with open(file='data/sendmess.txt', mode='w', encoding='utf-8') as e:
                            tad.append({"timeout": timec, "mes": str.replace(res['message'], "\n", " ")})
                            e.write(json.dumps(tad))
                        timec = timec + get_timeout(res['type'])
                        tttime = time.time()
                        subprocess.Popen([sys.executable, 'singlemessthread.py', str(len(tad)-1)])
                    if res['type'] == "e":
                        try:
                            with open(file='data/sendmess.txt', mode='r', encoding='utf-8') as e:
                                tad = json.loads(e.read())
                        except:
                            tad = []
                        with open(file='data/sendmess.txt', mode='w', encoding='utf-8') as e:
                            tad.append({"timeout": timee, "mes": str.replace(res['message'], "\n", " ")})
                            e.write(json.dumps(tad))
                        timee = timee + get_timeout(res['type'])
                        tttime = time.time()
                        subprocess.Popen([sys.executable, 'singlemessthread.py', str(len(tad)-1)])
                    if res['type'] == "s":
                        try:
                            with open(file='data/sendmess.txt', mode='r', encoding='utf-8') as e:
                                tad = json.loads(e.read())
                        except:
                            tad = []
                        with open(file='data/sendmess.txt', mode='w', encoding='utf-8') as e:
                            tad.append({"timeout": times, "mes": str.replace(res['message'], "\n", " ")})
                            e.write(json.dumps(tad))
                        times = times + get_timeout(res['type'])
                        tttime = time.time()
                        subprocess.Popen([sys.executable, 'singlemessthread.py', str(len(tad)-1)])
                    """
            with open(file='data/buffer.txt', mode='w', encoding='utf-8') as q:
                if len(dat) == 0:
                    q.write("[]")
                else:
                    q.write(json.dumps(dat))
        max = 0.0



start_buffer_thread()
