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
import asyncio
from twitchioc.dataclasses import User


def summvalue(start: str, end: str, value: float, dollar: float, euro: float, iens: float, grivn: float):
    result = "неккоректно написаны валюты, пишите в именительном падеже (рубль-доллар и т.д.)"
    splited = start + end
    if splited.find("рубль") != -1:
        if start == "рубль":
            if end == "доллар":
                result = f"{value} RUB = {round(value / dollar, 2)} USD"
            elif end == "евро":
                result = f"{value} RUB = {round(value / euro, 2)} EUR"
            elif end == "йена":
                result = f"{value} RUB = {round(value / iens, 2)} JPY"
            elif end == "гривны":
                result = f"{value} RUB = {round(value / grivn, 2)} UAH"
        else:
            if start == "доллар":
                result = f"{value} USD = {round(value * dollar, 2)} RUB"
            elif start == "евро":
                result = f"{value} EUR = {round(value * euro, 2)} RUB"
            elif start == "йена":
                result = f"{value} JPY = {round(value * iens, 2)} RUB"
            elif start == "гривны":
                result = f"{value} UAH = {round(value * grivn, 2)} RUB"
    elif splited.find("доллар") != -1:
        if start == "доллар":
            if end == "евро":
                result = f"{value} USD = {round(value * dollar / euro, 2)} EUR"
            elif end == "йена":
                result = f"{value} USD = {round(value * dollar / iens, 2)} JPY"
            elif end == "гривны":
                result = f"{value} USD = {round(value * dollar / grivn, 2)} UAH"
        else:
            if start == "евро":
                result = f"{value} EUR = {round(value * euro / dollar, 2)} USD"
            elif start == "йена":
                result = f"{value} JPY = {round(value * iens / dollar, 2)} USD"
            elif start == "гривны":
                result = f"{value} UAH = {round(value * grivn / dollar, 2)} USD"
    elif splited.find("йена") != -1:
        if start == "йена":
            if end == "евро":
                result = f"{value} JPY = {round(value * iens / euro, 2)} EUR"
            elif end == "гривны":
                result = f"{value} JPY = {round(value * iens / grivn, 2)} UAH"
        else:
            if start == "евро":
                result = f"{value} EUR = {round(value * euro / iens, 2)} JPY"
            elif start == "гривны":
                result = f"{value} UAH = {round(value * grivn / iens, 2)} JPY"
    else:
        if start == "евро":
            result = f"{value} EUR = {round(value * euro / grivn, 2)} UAH"
        elif end == "гривны":
            result = f"{value} UAH = {round(value * grivn / euro, 2)} EUR"
    return result



def sendPaste(paste):
    url = "https://pastebin.com/api/api_post.php"
    req = requests.post(url, data=paste)
    return req.text

def createPaste(code, name, format_, private, date):
    dev_key = "6Dg9D7qLYfBZdZrq--nH5wfZ0507TjnN"
    p = {}
    p['api_dev_key'] = dev_key
    p['api_option'] = 'paste'
    p['api_paste_code'] = code
    p['api_paste_name'] = name
    p['api_paste_format'] = format_
    p['api_paste_private'] = private
    p['api_paste_expire_date'] = date
    return p


def get_bufer_max() -> float:
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as e:
        try:
            data = json.loads(e.read())
            return data['buffermax']
        except:
            return 5


def get_bufer_timeout() -> float:
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as e:
        try:
            data = json.loads(e.read())
            return data['bufferdelay']
        except:
            return 1.0


def check_on_toomuchsimbols(string):
    return (string[:493] + '...') if len(string) > 495 else string


def check_on_toomuchbool(string) -> bool:
    return len(string) >= 500


def vip(mod: bool, name: str) -> bool:
    if mod or name == "danantur" or name == "mooncat3":
        return True
    else:
        return False


def add_to_buffer(type: str, message: str, author: User, command: str):
    try:
        with open(file='data/buffer.txt', mode='r', encoding='utf-8') as e:
            dat = json.loads(e.read())
    except:
        dat = []
    while config.buferchanged:
        time.sleep(0.1)
    config.buferchanged = True
    with open(file='data/buffer.txt', mode='w', encoding='utf-8') as q:
        dat.append({"vip": vip(author.is_mod, author.name), "nickname": author.name, "type": type, "message": message, "command": command})
        q.write(json.dumps(dat))
    config.buferchanged = False


def check_active() -> bool:
    with open(file='data/settings.txt', mode='r', encoding='utf-8') as q:
        dat = json.loads(q.read())
        if not dat['entertain']:
            return True
    with open(file='data/TRASHMASSIVE.txt', mode='r', encoding='utf-8') as q:
        dat = json.loads(q.read())
        return dat['active']


def parse_stream_stat(nickname: str, tag: str, TRASHMASSIVE: dict, author: User, date="", id=0, active=False):
    def summ_times() -> time:
        timeq: time = 0.0
        for t in game_mass:
            if 'time' in t.keys():
                timeq = timeq + float(t['time'])
        return timeq
    def parse_time(timetet: time, secs: bool) -> str:
        rounded = ""
        timestart = timetet
        if timestart / 3600 >= 1:
            rounded += f"{int(timestart / 3600)}h"
            timestart = timestart % 3600
        if timestart / 60 >= 1:
            if rounded.find("h") != -1 and not secs:
                rounded += " "
            rounded += f"{int(timestart / 60)}m"
            timestart = timestart % 60
        if timestart >= 1 and (rounded.find("h") == -1 or secs):
            if rounded.find("m") != -1 and not secs:
                rounded += " "
            rounded += f"{int(timestart)}s"
        return rounded
    id = len(TRASHMASSIVE['TRASHMASS']) - 1 - id
    strim_name = TRASHMASSIVE['TRASHMASS'][id]['name']
    strim_duration = parse_time(TRASHMASSIVE['TRASHMASS'][id]['duration'], True)
    viewsummcount = 0
    id_game = "0"
    game_mass = []
    timet = 0.0
    maxviewcount = 0
    for dat in TRASHMASSIVE['TRASHMASS'][id]['MASS']:
        viewsummcount += dat['ViewerCount']
        if dat['ViewerCount'] > maxviewcount:
            maxviewcount = dat['ViewerCount']
        if len(game_mass) > 0 and (id_game != dat['GAME_ID'] or (dat == TRASHMASSIVE['TRASHMASS'][id]['MASS'][len(TRASHMASSIVE['TRASHMASS'][id]['MASS']) - 1] and dat['GAME_ID'] == TRASHMASSIVE['TRASHMASS'][id]['MASS'][len(TRASHMASSIVE['TRASHMASS'][id]['MASS']) - 2]['GAME_ID'])):
            game_mass[len(game_mass) - 1]['time'] = dat['time_of_update'] - timet
        if id_game != dat['GAME_ID']:
            if dat['GAME_ID'] != "Timeout":
                id_game = dat['GAME_ID']
                game_mass.append({"name": dat['GAME_ID']})
            else:
                id_game = "Timeout"
                game_mass.append({"name": "Timeout"})
            timet = dat['time_of_update']
            if len(game_mass) == 1:
                game_mass[len(game_mass) - 1]['time'] = dat['time_of_update']
            else:
                game_mass[len(game_mass) - 1]['time'] = dat['time_of_update'] - summ_times()
    streamstat = {"Games": game_mass, "middleviewcount": viewsummcount / len(TRASHMASSIVE['TRASHMASS'][id]['MASS']), "StreamName": strim_name,
                  "StreamDuration": strim_duration}
    categorystr = ""
    if len(tag) > 1 and len(tag) <= 26 and tag.find(" ") == -1:
        seter = ' ' + tag
        nickname = ''
    else:
        seter = ''
    if len(date) > 0:
        actualdate = datetime.strptime(date, "%m.%d.%y")
        date = datetime.strftime(actualdate, "%a, %d %B, %Y")
        date = f"[{date}]"
    else:
        if active:
            date = "текущий"
        else:
            date = "прошлый"
    crash = False
    already = False
    for r in streamstat['Games']:
        rounded = parse_time(r['time'], False)
        if len(rounded) > 0:
            categorystr += f"{r['name']} [{rounded}]"
            if r != streamstat['Games'][len(streamstat['Games']) - 1]:
                categorystr += " » "
        if not crash:
            crash = len(f"{nickname}{seter} {date} стрим: {streamstat['StreamName']} [{streamstat['StreamDuration']}] || среднее зр: {int(streamstat['middleviewcount'])} || {categorystr}") >= 500
        if crash and not already:
            already = True
            while len(f"{nickname}{seter} {date} стрим: {streamstat['StreamName']} [{streamstat['StreamDuration']}] || среднее зр: {int(streamstat['middleviewcount'])} || {categorystr}") > 500 or categorystr[categorystr.rfind("»")+2: len(categorystr)] == f"{r['name']} [{rounded}]":
                categorystr = categorystr[0:categorystr.rfind("»")-1]
            add_to_buffer("c", f"{nickname}{seter} {date} стрим: {streamstat['StreamName']} [{streamstat['StreamDuration']}] || среднее зр: {int(streamstat['middleviewcount'])} || {categorystr}", author)
            categorystr = ""
            if len(rounded) > 0:
                categorystr += f"{r['name']} [{rounded}]"
                if r != streamstat['Games'][len(streamstat['Games']) - 1]:
                    categorystr += " » "
    if not crash:
        return f"{nickname}{seter} {date} стрим: {streamstat['StreamName']} [{streamstat['StreamDuration']}] || среднее зр: {int(streamstat['middleviewcount'])} || {categorystr}"
    else:
        time.sleep(1)
        return f"{nickname}{seter} {categorystr}"


def get_archive_stream_stat(id, nickname, tag, author):
    with open(file='data/TRASHMASSIVE.txt', mode='r', encoding='utf-8') as q:
        TRASHMASSIVE = json.loads(q.read())
        if id <= len(TRASHMASSIVE['TRASHMASS']) - 1:
            date = TRASHMASSIVE['TRASHMASS'][len(TRASHMASSIVE['TRASHMASS']) - 1 - id]['date']
        else:
            return "{} стрима с id {} нет в архиве"
    return parse_stream_stat(nickname=nickname, tag=tag, TRASHMASSIVE=TRASHMASSIVE, date=date, id=id, author=author)


def get_last_stream_stat(tag, nickname, author):
    with open(file='data/TRASHMASSIVE.txt', mode='r', encoding='utf-8') as q:
        TRASHMASSIVE = json.loads(q.read())
        active = TRASHMASSIVE['active']
    return parse_stream_stat(nickname=nickname, tag=tag, TRASHMASSIVE=TRASHMASSIVE, active=active, author=author)


def parse_standartfile_message(nickname, formatable, message, command, name_of_file) -> str:
    if message == command:
        return f"{nickname}, введите {command} [message]"
    else:
        if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1 or message.find(
                'заходите') != -1:
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


async def gettopclip(days_before: int = 0, argument: str = "", nickname: str = "") -> str:
    # -------------------------------------checking for clip--------------------------------------
    async def do_request_for_getting_clip(id_game: str = "0", days_before: int = 0, ever: bool = False) -> {str: str}:
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
            config.istopcliprunning = True
            while True:
                for p in data["data"]:
                    if p['game_id'] == id_game:
                        config.istopcliprunning = False
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
                    config.istopcliprunning = False
                    return {"code": "3", "url": ""}
                else:
                    ident += 1
                await asyncio.sleep(0.5)

    # -------------------------------------making response string--------------------------------------
    def make_response_string(response: {}, dat: int) -> str:
        def get_needed_datestring(dt) -> str:
            if dt == 1:
                return "за 24 часа"
            if dt == 7:
                return "за неделю"
            if dt == 30:
                return "за месяц"
            if dt == 365:
                return "за год"
            if dt == 0:
                return "за всё время"

        if response["code"] != "2" and response['code'] != "3" and response['code'] != "4":
            if response["code"] == "0":
                return "{}, самый топовый клип {} PogU {} ".format(nickname, get_needed_datestring(dat),
                                                                   response["url"])
            else:
                return "{}, самый топовый клип по категории {} {} PogU {} ".format(nickname, argument,
                                                                                   get_needed_datestring(dat),
                                                                                   response["url"])
        if response['code'] == "2":
            return "{}, такой категории нет FeelsBadMan ".format(nickname)
        if response['code'] == "3":
            return "{}, из 3000 клипов не было найдено ни одного с такой категорией DaUj ".format(nickname)
        if response['code'] == "4":
            return "{}, сейчас идёт поиск другого клипа ".format(nickname)

    # ------------------------------------helping with abreviatures---------------------------
    def abreviatur_helper(argument: str) -> str:
        with open('data/abreviatures.txt') as n:
            ad = json.loads(n.read())
            if argument in ad:
                return ad[argument]
            return ""

    # -------------------------------------method itself--------------------------------------
    if config.istopcliprunning:
        return make_response_string({"code": "4", "url": ""}, days_before)
    id_game = "0"
    if len(argument) > 0:
        print(argument + "  " + str(len(argument)))
        if len(argument) <= 6 and abreviatur_helper(argument) != "":
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
        return make_response_string(await do_request_for_getting_clip(id_game=id_game, ever=True), days_before)
    else:
        return make_response_string(await do_request_for_getting_clip(id_game=id_game, days_before=days_before), days_before)


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


def get_goroskop(message: str, nickname) -> str:
    # ----------------------method for getting goroskop-----------------
    def parse_goroskop(name: str) -> str:
        # ----------------------ifs----------------------------------------
        def choose_string_for_response(gor) -> str:
            with open(file='data/goroskopdictionary.txt', encoding='utf_8') as q:
                return json.loads(q.read())['response_strings'][gor]

        r = requests.get('https://www.wday.ru/horoscope/common/{}/daily/'.format(name))
        soup = BeautifulSoup(r.content, 'lxml')
        goroskop = soup.find('div', class_='tab-panel text active').get_text()
        goroskop_day = soup.find('h2', class_='horo-title').get_text()

        return '{} {} {} {}'.format(nickname, goroskop_day, choose_string_for_response(name), goroskop)

    # ----------------------ifs----------------------------------------
    if message == "+гороскоп":
        return "{}, введите +гороскоп [знак зодиака]".format(nickname)

    with open(file='data/goroskopdictionary.txt', encoding='utf_8') as q:
        gors = json.loads(q.read())
        if message.lower() in gors['query_strings']:
            return parse_goroskop(gors['query_strings'][message.lower()])
        else:
            return f"{nickname} введите правильный знак зодиака WeirdChamp"
