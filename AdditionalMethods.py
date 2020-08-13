import urllib.request
import urllib.response
from urllib.parse import quote
import time
import json
import rfc3339
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import random
import re
import config

def get_last_stream_stat():
    def summ_times() -> time:
        timeq: time = 0.0
        for t in game_mass:
            if 'time' in t.keys():
                timeq = timeq + float(t['time'])
        return timeq
    with open(file='data/TRASH.txt', mode='r', encoding='utf-8') as q:
        TRASHMASSIVE = json.loads(q.read())
    url = "https://api.twitch.tv/helix/videos?user_id=34711476&first=2"
    request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(config.OAUTH),
                                                       "Client-ID": "{}".format(config.CLIENT_ID)})
    response = urllib.request.urlopen(request).read()
    data = json.loads(response)
    strim_name = data['data'][0]['title']
    strim_duration = data['data'][0]['duration']
    viewsummcount = 0
    id_game = "0"
    game_mass = []
    timet = 0.0
    maxviewcount=0
    for dat in TRASHMASSIVE:
        viewsummcount += dat['ViewerCount']
        if dat['ViewerCount'] > maxviewcount:
            maxviewcount = dat['ViewerCount']
        if len(game_mass) > 0 and (id_game != dat['GAME_ID'] or (dat == TRASHMASSIVE[len(TRASHMASSIVE)-1] and dat['GAME_ID'] == TRASHMASSIVE[len(TRASHMASSIVE)-2]['GAME_ID'])):
            game_mass[len(game_mass) - 1]['time'] = dat['time_of_update'] - timet
        if id_game != dat['GAME_ID']:
            id_game = dat['GAME_ID']
            url = "https://api.twitch.tv/helix/games?id={}".format(id_game)
            request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(config.OAUTH),
                                                               "Client-ID": "{}".format(config.CLIENT_ID)})
            response = urllib.request.urlopen(request).read()
            data = json.loads(response)
            game_mass.append({"name": data['data'][0]['name']})
            timet = dat['time_of_update']
            if len(game_mass) == 1:
                game_mass[len(game_mass) - 1]['time'] = dat['time_of_update']
            else:
                game_mass[len(game_mass) - 1]['time'] = dat['time_of_update'] - summ_times()
    streamstat = {"Games": game_mass, "middleviewcount": viewsummcount / len(TRASHMASSIVE), "StreamName": strim_name, "StreamDuration": strim_duration}
    categorystr = ""
    for r in streamstat['Games']:
        rounded = ""
        timestart = r['time']
        if timestart/3600 > 1:
            rounded += f"{int(timestart/3600)}h "
            timestart = timestart % 3600
        if timestart/60 > 1:
            rounded += f"{int(timestart/60)}m "
            timestart = timestart % 60
        if timestart/60 > 1 and rounded.find("h") == -1:
            rounded = f"{int(timestart)}s "
        categorystr += f"{r['name']}[{rounded}] > "
    return f"стрим: {streamstat['StreamName']}[{streamstat['StreamDuration']}] || среднее зр: {int(streamstat['middleviewcount'])} || {categorystr}"

def parse_standartfile_message(nickname, formatable, message, command, name_of_file) -> str:
    if message == command:
        return f"{nickname}, введите {command} [message]"
    else:
        if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1 or message.find('заходите') != -1:
            return f"{nickname}, думал забанить меня? WeirdChamp "
        else:
            with open(f'data/{name_of_file}.txt', 'r', encoding='utf-8') as c:
                List = list(c)
                randomm = random.choice(List)
                randomm = re.sub("\n", '', randomm)
                subject = str.replace(message, f'{command} ', '')
                subject = re.sub("\n", '', subject)
                return formatable.format(nickname=nickname, filestr=randomm, messagestr=subject)

def parse_simplefile_message(formatable, name_of_file) -> str:
    with open(f'data/{name_of_file}.txt', 'r', encoding='utf-8') as n:
        List = list(n)
        randomm = random.choice(List)
        randomm = re.sub("\n", '', randomm)
        return formatable.format(str(randomm))

def gettopclip(days_before: int = 0, argument: str = "", nickname: str = "") -> str:
    #-------------------------------------checking for clip--------------------------------------
    def do_request_for_getting_clip(id_game: str = "0", days_before: int = 0, ever: bool = False) -> {str: str}:
        if ever:
            url = "https://api.twitch.tv/helix/clips?broadcaster_id={}".format(config.BROADCASTER_ID)
        else:
            datepast = rfc3339.format((datetime.utcnow() + timedelta(hours=3)) - timedelta(days=days_before), utc=True,
                                      use_system_timezone=False)
            datenow = rfc3339.format(datetime.utcnow() + timedelta(hours=3), utc=True, use_system_timezone=False)
            url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&started_at={}&ended_at={}".format(
                config.BROADCASTER_ID, datepast,
                datenow)

        request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(config.OAUTH),
                                                           "Client-ID": "{}".format(config.CLIENT_ID)})
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
                    url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&after={}".format(config.BROADCASTER_ID,
                                                                                                data['pagination'][
                                                                                                    'cursor'])
                else:
                    url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&after={}&started_at={}&ended_at={}".format(
                        config.BROADCASTER_ID, data['pagination']['cursor'], datepast, datenow)
                request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(config.OAUTH),
                                                                   "Client-ID": "{}".format(config.CLIENT_ID)})
                response = urllib.request.urlopen(request).read()
                print(response)
                data = json.loads(response)
                if ident == 30:
                    return {"code": "3", "url": ""}
                else:
                    ident += 1
    # -------------------------------------making response string--------------------------------------
    def make_response_string(response: {}, dat: int) -> str:
        def get_needed_datestring(dt) -> str:
            if dt == 1:
                return "за 24 часа"
            if dt == 30:
                return "за месяц"
            if dt == 365:
                return "за год"
            if dt == 0:
                return "за всё время"
        if response["code"] != "2" and response['code'] != "3":
            if response["code"] == "0":
                return "{}, самый топовый клип {} PogU {} ".format(nickname, get_needed_datestring(dat), response["url"])
            else:
                return "{}, самый топовый клип по категории {} {} PogU {} ".format(nickname, argument, get_needed_datestring(dat), response["url"])
        if response['code'] == "2":
            return "{}, такой категории нет PeepoWeird ".format(nickname)
        if response['code'] == "3":
            return "{}, из 3000 клипов не было найдено ни одного с такой категорией DaUj ".format(nickname)
    #------------------------------------helping with abreviatures---------------------------
    def abreviatur_helper(argument: str) -> str:
        with open('data/abreviatures.txt') as n:
            ad = json.loads(n.read())
            if argument in ad:
                return ad[argument]
            return ""
    #-------------------------------------method itself--------------------------------------
    id_game = "0"
    if len(argument) > 0:
        print(argument + "  " + str(len(argument)))
        if len(argument) <= 5 and abreviatur_helper(argument) != "":
            argument = abreviatur_helper(argument)
        qstr = quote(argument)
        url = "https://api.twitch.tv/helix/games?name={}".format(qstr)
        request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(config.OAUTH),
                                                           "Client-ID": "{}".format(config.CLIENT_ID)})
        try:
            response = urllib.request.urlopen(request).read()
            data = json.loads(response)
            for p in data["data"]:
                id_game = p['id']
            if id_game == "0":
                return make_response_string({"code": "2", "url": ""}, days_before)
        except:
            return make_response_string({"code": "2", "url": ""}, days_before)
    if days_before == 0:
        return make_response_string(do_request_for_getting_clip(id_game=id_game, ever=True), days_before)
    else:
        return make_response_string(do_request_for_getting_clip(id_game=id_game, days_before=days_before), days_before)

def parse_response_query(data: json) -> str:
    with open(file='data/aiml.txt', encoding='utf-8') as q:
        aiml = json.loads(q.read())
        if data['aiml'] in aiml:
            return data['aiml'] + " " + aiml[data['aiml']]
    with open(file='data/emotions.txt', encoding='utf-8') as q:
        emotions = json.loads(q.read().replace("'", '"'))
        if data['emotion'] in emotions:
            return data['aiml'] + " " + emotions[data['emotion']]
    with open(file='data/rubname.txt', encoding='utf-8') as q:
        newrubname = json.loads(q.read().replace("'", '"'))
        if data['newrubname'] in emotions:
            return data['aiml'] + " " + newrubname[data['newrubname']]
    return data['aiml'] + " P226Smug"

def get_goroskop(message, nickname) -> str:
    #----------------------method for getting goroskop-----------------
    def parse_goroskop(name: str) -> str:
        # ----------------------ifs----------------------------------------
        def choose_string_for_response(gor) -> str:
            with open(file='data/goroskopdictionary.txt', encoding='utf-8') as q:
                return json.loads(q.read())['response_strings'][gor]

        URL = 'https://www.wday.ru/horoscope/common/{}/daily/'.format(name)

        def get_html(url, params=None):
            r = requests.get(url, params=params)
            return r

        def get_content(html):
            soup = BeautifulSoup(html, 'html.parser')
            global goroskop
            global goroskop_day
            goroskop = soup.find('div', class_='tab-panel text active').get_text()
            goroskop_day = soup.find('h2', class_='horo-title').get_text()

        def parse():
            html = get_html(URL)
            get_content(html.text)

        parse()
        return '{} {} {}'.format(goroskop_day, choose_string_for_response(name), goroskop)

    # ----------------------ifs----------------------------------------
    if message == "+гороскоп":
        return "{}, введите +гороскоп [знак зодиака]".format(nickname)

    with open(file='data/goroskopdictionary.txt', encoding='utf-8') as q:
        gors = json.loads(q.read())
        if message in gors['query_strings']:
            return parse_goroskop(gors['query_strings'][message])
        else:
            return ""
