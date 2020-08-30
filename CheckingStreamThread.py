import urllib.request
import json

from github import Github

import config
import time
import datetime

dat = {}
global active
global times
safer: int


def checkingthread():
    def get_game_name(id: str) -> str:
        if not id in games.keys():
            url = "https://api.twitch.tv/helix/games?id={}".format(id)
            request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(config.OAUTH),
                                                               "Client-ID": "{}".format(config.CLIENT_ID)})
            response = urllib.request.urlopen(request).read()
            data = json.loads(response)
            games[id] = data['data'][0]['name']
        print(games[id])
        return games[id]
    active = False
    times = time.time()
    safer = 0
    games = {}
    while True:
        url = f"https://api.twitch.tv/helix/streams?user_id={config.BROADCASTER_ID}"
        request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(config.OAUTH),
                                                           "Client-ID": "{}".format(config.CLIENT_ID)})
        response = urllib.request.urlopen(request).read()
        data = json.loads(response)
        if len(data['data']) > 0:
            print(data)
            if not active:
                with open(file='data/TRASHMASSIVE.txt', mode='r', encoding='utf-8') as q:
                    dat = json.loads(q.read())
                print(dat)
                if not dat['active']:
                    dat['active'] = True
                    dat['TRASHMASS'].append({"date": datetime.datetime.strftime(datetime.datetime.now(), "%m.%e.%y"), "MASS": []})
                    while len(dat['TRASHMASS']) > 10:
                        dat['TRASHMASS'].remove(dat['TRASHMASS'][0])
                    with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                        q.write(json.dumps(dat))
                    times = time.time()
                    active = True
                else:
                    times = time.time() - dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['duration']
                    active = True
            if safer > 0:
                safer = 0
                res = {"GAME_ID": "Timeout", "ViewerCount": data['data'][0]['viewer_count'], "time_of_update": time.time() - times}
                dat['duration'] = time.time() - times
                with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                    dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['MASS'].append(res)
                    q.write(json.dumps(dat))
            res = {"GAME_ID": get_game_name(data['data'][0]['game_id']), "ViewerCount": data['data'][0]['viewer_count'], "time_of_update": time.time() - times}
            if len(dat['TRASHMASS'][len(dat['TRASHMASS'])-1]['MASS']) > 0:
                if res['GAME_ID'] != dat['TRASHMASS'][len(dat['TRASHMASS'])-1]['MASS'][len(dat['TRASHMASS'][len(dat['TRASHMASS'])-1]['MASS']) - 1]["GAME_ID"] or res['ViewerCount'] != dat['TRASHMASS'][len(dat['TRASHMASS'])-1]['MASS'][len(dat['TRASHMASS'][len(dat['TRASHMASS'])-1]['MASS']) - 1]["ViewerCount"]:
                    dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['duration'] = time.time() - times
                    with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                        dat['TRASHMASS'][len(dat['TRASHMASS'])-1]['MASS'].append(res)
                        q.write(json.dumps(dat))
            else:
                dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['duration'] = time.time() - times
                dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['name'] = data['data'][0]['title']
                dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['date'] = datetime.datetime.now().strftime("%m.%d.%y")
                with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                    dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['MASS'].append(res)
                    q.write(json.dumps(dat))
        else:
            if active and safer > 60:
                safer = 0
                active = False
                with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                    q.write(json.dumps(dat))
                g = Github("f0011283768114fac26230cd23b3208ed10d0a54")

                repo = g.search_repositories("slonb0t")[0]

                contents = repo.get_contents("data/TRASHMASSIVE.txt")
                repo.delete_file(contents.path, "Automated Remove from Bot", contents.sha)

                repo.create_file("data/TRASHMASSIVE.txt", "Automated Upload from Bot", json.dumps(dat))
            else:
                if active:
                    if safer == 0:
                        dat['active'] = False
                        dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['duration'] = time.time() - times
                        with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                            dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['MASS'].append(dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['MASS'][len(dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['MASS']) - 1])
                            dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['MASS'][len(dat['TRASHMASS'][len(dat['TRASHMASS']) - 1]['MASS']) - 1]['time_of_update'] = time.time() - times
                            q.write(json.dumps(dat))
                    safer += 1
                else:
                    with open(file='data/TRASHMASSIVE.txt', mode='r', encoding='utf-8') as q:
                        dat = json.loads(q.read())
                    dat['active'] = False
                    with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as q:
                        q.write(json.dumps(dat))

        if active:
            time.sleep(10)
        if not active:
            time.sleep(60)



checkingthread()
