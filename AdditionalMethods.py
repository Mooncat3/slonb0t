import urllib.request
import urllib.response
from urllib.parse import quote
import json
import rfc3339
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import random
import re

BROADCASTER_ID = "34711476"
OAUTH = "2ed7e435kk3dm1tpgo73gnu7xcjczy"
CLIENT_ID = "gp762nuuoqcoxypju8c569th9wz7q5"


def parse_standartfile_message(nickname, formatable, message, command, name_of_file) -> str:
    if message == command:
        return f"@{nickname}, введите {command} [message]"
    else:
        if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1 or message.find('заходите') != -1:
            return f"@{nickname}, думал забанить меня? WeirdChamp "
        else:
            with open(f'{name_of_file}.txt', 'r', encoding='utf-8') as c:
                List = list(c)
                randomm = random.choice(List)
                randomm = re.sub("\n", '', randomm)
                subject = str.replace(message, f'{command} ', '')
                subject = re.sub("\n", '', subject)
                return formatable.format(nickname=nickname, filestr=randomm, messagestr=subject)

def parse_simplefile_message(formatable, name_of_file) -> str:
    with open(f'{name_of_file}.txt', 'r', encoding='utf-8') as n:
        List = list(n)
        randomm = random.choice(List)
        randomm = re.sub("\n", '', randomm)
        return formatable.format(str(randomm))

def gettopclip(days_before: int = 0, argument: str = "", nickname: str = "") -> str:
    #-------------------------------------checking for clip--------------------------------------
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
                    url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&after={}".format(BROADCASTER_ID,
                                                                                                data['pagination'][
                                                                                                    'cursor'])
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
        with open('abreviatures.txt') as n:
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
        request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(OAUTH),
                                                           "Client-ID": "{}".format(CLIENT_ID)})
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
    with open(file='aiml.txt', encoding='utf-8') as q:
        aiml = json.loads(q.read())
        if data['aiml'] in aiml:
            return data['aiml'] + " " + aiml[data['aiml']]
    with open(file='emotions.txt', encoding='utf-8') as q:
        emotions = json.loads(q.read().replace("'", '"'))
        if data['emotion'] in emotions:
            return data['aiml'] + " " + emotions[data['emotion']]
    with open(file='rubname.txt', encoding='utf-8') as q:
        newrubname = json.loads(q.read().replace("'", '"'))
        if data['newrubname'] in emotions:
            return data['aiml'] + " " + newrubname[data['newrubname']]
    return data['aiml'] + " P226Smug"

def get_goroskop(message, nickname) -> str:
    #----------------------method for getting goroskop-----------------
    def parse_goroskop(name: str) -> str:
        # ----------------------ifs----------------------------------------
        def choose_string_for_response(gor) -> str:
            with open(file='goroskopdictionary.txt', encoding='utf-8') as q:
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

    with open(file='goroskopdictionary.txt', encoding='utf-8') as q:
        gors = json.loads(q.read())
        if message in gors['query_strings']:
            return parse_goroskop(gors['query_strings'][message])
        else:
            return ""
