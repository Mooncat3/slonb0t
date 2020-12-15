import urllib.request
import urllib.response
from urllib.parse import quote
import time
from time import gmtime, strftime
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
import Settings


def check_on_max_or_not(arg: str) -> bool:
    if arg == "анекдот":
        return False
    elif arg == "ауф":
        return False
    elif arg == "creepypasta":
        return False
    elif arg == "creep":
        return False
    return True


def sendPaste(paste):
    url = "https://pastebin.com/api/api_post.php"
    req = requests.post(url, data=paste)
    return req.text


def createPaste(code, name, format_, private, date):
    dev_key = "6Dg9D7qLYfBZdZrq--nH5wfZ0507TjnN"
    p = {'api_dev_key': dev_key, 'api_option': 'paste', 'api_paste_code': code, 'api_paste_name': name,
         'api_paste_format': format_, 'api_paste_private': private, 'api_paste_expire_date': date}
    return p


def check_on_toomuchsimbols(string):
    return (string[:496] + '...') if len(string) >= 500 else string


def check_on_toomuchbool(string) -> bool:
    return len(string) >= 500


def vip(mod: bool, name: str) -> bool:
    if mod or name == "danantur" or name == "mooncat3":
        return True
    else:
        return False


def add_to_buffer(type: str, message: str, author: User, command: str):
    # message = '/me ' + message
    try:
        with open(file='data/buffer.txt', mode='r', encoding='utf-8') as e:
            dat = json.loads(e.read())
    except:
        dat = []
    while config.buferchanged:
        time.sleep(0.1)
    config.buferchanged = True
    if check_on_max_or_not(command):
        message = check_on_toomuchsimbols(message)
    with open(file='data/buffer.txt', mode='w', encoding='utf-8') as q:
        dat.append({"vip": vip(author.is_mod, author.name), "nickname": author.name, "type": type, "message": message,
                    "command": command})
        q.write(json.dumps(dat))
    config.buferchanged = False


def check_active(shouldchecksettings=True) -> bool:
    if shouldchecksettings:
        if not Settings.get_entertain():
            return True
    with open('data/TRASHMASSIVE.txt') as q:
        dat = json.loads(str(q.read()))
        return dat['active']
    
def parse_time(seconds: float, secs: bool = True):
    if seconds / 32140800 >= 1:
        return f"{int(seconds/32140800)}yr {int(strftime('%m', gmtime(seconds%32140800)))-1}mo"
    elif int(strftime('%m', gmtime(seconds))) >= 2:
        return f"{int(strftime('%m', gmtime(seconds)))-1}mo {int(strftime('%W', gmtime(seconds%2678400)))}wk"
    elif int(strftime('%W', gmtime(seconds))) >= 1:
        return f"{int(strftime('%W', gmtime(seconds)))}wk {int(strftime('%j', gmtime(seconds%604800)))-1}d"
    elif int(strftime('%j', gmtime(seconds))) >= 2:
        return f"{int(strftime('%j', gmtime(seconds)))-1}d {int(strftime('%H', gmtime(seconds)))}h"
    elif int(strftime('%H', gmtime(seconds))) >= 1:
        return f"{int(strftime('%H', gmtime(seconds)))}h {int(strftime('%M', gmtime(seconds)))}m"
    else:
        if secs:
            return f"{int(strftime('%M', gmtime(seconds)))}m {int(strftime('%S', gmtime(seconds)))}s"
        else:
            return f"{int(strftime('%M', gmtime(seconds)))}m"

def parse_stream_stat(nickname: str, tag: str, TRASHMASSIVE: dict, author: User, date="", id=0, active=False):
    def summ_times() -> time:
        timeq: time = 0.0
        for t in game_mass:
            if 'time' in t.keys():
                timeq = timeq + float(t['time'])
        return timeq

    id = len(TRASHMASSIVE['TRASHMASS']) - 1 - id
    strim_name = TRASHMASSIVE['TRASHMASS'][id]['name']
    strim_duration = parse_time(TRASHMASSIVE['TRASHMASS'][id]['duration'])
    viewsummcount = 0
    id_game = "0"
    game_mass = []
    timet = 0.0
    maxviewcount = 0
    for dat in TRASHMASSIVE['TRASHMASS'][id]['MASS']:
        viewsummcount += dat['ViewerCount']
        if dat['ViewerCount'] > maxviewcount:
            maxviewcount = dat['ViewerCount']
        if len(game_mass) > 0 and (id_game != dat['GAME_ID'] or (
                dat == TRASHMASSIVE['TRASHMASS'][id]['MASS'][len(TRASHMASSIVE['TRASHMASS'][id]['MASS']) - 1] and dat[
            'GAME_ID'] == TRASHMASSIVE['TRASHMASS'][id]['MASS'][len(TRASHMASSIVE['TRASHMASS'][id]['MASS']) - 2][
                    'GAME_ID'])):
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
    streamstat = {"Games": game_mass, "middleviewcount": viewsummcount / len(TRASHMASSIVE['TRASHMASS'][id]['MASS']),
                  "StreamName": strim_name,
                  "StreamDuration": strim_duration}
    categorystr = ""
    if 1 < len(tag) <= 26 and tag.find(" ") == -1:
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
        rounded = parse_time(r['time'])
        if len(rounded) > 0:
            categorystr += f"{r['name']} [{rounded}]"
            if r != streamstat['Games'][len(streamstat['Games']) - 1]:
                categorystr += " » "
        if not crash:
            crash = len(
                f"{nickname}{seter} {date} стрим: {streamstat['StreamName']} [{streamstat['StreamDuration']}] || среднее зр: {int(streamstat['middleviewcount'])} || {categorystr}") >= 500
        if crash and not already:
            already = True
            while len(
                    f"{nickname}{seter} {date} стрим: {streamstat['StreamName']} [{streamstat['StreamDuration']}] || "
                    f"среднее зр: {int(streamstat['middleviewcount'])} || {categorystr}") > 500 or categorystr[
                                                                                                   categorystr.rfind(
                                                                                                       "»") + 2: len(
                                                                                                       categorystr)] == f"{r['name']} [{rounded}]":
                categorystr = categorystr[0:categorystr.rfind("»") - 1]
            add_to_buffer("c",
                          f"{nickname}{seter} {date} стрим: {streamstat['StreamName']} [{streamstat['StreamDuration']}] || среднее зр: {int(streamstat['middleviewcount'])} || {categorystr}",
                          author, "history")
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


async def gettopclip(days_before: int = 0, argument: str = "", nickname: str = "", year: int = 0) -> str:
    # -------------------------------------checking for clip--------------------------------------
    async def do_request_for_getting_clip(id_game: str = "0", days_before: int = 0, ever: bool = False) -> {str: str}:
        try:
            if ever:
                if year == 0:
                    url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&first=100".format(config.BROADCASTER_ID)
                elif year > 0:
                    print()
                    datepast = rfc3339.format(datetime.strptime(f"{year}.01.01", '%Y.%m.%d').date(),
                                              utc=True,
                                              use_system_timezone=False)
                    datenow = rfc3339.format(datetime.strptime(f"{year + 1}.01.01", '%Y.%m.%d').date(), utc=True,
                                             use_system_timezone=False)
                    url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&started_at={}&ended_at={}&first=100".format(
                        config.BROADCASTER_ID, datepast,
                        datenow)
            else:
                datepast = rfc3339.format((datetime.utcnow() + timedelta(hours=3)) - timedelta(days=days_before),
                                          utc=True,
                                          use_system_timezone=False)
                datenow = rfc3339.format(datetime.utcnow() + timedelta(hours=3), utc=True, use_system_timezone=False)
                url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&started_at={}&ended_at={}&first=100".format(
                    config.BROADCASTER_ID, datepast,
                    datenow)
            request = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(config.OAUTH),
                                                               "Client-ID": "{}".format(config.CLIENT_ID)})
            response = urllib.request.urlopen(request).read()
            data: dict = json.loads(response)
            ident: int = 1
            if id_game == "0":
                for p in data["data"]:
                    return {"code": "0", "url": p['url']}
            elif id_game == "-1":
                config.istopcliprunning = True
                clips = []
                while True:
                    if ever:
                        if year == 0:
                            if 'cursor' in data['pagination'].keys():
                                url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&after={}&first=100".format(
                                    config.BROADCASTER_ID,
                                    data['pagination'][
                                        'cursor'])
                            else:
                                config.istopcliprunning = False
                                return {"code": "5", "url": random.choice(clips)}
                        else:
                            if 'cursor' in data['pagination'].keys():
                                url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&started_at={}&ended_at={}&after={}&first=100".format(
                                    config.BROADCASTER_ID,
                                    datepast,
                                    datenow,
                                    data['pagination'][
                                        'cursor'])
                            else:
                                config.istopcliprunning = False
                                return {"code": "5", "url": random.choice(clips)}
                    else:
                        if 'cursor' in data['pagination'].keys():
                            url = "https://api.twitch.tv/helix/clips?broadcaster_id={}&after={}&started_at={}&ended_at={}&first=100".format(
                                config.BROADCASTER_ID, data['pagination']['cursor'], datepast, datenow)
                        else:
                            config.istopcliprunning = False
                            return {"code": "5", "url": random.choice(clips)}
                    request = urllib.request.Request(url=url,
                                                     headers={"Authorization": "Bearer {}".format(config.OAUTH),
                                                              "Client-ID": "{}".format(config.CLIENT_ID)})
                    response = urllib.request.urlopen(request).read()
                    data = json.loads(response)
                    for p in data["data"]:
                        clips.append(p['url'])
                    if ident == count:
                        config.istopcliprunning = False
                        return {"code": "5", "url": random.choice(clips)}
                    else:
                        ident += 1
                    await asyncio.sleep(0.1)
            else:
                config.istopcliprunning = True
                while True:
                    for p in data["data"]:
                        if p['game_id'] == id_game:
                            config.istopcliprunning = False
                            return {"code": "1", "url": p['url']}
                    if ever:
                        config.istopcliprunning = False
                        return {"code": "3", "url": ""}
                    request = urllib.request.Request(url=url,
                                                     headers={"Authorization": "Bearer {}".format(config.OAUTH),
                                                              "Client-ID": "{}".format(config.CLIENT_ID)})
                    response = urllib.request.urlopen(request).read()
                    data = json.loads(response)
                    if ident == count:
                        config.istopcliprunning = False
                        return {"code": "3", "url": ""}
                    else:
                        ident += 1
                    await asyncio.sleep(0.5)
        except Exception as ex:
            print(f"EXCEPTION IN CLIPS:  {ex}")
            config.istopcliprunning = False
            return {"code": "3", "url": ""}

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
            if dt == 0 and year == 0:
                return "за всё время"
            else:
                return f"за {year} год"

        if response["code"] == "0":
            return "{}, самый топовый клип {} PogU {} ".format(nickname, get_needed_datestring(dat),
                                                               response["url"])
        elif response["code"] == "1":
            return "{}, самый топовый клип по категории {} {} PogU {} ".format(nickname, argument,
                                                                               get_needed_datestring(dat),
                                                                               response["url"])
        elif response['code'] == "2":
            return "{}, такой категории нет FeelsBadMan ".format(nickname)
        elif response['code'] == "3":
            return "{}, из 1000 клипов не было найдено ни одного с такой категорией DaUj ".format(nickname)
        elif response['code'] == "4":
            return "{}, сейчас идёт поиск другого клипа ".format(nickname)
        elif response['code'] == "5":
            return "{}, случайный клип {} PogU {} ".format(nickname, get_needed_datestring(dat),
                                                           response["url"])
        elif response['code'] == "6":
            return "{}, {}".format(nickname, response["url"])

    # ------------------------------------helping with abreviatures---------------------------
    def abreviatur_helper(argument: str) -> str:
        with open('data/abreviatures.txt') as n:
            ad = json.loads(n.read())
            if argument in ad:
                return ad[argument]
            return ""

    # -------------------------------------method itself--------------------------------------
    argument = argument.lower()
    if config.istopcliprunning:
        return make_response_string({"code": "4", "url": ""}, days_before)
    id_game = "0"
    if days_before == 0:
        count = 11
    else:
        count = 6
    if len(argument) > 0:
        if argument == "rand":
            id_game = "-1"
        else:
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
        return make_response_string(await do_request_for_getting_clip(id_game=id_game, days_before=days_before),
                                    days_before)


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
    return data['aiml'] + " catFax"

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
    if message == "!гороскоп":
        return "{}, введите !гороскоп [знак зодиака]".format(nickname)

    with open(file='data/goroskopdictionary.txt', encoding='utf_8') as q:
        gors = json.loads(q.read())
    if message.lower() in gors['query_strings']:
        return parse_goroskop(gors['query_strings'][message.lower()])
    else:
        return f"{nickname} введите правильный знак зодиака WeirdChamp"
