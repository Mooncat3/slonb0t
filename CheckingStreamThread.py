import urllib.request
import json
import config
import time


TRASHMASSIVE = []
global active
global times


def checkingthread():
    active = False
    times = time.time()
    while True:
        url = "https://api.twitch.tv/helix/streams"
        request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(config.OAUTH),
                                                           "Client-ID": "{}".format(config.CLIENT_ID)})
        response = urllib.request.urlopen(request).read()
        data = json.loads(response)
        if len(data['data']) > 0:
            if not active:
                times = time.time()
                TRASHMASSIVE.clear()
                active = True
            res = {"GAME_ID": data['data'][0]['game_id'], "ViewerCount": data['data'][0]['viewer_count'], "time_of_update": time.time() - times}
            if len(TRASHMASSIVE) > 0:
                if res['GAME_ID'] != TRASHMASSIVE[len(TRASHMASSIVE) - 1]["GAME_ID"] or res['ViewerCount'] != TRASHMASSIVE[len(TRASHMASSIVE) - 1]["ViewerCount"]:
                    TRASHMASSIVE.append(res)
                    with open(file='data/TRASH.txt', mode='w', encoding='utf-8') as q:
                        q.write(json.dumps(TRASHMASSIVE))
                    print(TRASHMASSIVE[len(TRASHMASSIVE) - 1])
            else:
                TRASHMASSIVE.append(res)
                with open(file='data/TRASH.txt', mode='w', encoding='utf-8') as q:
                    q.write(json.dumps(TRASHMASSIVE))
                print(TRASHMASSIVE[len(TRASHMASSIVE) - 1])
        else:
            if active:
                active = False
                with open(file='data/TRASH.txt', mode='w', encoding='utf-8') as q:
                    q.write(json.dumps(TRASHMASSIVE))
                print(TRASHMASSIVE)
        time.sleep(60)



checkingthread()
