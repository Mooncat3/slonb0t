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

def get_timeout(abr: str) -> time:
    if abr == "c":
        return 3.0
    if abr == "e":
        return 3.0
    if abr == "s":
        return 3.0
    if abr == "r":
        return 5.0

def start_buffer_thread():
    tttime = time.time()
    timec = 0.0
    timee = 0.0
    times = 0.0
    timer = 0.0
    dopbol = True
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
        with open(file='data/buffer.txt', mode='r', encoding='utf-8') as e:
            dat = json.loads(e.read())
            for res in dat:
                if not res['bufered']:
                    res['bufered'] = True
                    if res['type'] == "r":
                        if dopbol:
                            dopbol = False
                            if timer > 0.0:
                                timer = timer - (time.time() - tttime)
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
                        if timec > 0.0:
                            timec = timec - (time.time() - tttime)
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
                        if timee > 0.0:
                            timee = timee - (time.time() - tttime)
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
                        if times > 0.0:
                            times = times - (time.time() - tttime)
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
            with open(file='data/buffer.txt', mode='w', encoding='utf-8') as q:
                if len(dat) == 0:
                    q.write("[]")
                else:
                    q.write(json.dumps(dat))
        max = 0.0



start_buffer_thread()