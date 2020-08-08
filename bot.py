from twitchio.ext import commands
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import forApiCalls
import re
import random
import time


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token='oauth:2ed7e435kk3dm1tpgo73gnu7xcjczy', client_id='9qmki7jzmtz6qnjj4z35yucfn29xb9',
                         nick='SLONB0T', prefix='+', initial_channels=['danantur'])

    async def event_ready(self):
        print(f'Ready | {self.nick} on {self.initial_channels}')

    async def event_message(self, message):
        await self.handle_commands(message)

    @commands.command(name='анекдот')
    async def anekdot(self, ctx):
        message = ctx.message.content
        s = ctx.send
        URL = 'http://anecdotica.ru/'
        HEADERS = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'accept': '*/*'}
        def get_html(url, params=None):
            r = requests.get(url, headers=HEADERS, params=params)
            return r

        def get_content(html):
            soup = BeautifulSoup(html, 'html.parser')
            global anekdot
            anekdot = soup.find('div', class_='item_text').get_text()

        def parse():
            html = get_html(URL)
            get_content(html.text)

        parse()
        await s(anekdot + " KeK")

    @commands.command(name='гороскоп')
    async def goroskop(self, ctx):
        message = ctx.message.content
        s = ctx.send
        if message.find('+гороскоп овен') != -1:
            URL = 'https://www.wday.ru/horoscope/common/oven/daily/'
            HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36','accept': '*/*'}
            def get_html(url, params=None):
                r = requests.get(url, headers=HEADERS, params=params)
                return r
            def get_content(html):
                soup = BeautifulSoup(html, 'html.parser')
                global goroskop
                global goroskop_day
                goroskop = soup.find('div',class_='tab-panel text active').get_text()
                goroskop_day = soup.find('h2', class_='horo-title').get_text()
            def parse():
                html = get_html(URL)
                get_content(html.text)
            parse()
            await s(goroskop_day + ' для овенов - ' + goroskop)

        if message.find('+гороскоп телец') != -1:
            URL = 'https://www.wday.ru/horoscope/common/telec/daily/'
            HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36','accept': '*/*'}
            def get_html(url, params=None):
                r = requests.get(url, headers=HEADERS, params=params)
                return r
            def get_content(html):
                soup = BeautifulSoup(html, 'html.parser')
                global goroskop
                global goroskop_day
                goroskop = soup.find('div',class_='tab-panel text active').get_text()
                goroskop_day = soup.find('h2', class_='horo-title').get_text()
            def parse():
                html = get_html(URL)
                get_content(html.text)
            parse()
            await s(goroskop_day + ' для тельцов - ' + goroskop)

        if message.find('+гороскоп близнецы') != -1:
            URL = 'https://www.wday.ru/horoscope/common/bliznecy/daily/'
            HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36','accept': '*/*'}
            def get_html(url, params=None):
                r = requests.get(url, headers=HEADERS, params=params)
                return r
            def get_content(html):
                soup = BeautifulSoup(html, 'html.parser')
                global goroskop
                global goroskop_day
                goroskop = soup.find('div',class_='tab-panel text active').get_text()
                goroskop_day = soup.find('h2', class_='horo-title').get_text()
            def parse():
                html = get_html(URL)
                get_content(html.text)
            parse()
            await s(goroskop_day + ' для близнецов - ' + goroskop)

        if message.find('+гороскоп рак') != -1:
            URL = 'https://www.wday.ru/horoscope/common/rak/daily/'
            HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36','accept': '*/*'}
            def get_html(url, params=None):
                r = requests.get(url, headers=HEADERS, params=params)
                return r
            def get_content(html):
                soup = BeautifulSoup(html, 'html.parser')
                global goroskop
                global goroskop_day
                goroskop = soup.find('div',class_='tab-panel text active').get_text()
                goroskop_day = soup.find('h2', class_='horo-title').get_text()
            def parse():
                html = get_html(URL)
                get_content(html.text)
            parse()
            await s(goroskop_day + ' для раков - ' + goroskop)

        if message.find('+гороскоп лев') != -1:
            URL = 'https://www.wday.ru/horoscope/common/lev/daily/'
            HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36','accept': '*/*'}
            def get_html(url, params=None):
                r = requests.get(url, headers=HEADERS, params=params)
                return r
            def get_content(html):
                soup = BeautifulSoup(html, 'html.parser')
                global goroskop
                global goroskop_day
                goroskop = soup.find('div',class_='tab-panel text active').get_text()
                goroskop_day = soup.find('h2', class_='horo-title').get_text()
            def parse():
                html = get_html(URL)
                get_content(html.text)
            parse()
            await s(goroskop_day + ' для львов - ' + goroskop)

        if message.find('+гороскоп дева') != -1:
            URL = 'https://www.wday.ru/horoscope/common/deva/daily/'
            HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36','accept': '*/*'}
            def get_html(url, params=None):
                r = requests.get(url, headers=HEADERS, params=params)
                return r
            def get_content(html):
                soup = BeautifulSoup(html, 'html.parser')
                global goroskop
                global goroskop_day
                goroskop = soup.find('div',class_='tab-panel text active').get_text()
                goroskop_day = soup.find('h2', class_='horo-title').get_text()
            def parse():
                html = get_html(URL)
                get_content(html.text)
            parse()
            await s(goroskop_day + ' для дев - ' + goroskop)

        if message.find('+гороскоп весы') != -1:
            URL = 'https://www.wday.ru/horoscope/common/vesy/daily/'
            HEADERS = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                'accept': '*/*'}

            def get_html(url, params=None):
                r = requests.get(url, headers=HEADERS, params=params)
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
            await s(goroskop_day + ' для весов - ' + goroskop)

        if message.find('+гороскоп скорпион') != -1:
            URL = 'https://www.wday.ru/horoscope/common/skorpion/daily/'
            HEADERS = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                'accept': '*/*'}

            def get_html(url, params=None):
                r = requests.get(url, headers=HEADERS, params=params)
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
            await s(goroskop_day + ' для скорпионов - ' + goroskop)

        if message.find('+гороскоп стрелец') != -1:
            URL = 'https://www.wday.ru/horoscope/common/strelec/daily/'
            HEADERS = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                'accept': '*/*'}

            def get_html(url, params=None):
                r = requests.get(url, headers=HEADERS, params=params)
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
            await s(goroskop_day + ' для стрельцов - ' + goroskop)

        if message.find('+гороскоп козерог') != -1:
            URL = 'https://www.wday.ru/horoscope/common/kozerog/daily/'
            HEADERS = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                'accept': '*/*'}

            def get_html(url, params=None):
                r = requests.get(url, headers=HEADERS, params=params)
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
            await s(goroskop_day + ' для козерогов - ' + goroskop)

        if message.find('+гороскоп водолей') != -1:
            URL = 'https://www.wday.ru/horoscope/common/vodolej/daily/'
            HEADERS = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                'accept': '*/*'}

            def get_html(url, params=None):
                r = requests.get(url, headers=HEADERS, params=params)
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
            await s(goroskop_day + ' для водолеев - ' + goroskop)

        if message.find('+гороскоп рыба') != -1:
            URL = 'https://www.wday.ru/horoscope/common/ryby/daily/'
            HEADERS = {}

            def get_html(url, params=None):
                r = requests.get(url, headers=HEADERS, params=params)
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
            await s(goroskop_day + ' для рыб - ' + goroskop)

    @commands.command(name='topclipever')
    async def topclipever(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        message = ctx.message.content
        top = str.replace(message, '+topclipever ', '')
        top = re.sub("\n", '', top)
        result = forApiCalls.gettopclip(0, top)
        if result["code"] != "2":
            if result["code"] == "0":
                await s(nickname + ", самый топовый клип за всё время PogU {} ".format(result["url"]))
            else:
                await s(
                    nickname + ", самый топовый клип по категории {} за всё время PogU {} ".format(top, result["url"]))
        else:
            await s(nickname + ", в топе 100 за этот период такой категории нет Sadge")

    @commands.command(name='topclipyear')
    async def topclipyear(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        message = ctx.message.content
        top = str.replace(message, '+topclipyear ', '')
        top = re.sub("\n", '', top)
        result = forApiCalls.gettopclip(1, top)
        if result["code"] != "2":
            if result["code"] == "0":
                await s(nickname + ", самый топовый клип за год PogU {} ".format(result["url"]))
            else:
                await s(nickname + ", самый топовый клип по категории {} за год PogU {} ".format(top, result["url"]))
        else:
            await s(nickname + ", в топе 100 за этот период такой категории нет Sadge")

    @commands.command(name='topclipmonth')
    async def topclipmonth(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        message = ctx.message.content
        top = str.replace(message, '+topclipmonth ', '')
        top = re.sub("\n", '', top)
        result = forApiCalls.gettopclip(2, top)
        if result["code"] != "2":
            if result["code"] == "0":
                await s(nickname + ", самый топовый клип за месяц PogU {} ".format(result["url"]))
            else:
                await s(nickname + ", самый топовый клип по категории {} за месяц PogU {} ".format(top, result["url"]))
        else:
            await s(nickname + ", в топе 100 за этот период такой категории нет Sadge")

    @commands.command(name='topclipday')
    async def topclipday(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        message = ctx.message.content
        top = str.replace(message, '+topclipday ', '')
        top = re.sub("\n", '', top)
        result = forApiCalls.gettopclip(3, top)
        if result["code"] != "2":
            if result["code"] == "0":
                await s("{}, самый топовый клип за 24 часа PogU {} ".format(nickname, result["url"]))
            else:
                await s(
                    "{}, самый топовый клип по категории {} за 24 часа PogU {} ".format(nickname, top, result["url"]))
        else:
            await s("{}, в топе 100 за этот период такой категории нет Sadge".format(nickname))

    @commands.command(name='iq')
    async def iq(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        iq = random.randrange(55, 180, 1)
        if iq == 110:
            await s(nickname + ", ваш IQ = " + str(iq) + "! Вы Хесус?! PogU")
        if iq == 89:
            await s(nickname + ", ваш IQ = " + str(iq) + "! Вы Братишкин?! PogU")
        else:
            if iq < 110 and iq > 70:
                await s(nickname + ", ваш IQ = " + str(iq) + "! Надо же, у стримера больше IQ чем у вас KeK")
            if iq > 110 and iq < 135:
                await s(nickname + ", ваш IQ = " + str(iq) + "! Ого, а вы не глупый человек ThumbUp")
            if iq < 70:
                await s(nickname + ", ваш IQ = " + str(iq) + "! Чел... сходи книгу почитай WeirdChamp")
            if iq >= 135:
                await s(nickname + ", ваш IQ = " + str(iq) + "! Внимание! В чате гений WAYTOOSMART Clap")

    @commands.command(name='паста')
    async def pasta(self, ctx):
        s = ctx.send
        with open('nadya.txt', 'r', encoding='utf-8') as n:
            nadyaa = list(n)
            randomnadya = random.choice(nadyaa)
            randomnadya = re.sub("\n", '', randomnadya)
            await s(randomnadya)

    @commands.command(name='help')
    async def help(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        await s(nickname + ", Привет, я бот по имени слон. Можешь использовать следующие команды (страница 1): +паста, +me, +do [nickname], +iq, +temp, +love [nickname], +бубу [something], +steal [nickname] Чтобы перейти на следующую страницу введите +help1 catJAM")

    @commands.command(name='help1')
    async def help1(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        await s(nickname + ", страница 2: +привет [nickname], +try [something], +time, +когда [something], +обнять [nickname], +COCK, +BOOBS, +вверх Чтобы перейти на следующую страницу введите +help2")

    @commands.command(name='help2')
    async def help2(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        await s(nickname + ", страница 3: +анекдот, +гороскоп, +topclipever [category], +topclipyear [category], +topclipmonth [category], +topclipday [category]")

    @commands.command(name='temp')
    async def temp(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        tempp = random.uniform(25, 45)
        temp = round(tempp, 1)
        if temp >= 35.7 and temp <= 37:
            await s(nickname + ", ваша температура " + str(temp) + " °C! У вас температура в пределах нормы ThumbUp")
        else:
            if temp > 37 and temp < 40 or temp < 35.7 and temp >= 32:
                await s(nickname + ", ваша температура " + str(temp) + " °C! Вы больны? coronaS")
            else:
                if temp > 40 or temp < 32:
                    await s(nickname + ", ваша температура " + str(temp) + " °C! Срочно вызывайте скорую! Durka")

    @commands.command(name='me')
    async def me(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        with open('me.txt', 'r', encoding='utf-8') as b:
            listme = list(b)
            randomm = random.choice(listme)
            randomm = re.sub("\n", '', randomm)
            await s(randomm.format(nickname))

    @commands.command(name='do')
    async def do(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        if message[len('+do'):len(message)] == "":
            await s(nickname + ", введите +do [nickname]")
        else:
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1 or message.find('заходите') != -1:
                await s(nickname + ", думал забанить меня? WeirdChamp ")
            else:
                with open('do.txt', 'r', encoding='utf-8') as c:
                    listme = list(c)
                    randomdo = random.choice(listme)
                    randomdo = re.sub("\n", '', randomdo)
                    do = str.replace(message, '+do ', '')
                    do = re.sub("\n", '', do)
                    await s(randomdo.format(nickname, do))

    @commands.command(name='бубу')
    async def bubu(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        if message[len('+бубу'):len(message)] == "":
            await s(nickname + ", введите +бубу [something]")
        else:
            bubu = str.replace(message, '+бубу ', '')
            bubu = re.sub("\n", '', bubu)
            await s("Ну " + str(bubu) + " и " + str(bubu) + " Чё бубнить-то? ThumbUp")

    @commands.command(name='love')
    async def love(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        if message[len('+love'):len(message)] == "":
            await s(nickname + ", введите +love [nickname]")
        else:
            procent = random.randrange(0, 100, 1)
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1 or message.find(
                    'заходите') != -1:
                await s(nickname + ", думал забанить меня? WeirdChamp ")
            else:
                love = str.replace(message, '+love ', '')
                love = re.sub("\n", '', love)
                await s(nickname + " любит " + str(love) + " на " + str(procent) + "%!")

    @commands.command(name='steal')
    async def steal(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        if message[len('+steal'):len(message)] == "":
            await s(nickname + ", введите +steal [nickame]")
        else:
            procent = random.randrange(0, 100, 1)
            ruble = random.randrange(0, 2000, 1)
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1 or message.find(
                    'заходите') != -1:
                await s(nickname + ", думал забанить меня? WeirdChamp ")
            else:
                steal = str.replace(message, '+steal ', '')
                steal = re.sub("\n", '', steal)
                if procent >= 33:
                    await s(nickname + " украл у " + str(steal) + " " + str(ruble) + " руб. BOP")
                else:
                    await s(nickname + " ничего не украл у " + str(steal) + " KeK Lohich")

    @commands.command(name='try')
    async def ttry(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        if message[len('+try'):len(message)] == "":
            await s(nickname + ", введите +try [something]")
        else:
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1 or message.find(
                    'заходите') != -1:
                await s(nickname + ", думал забанить меня? WeirdChamp ")
            else:
                tryy = str.replace(message, '+try ', '')
                tryy = re.sub("\n", '', tryy)
                with open('try.txt', 'r', encoding='utf-8') as m:
                    listtry = list(m)
                    tryr = random.choice(listtry)
                    tryr = re.sub("\n", '', tryr)
                await s(nickname + " попробовал " + tryy + "... " + tryr)

    @commands.command(name='time')
    async def time(self, ctx):
        s = ctx.send
        await s(datetime.strftime(datetime.now() + timedelta(hours=3), "Чичас %H:%M:%S по МСК Waiting"))

    @commands.command(name='обнять')
    async def hug(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        if message[len('+обнять'):len(message)] == "":
            await s(nickname + ", введите +обнять [nickname]")
        else:
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1 or message.find(
                    'заходите') != -1:
                await s(nickname + ", думал забанить меня? WeirdChamp ")

            else:
                with open('hug.txt', 'r', encoding='utf-8') as j:
                    hugg = list(j)
                    randomhug = random.choice(hugg)
                    randomhug = re.sub("\n", '', randomhug)
                    hug = str.replace(message, '+обнять ', '')
                    hug = re.sub("\n", '', hug)
                    await s(nickname + " " + randomhug + " обнимает " + hug + " VoHiYo")

    @commands.command(name='COCK')
    async def cock(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        cock = random.randrange(1, 36, 1)
        await s(nickname + ", твой COCK равен " + str(cock) + " см! YEP")

    @commands.command(name='BOOBS')
    async def boobs(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        boobs = random.randrange(0, 7, 1)
        if boobs == 7:
            await s(nickname + ", твои BOOBS 6+ размера YEP PogU")
        else:
            await s(nickname + ", твои BOOBS " + str(boobs) + " размера YEP")

    @commands.command(name='вверх')
    async def vverh(self, ctx):
        s = ctx.send
        with open('down.txt', 'r', encoding='utf-8') as n:
            downn = list(n)
            randomdown = random.choice(downn)
            randomdown = re.sub("\n", '', randomdown)
            await s(":point_up_2: " + str(randomdown))

        """
    @commands.command(name='игры')
    async def hug(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        await s(nickname + ", cписок всех мини-игр у бота: +угадать число")

    @commands.command(name='угадать число')
    async def chislo(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        await s("Правила: бот загадывает число от 0 до 20. Ваша задача угадать это число. У вас есть минута. Pog нали!")
        number = random.randrange(0, 20, 1)
        for i in range(600, 0, -1):
            time.sleep(0.1)
            rubles = random.randrange(0, 5000, 1)
            if message.find(str(number)) != -1:
                await s(nickname + ", поздравляю! Ты победил! Приз " + str(rubles) + " руб. PepoParty ")
        await s("Чат проиграл, время вышло Sadge ")
        """

    @commands.command(name='когда')
    async def kogda(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        if message[len('+когда'):len(message)] == "":
            await s(nickname + ", введите +когда [something]")
        else:
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1 or message.find(
                    'заходите') != -1:
                await s(nickname + ", думал забанить меня? WeirdChamp ")
            else:
                with open('kogda.txt', 'r', encoding='utf-8') as m:
                    listkogda = list(m)
                    koogda = str.replace(message, '+когда ', '')
                    koogda = re.sub("\n", '', koogda)
                    kogda = random.choice(listkogda)
                    kogda = re.sub("\n", '', kogda)
                    await s(nickname + ", " + koogda + ' ' + kogda)

    @commands.command(name='привет')
    async def privet(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        if message[len('+привет'):len(message)] == "":
            await s(nickname + ", введите +привет [nickname]")
        else:
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1 or message.find(
                    'заходите') != -1:
                await s(nickname + ", думал забанить меня? WeirdChamp ")
            else:
                with open('privet.txt', 'r', encoding='utf-8') as c:
                    privit = list(c)
                    randommm = random.choice(privit)
                    randommm = re.sub("\n", '', randommm)
                    privet = str.replace(message, '+привет ', '')
                    privet = re.sub("\n", '', privet)
                    await s(nickname + " передаёт " + randommm + " привет " + privet + " peepoHey peepoLove")


bot = Bot()
bot.run()
