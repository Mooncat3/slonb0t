import urllib.request
import urllib.response
from urllib.request import urlretrieve
from urllib.parse import quote
import json
import rfc3339
from datetime import datetime, timedelta

BROADCASTER_ID = "34711476"
OAUTH = "2ed7e435kk3dm1tpgo73gnu7xcjczy"
CLIENT_ID = "gp762nuuoqcoxypju8c569th9wz7q5"


def gettopclip(clipcode: int, argument) -> {str: str}:
    id_game = "0"
    if len(argument) > 0:
        qstr = quote(argument)
        url = "https://api.twitch.tv/helix/games?name={}".format(qstr)
        request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(OAUTH),
                                                           "Client-ID": "{}".format(CLIENT_ID)})
        try:
            response = urllib.request.urlopen(request).read()
        except:
            return {"code": "2", "url": ""}
        data = json.loads(response)
        for p in data["data"]:
            id_game = p['id']
    if clipcode == 0:
        url = "https://api.twitch.tv/helix/clips?broadcaster_id={}".format(BROADCASTER_ID)
        request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(OAUTH),
                                                           "Client-ID": "{}".format(CLIENT_ID)})
        response = urllib.request.urlopen(request).read()
        data = json.loads(response)
        if id_game == "0":
            for p in data["data"]:
                return {"code": "0", "url": p['url']}
        else:
            for p in data["data"]:
                if p['game_id'] == id_game:
                    return {"code": "1", "url": p['url']}
            return {"code": "2", "url": ""}
    if clipcode == 1:
        datepast = rfc3339.format((datetime.utcnow() + timedelta(hours=3)) - timedelta(days=365), utc=True,
                                  use_system_timezone=False)
        datenow = rfc3339.format(datetime.utcnow() + timedelta(hours=3), utc=True, use_system_timezone=False)

        url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&started_at={}&ended_at={}".format(BROADCASTER_ID,
                                                                                                     datepast,
                                                                                                     datenow)
        request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(OAUTH),
                                                           "Client-ID": "{}".format(CLIENT_ID)})
        response = urllib.request.urlopen(request).read()
        data = json.loads(response)
        if id_game == "0":
            for p in data["data"]:
                return {"code": "0", "url": p['url']}
        else:
            for p in data["data"]:
                if p['game_id'] == id_game:
                    return {"code": "1", "url": p['url']}
            return {"code": "2", "url": ""}
    if clipcode == 2:
        datepast = rfc3339.format((datetime.utcnow() + timedelta(hours=3)) - timedelta(days=30), utc=True,
                                  use_system_timezone=False)
        datenow = rfc3339.format(datetime.utcnow(), utc=True, use_system_timezone=False)
        url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&started_at={}&ended_at={}".format(
            BROADCASTER_ID, datepast,
            datenow)
        request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(OAUTH),
                                                           "Client-ID": "{}".format(CLIENT_ID)})
        response = urllib.request.urlopen(request).read()
        data = json.loads(response)
        if id_game == "0":
            for p in data["data"]:
                return {"code": "0", "url": p['url']}
        else:
            for p in data["data"]:
                if p['game_id'] == id_game:
                    return {"code": "1", "url": p['url']}
            return {"code": "2", "url": ""}
    if clipcode == 3:
        datepast = rfc3339.format((datetime.utcnow() + timedelta(hours=3)) - timedelta(days=1), utc=True,
                                  use_system_timezone=False)
        datenow = rfc3339.format(datetime.utcnow() + timedelta(hours=3), utc=True, use_system_timezone=False)
        url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&started_at={}&ended_at={}".format(
            BROADCASTER_ID, datepast,
            datenow)
        request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(OAUTH),
                                                           "Client-ID": "{}".format(CLIENT_ID)})
        response = urllib.request.urlopen(request).read()
        data = json.loads(response)
        if id_game == "0":
            for p in data["data"]:
                return {"code": "0", "url": p['url']}
        else:
            for p in data["data"]:
                if p['game_id'] == id_game:
                    return {"code": "1", "url": p['url']}
            return {"code": "2", "url": ""}
