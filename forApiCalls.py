import urllib.request
import urllib.response
from urllib.parse import quote
import json
import rfc3339
from datetime import datetime, timedelta

BROADCASTER_ID = "34711476"
OAUTH = "2ed7e435kk3dm1tpgo73gnu7xcjczy"
CLIENT_ID = "gp762nuuoqcoxypju8c569th9wz7q5"


def gettopclip(days_before: int = 0, argument: str = "") -> {str: str}:
    id_game = "0"
    if len(argument) > 0:
        print(argument + "  " + str(len(argument)))
        if len(argument) <= 5 and abreviatur_helper(argument) != "":
            argument = abreviatur_helper(argument)
        qstr = quote(argument)
        url = "https://api.twitch.tv/helix/games?name={}".format(qstr)
        request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(OAUTH),
                                                           "Client-ID": "{}".format(CLIENT_ID)})
        try:
            response = urllib.request.urlopen(request).read()
            data = json.loads(response)
            for p in data["data"]:
                id_game = p['id']
            if id_game == "0":
                return {"code": "2", "url": ""}
        except:
            return {"code": "2", "url": ""}
    if days_before == 0:
        return do_request_for_getting_clip(id_game=id_game, ever=True)
    else:
        return do_request_for_getting_clip(id_game=id_game, days_before=days_before)


def do_request_for_getting_clip(id_game: str = "0", days_before: int = 0, ever: bool = False) -> {str: str}:
    if ever:
        url = "https://api.twitch.tv/helix/clips?broadcaster_id={}".format(BROADCASTER_ID)
    else:
        datepast = rfc3339.format((datetime.utcnow() + timedelta(hours=3)) - timedelta(days=days_before), utc=True,
                                  use_system_timezone=False)
        datenow = rfc3339.format(datetime.utcnow() + timedelta(hours=3), utc=True, use_system_timezone=False)
        url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&started_at={}&ended_at={}".format(
            BROADCASTER_ID, datepast,
            datenow)

    request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(OAUTH),
                                                       "Client-ID": "{}".format(CLIENT_ID)})
    response = urllib.request.urlopen(request).read()
    data = json.loads(response)
    ident: int = 1
    if id_game == "0":
        for p in data["data"]:
            return {"code": "0", "url": p['url']}
    else:
        while True:
            for p in data["data"]:
                if p['game_id'] == id_game:
                    return {"code": "1", "url": p['url']}
            if ever:
                url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&after={}".format(BROADCASTER_ID, data['pagination']['cursor'])
            else:
                url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&after={}&started_at={}&ended_at={}".format(
                    BROADCASTER_ID, data['pagination']['cursor'], datepast, datenow)
            request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(OAUTH),
                                                                   "Client-ID": "{}".format(CLIENT_ID)})
            response = urllib.request.urlopen(request).read()
            print(response)
            data = json.loads(response)
            if ident == 30:
                return {"code": "3", "url": ""}
            else:
                ident += 1

def abreviatur_helper(argument: str) -> str:
    with open('abreviatures.txt') as n:
        ad = json.loads(n.read())
        if argument in ad:
            return ad[argument]
        return ""
