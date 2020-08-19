import urllib.request
import json
import config
import time
import datetime


TRASHMASSIVE = []
dat = {}
global active
global times
safer: int


def checkingthread():
    active = False
    times = time.time()
    safer = 0
    while True:
        url = f"https://api.twitch.tv/helix/streams?user_id={config.BROADCASTER_ID}"
        request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(config.OAUTH),
                                                           "Client-ID": "{}".format(config.CLIENT_ID)})
        response = urllib.request.urlopen(request).read()
        data = json.loads(response)
        if len(data['data']) > 0:
            if not active:
                with open(file='data/TRASHMASSIVE.txt', mode='r', encoding='utf-8') as q:
                    dat = json.loads(q.read())
                dat['active'] = True
                dat['TRASHMASS'].append({"date": datetime.datetime.strftime(datetime.datetime.now(), "%m.%e.%y"), "MASS": []})
                with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                    q.write(json.dumps(dat))
                times = time.time()
                TRASHMASSIVE.clear()
                active = True
            if safer > 0:
                safer = 0
                res = {"GAME_ID": "666", "ViewerCount": data['data'][0]['viewer_count'], "time_of_update": time.time() - times}
                TRASHMASSIVE.append(res)
                with open(file='data/TRASH.txt', mode='w', encoding='utf-8') as q:
                    q.write(json.dumps(TRASHMASSIVE))
                with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                    dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['MASS'].append(res)
                    q.write(json.dumps(dat))
            res = {"GAME_ID": data['data'][0]['game_id'], "ViewerCount": data['data'][0]['viewer_count'], "time_of_update": time.time() - times}
            if len(TRASHMASSIVE) > 0:
                if res['GAME_ID'] != TRASHMASSIVE[len(TRASHMASSIVE) - 1]["GAME_ID"] or res['ViewerCount'] != TRASHMASSIVE[len(TRASHMASSIVE) - 1]["ViewerCount"]:
                    TRASHMASSIVE.append(res)
                    with open(file='data/TRASH.txt', mode='w', encoding='utf-8') as q:
                        q.write(json.dumps(TRASHMASSIVE))
                    with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                        dat['TRASHMASS'][len(dat['TRASHMASS'])-1]['MASS'].append(res)
                        q.write(json.dumps(dat))
            else:
                TRASHMASSIVE.append(res)
                with open(file='data/TRASH.txt', mode='w', encoding='utf-8') as q:
                    q.write(json.dumps(TRASHMASSIVE))
                with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                    dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['MASS'].append(res)
                    q.write(json.dumps(dat))
        else:
            if active and safer > 60:
                safer = 0
                active = False
                dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['MASS'][len(TRASHMASSIVE) - 1]['GAME_ID'] = dat['TRASHMASS'][len(dat['TRASHMASS']) - 2]['MASS']['GAME_ID']
                with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                    q.write(json.dumps(dat))
            else:
                if active:
                    if safer == 0:
                        dat['active'] = False
                        TRASHMASSIVE.append(TRASHMASSIVE[len(TRASHMASSIVE) - 1])
                        TRASHMASSIVE[len(TRASHMASSIVE) - 1]['time_of_update'] = time.time() - times
                        with open(file='data/TRASH.txt', mode='w', encoding='utf-8') as q:
                            q.write(json.dumps(TRASHMASSIVE))
                        with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                            dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['MASS'].append(TRASHMASSIVE[len(TRASHMASSIVE) - 1])
                            dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['MASS'][len(TRASHMASSIVE) - 1]['time_of_update'] = time.time() - times
                            q.write(json.dumps(dat))
                    safer += 1

        if active:
            time.sleep(10)
        if not active:
            time.sleep(60)



checkingthread()
