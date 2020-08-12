import sys
from abc import ABC
from twitchio.ext import commands
from datetime import timedelta, datetime
from bs4 import BeautifulSoup
import requests
import AdditionalMethods
import re
import random
import time
import subprocess
import config


class Bot(commands.Bot, ABC):

    def __init__(self):
        super().__init__(irc_token=f'oauth:{config.OAUTH}',
                         client_id=config.CLIENT_ID, nick=config.BOT, prefix='+',
                         initial_channels=config.CHANNELS)

    async def event_ready(self):
        print(f'Ready CommandsBot | {self.nick} on {self.initial_channels}')

    @commands.command(name='стрим')
    async def stream(self, ctx):
        s = ctx.send
        await s(AdditionalMethods.get_last_stream_stat())

    @commands.command(name='рецепт')
    async def recept(self, ctx):
        s = ctx.send
        URL = 'http://culinar.ivest.kz/randomMenu'

        def get_html(url, params=None):
            r = requests.get(url, params=params)
            return r

        def get_content(html):
            soup = BeautifulSoup(html, 'html.parser')
            global name
            global recept
            global recept1
            name = soup.find('a', class_='rec_name').get_text()
            recept = soup.find('div', class_='randome_recept_right').get_text()

        def parse():
            html = get_html(URL)
            get_content(html.text)

        parse()
        receptt = 'Способ приготовления:'.join(recept.split('Способ приготовления:')[:-1])
        recept1 = recept[recept.find("Способ приготовления:") + 1:]
        recept1 = (recept1[:495] + '...') if len(recept1) > 495 else recept1
        await s(f"{name} - {receptt}")
        time.sleep(2)
        await s(f"С{recept1}")

    @commands.command(name='анекдот')
    async def anekdot(self, ctx):
        s = ctx.send
        URL = 'http://anecdotica.ru/'

        def get_html(url, params=None):
            r = requests.get(url, params=params)
            return r

        def get_content(html):
            soup = BeautifulSoup(html, 'html.parser')
            global anekdot
            anekdot = soup.find('div', class_='item_text').get_text()

        def parse():
            html = get_html(URL)
            get_content(html.text)

        parse()
        anekdott = (anekdot[:493] + '...') if len(anekdot) > 493 else anekdot
        await s(f"{anekdott} KeK")

    @commands.command(name='курс')
    async def kurs(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        message = ctx.message.content
        URL = 'https://fortrader.org/quotes/usdrur'
        URL1 = 'https://fortrader.org/quotes/eurrur'

        def get_html(url, params=None):
            r = requests.get(url, params=params)
            return r

        def get_content(html, html1):
            soup = BeautifulSoup(html, 'html.parser')
            soup1 = BeautifulSoup(html1, 'html.parser')
            global dollar
            global euro
            dollar = soup.find('p', class_='rates_box1_inner pid-USDRUR-bid').get_text()
            euro = soup1.find('p', class_='rates_box1_inner pid-EURRUR-bid').get_text()

        def parse():
            html = get_html(URL)
            html1 = get_html(URL1)
            get_content(html.text, html1.text)

        parse()
        now = datetime.now() + timedelta(hours=3)
        today = now.strftime("%d.%m")

        if message == "+курс":
            await s(f"Курс валют на {today}: USD = {dollar} RUB | EURO = {euro} RUB")
        else:
            try:
                if message.find('+курс доллар-рубль') != -1:
                    kurs = str.replace(message, '+курс доллар-рубль ', '')
                    result = int(kurs) * float(dollar)
                    result = round(result, 2)
                    await s(f"{nickname}, {kurs} USD = {result} RUB")

                if message.find('+курс рубль-доллар') != -1:
                    kurs = str.replace(message, '+курс рубль-доллар ', '')
                    result = float(kurs) / float(dollar)
                    result = round(result, 2)
                    await s(f"{nickname}, {kurs} RUB = {result} USD")

                if message.find('+курс евро-рубль') != -1:
                    kurs = str.replace(message, '+курс евро-рубль ', '')
                    result = int(kurs) * float(euro)
                    result = round(result, 2)
                    await s(f"{nickname}, {kurs} EUR = {result} RUB")

                if message.find('+курс рубль-евро') != -1:
                    kurs = str.replace(message, '+курс рубль-евро ', '')
                    result = float(kurs) / float(euro)
                    result = round(result, 2)
                    await s(f"{nickname}, {kurs} RUB = {result} EUR")
            except OverflowError:
                await s("Число слишком большое WeirdChamp")

    @commands.command(name='topclipever')
    async def topclipever(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        message = ctx.message.content
        top = str.replace(message, '+topclipever ', '')
        top = re.sub("\n", '', top)
        if top == "+topclipever":
            top = ""
        await s(AdditionalMethods.gettopclip(0, top, nickname))

    @commands.command(name='topclipyear')
    async def topclipyear(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        message = ctx.message.content
        top = str.replace(message, '+topclipyear ', '')
        top = re.sub("\n", '', top)
        if top == "+topclipyear":
            top = ""
        await s(AdditionalMethods.gettopclip(365, top, nickname))

    @commands.command(name='topclipmonth')
    async def topclipmonth(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        message = ctx.message.content
        top = str.replace(message, '+topclipmonth ', '')
        top = re.sub("\n", '', top)
        if top == "+topclipmonth":
            top = ""
        await s(AdditionalMethods.gettopclip(30, top, nickname))

    @commands.command(name='topclipday')
    async def topclipday(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        message = ctx.message.content
        top = str.replace(message, '+topclipday ', '')
        top = re.sub("\n", '', top)
        if top == "+topclipday":
            top = ""
        await s(AdditionalMethods.gettopclip(1, top, nickname))

    @commands.command(name='iq')
    async def iq(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        iq = random.randrange(55, 180, 1)
        if iq == 110:
            await s(f"{nickname}, ваш IQ = {str(iq)}! Вы Хесус?! PogU")
        if iq == 89:
            await s(f"{nickname}, ваш IQ = {str(iq)}! Вы Братишкин?! PogU")
        else:
            if 110 > iq > 70:
                await s(f"{nickname}, ваш IQ = {str(iq)}! Надо же, у стримера больше IQ чем у вас KeK")
            if 110 < iq < 135:
                await s(f"{nickname}, ваш IQ = {str(iq)}! Ого, а вы не глупый человек ThumbUp")
            if iq < 70:
                await s(f"{nickname}, ваш IQ = {str(iq)}! Чел... сходи книгу почитай WeirdChamp")
            if iq >= 135:
                await s(f"{nickname}, ваш IQ = {str(iq)}! Внимание! В чате гений WAYTOOSMART Clap")

    @commands.command(name='паста')
    async def pasta(self, ctx):
        s = ctx.send
        await s(AdditionalMethods.parse_simplefile_message("{}", "nadya"))

    @commands.command(name='help')
    async def help(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        await s(
            f"{nickname}, Привет, я бот по имени слон. Можешь использовать следующие команды (страница 1): +паста, "
            f"+me, +do [message], +iq, +temp, +love [message], +бубу [message], +steal [message] Чтобы перейти на "
            f"следующую страницу введите +help1 catJAM")

    @commands.command(name='help1')
    async def help1(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        await s(
            f"{nickname}, страница 2: +привет [message], +try [message], +кнб, +time, +когда [message], +обнять ["
            f"message], +COCK, +BOOBS, +вниз Чтобы перейти на следующую страницу введите +help2")

    @commands.command(name='help2')
    async def help2(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        await s(
            f"{nickname}, страница 3: +анекдот, +гороскоп [message], +курс ['изначальная валюта'-'переводимая валюта'"
            f"(доллар-рубль, евро-рубль и наоборот)] [число], +рецепт, +topclipever [category], +topclipyear ["
            f"category], +topclipmonth [category], +topclipday [category]")

    @commands.command(name='temp')
    async def temp(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        tempp = random.uniform(25, 45)
        temp = round(tempp, 1)
        if 35.7 <= temp <= 37:
            await s(f"{nickname}, ваша температура {str(temp)} °C! У вас температура в норме ThumbUp")
        else:
            if 37 < temp < 40 or 35.7 > temp >= 32:
                await s(f"{nickname}, ваша температура {str(temp)} °C! У вас вирус? PepeS")
            else:
                if temp > 40 or temp < 32:
                    await s(f"{nickname}, ваша температура {str(temp)} °C! Вызывайте дурку! Durka")

    @commands.command(name='me')
    async def me(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        with open('data/me.txt', 'r', encoding='utf-8') as b:
            listme = list(b)
            randomm = random.choice(listme)
            randomm = re.sub("\n", '', randomm)
            await s(randomm.format(nickname))

    @commands.command(name='do')
    async def do(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        if message == "+do":
            await s(f"{nickname}, введите +do [message]")
        else:
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find(
                    'kill') != -1 or message.find('заходите') != -1:
                await s(f"{nickname}, думал забанить меня? WeirdChamp ")
            else:
                with open('data/do.txt', 'r', encoding='utf-8') as c:
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
        if message == "+бубу":
            await s(f"{nickname}, введите +бубу [something]")
        else:
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find(
                    'kill') != -1 or message.find('заходите') != -1:
                await s(f"{nickname}, думал забанить меня? WeirdChamp ")
            else:

                bubu = str.replace(message, '+бубу ', '')
                bubu = re.sub("\n", '', bubu)
                if len(bubu) < 235:
                    await s(f"Ну {str(bubu)} и {str(bubu)} Чё бубнить-то? ThumbUp")
                else:
                    await s("Слишком длинное бубу WeirdChamp ")

    @commands.command(name='love')
    async def love(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        if message == "+love":
            await s(f"{nickname}, введите +love [nickname]")
        else:
            procent = random.randrange(0, 100, 1)
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find(
                    'kill') != -1 or message.find('заходите') != -1:
                await s(f"{nickname}, думал забанить меня? WeirdChamp ")
            else:
                love = str.replace(message, '+love ', '')
                love = re.sub("\n", '', love)
                await s(f"{nickname} любит {str(love)} на {str(procent)} %!")

    @commands.command(name='steal')
    async def steal(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        if message == "+steal":
            await s(f"{nickname}, введите +steal [nickname]")
        else:
            procent = random.randrange(0, 100, 1)
            ruble = random.randrange(0, 2000, 1)
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find(
                    'kill') != -1 or message.find('заходите') != -1:
                await s(f"{nickname}, думал забанить меня? WeirdChamp ")
            else:
                steal = str.replace(message, '+steal ', '')
                steal = re.sub("\n", '', steal)
                if procent >= 33:
                    await s(f"{nickname} украл у {str(steal)} {str(ruble)} руб. BOP")
                else:
                    await s(f"{nickname} ничего не украл у {str(steal)} KeK Lohich")

    @commands.command(name='try')
    async def ttry(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        await s(
            AdditionalMethods.parse_standartfile_message(nickname, "{nickname} попробовал {messagestr}... {filestr}",
                                                         message, "+try", "try"))

    @commands.command(name='time')
    async def time(self, ctx):
        s = ctx.send
        await s(datetime.strftime(datetime.now() + timedelta(hours=3), "Чичас %H:%M по МСК Waiting"))

    @commands.command(name='обнять')
    async def hug(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        await s(AdditionalMethods.parse_standartfile_message(nickname, "{nickname} {filestr} обнимает {messagestr} "
                                                                       "VoHiYo",
                                                             message, "+обнять", "hug"))

    @commands.command(name='COCK')
    async def cock(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        cock = random.randrange(1, 36, 1)
        await s(f"{nickname}, твой COCK равен {str(cock)} см! YEP")

    @commands.command(name='кнб')
    async def cnb(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        listcnb = ['⛰', '✂️', '📜']
        usercnb = str.replace(message, '+кнб ', '')
        rndcnb1 = random.choice(listcnb)
        if message == '+кнб':
            await s(f"{nickname}, введите +кнб [камень, ножницы, бумага]")
        else:
            if usercnb == 'камень' and rndcnb1 == '⛰':
                await s(f"{nickname} поставил(а) ⛰ , а Бот поставил ⛰ . Ничья! ThumbUp")
            if usercnb == 'ножницы' and rndcnb1 == '✂️':
                await s(f"{nickname} поставил(а) ✂️ , а Бот поставил ✂️. Ничья! ThumbUp")
            if usercnb == 'бумага' and rndcnb1 == '📜':
                await s(f"{nickname} поставил(а) 📜 , а Бот поставил 📜 . Ничья! ThumbUp")
            if usercnb == 'бумага' and rndcnb1 == '⛰':
                await s(f"{nickname} поставил(а) 📜 , а Бот поставил ⛰ . Победа {nickname} EZ Clap")
            if usercnb == 'камень' and rndcnb1 == '📜':
                await s(f"{nickname} поставил(а) ⛰ , а Бот поставил 📜 . Победа Бота Lohich")
            if usercnb == 'камень' and rndcnb1 == '✂️':
                await s(f"{nickname} поставил(а) ⛰ , а Бот поставил ✂️. Победа {nickname} EZ Clap")
            if usercnb == 'ножницы' and rndcnb1 == '⛰':
                await s(f"{nickname} поставил(а) ✂️ , а Бот поставил ⛰ . Победа Бота Lohich")
            if usercnb == 'ножницы' and rndcnb1 == '📜':
                await s(f"{nickname} поставил(а) ✂️ , а Бот поставил 📜 . Победа {nickname} EZ Clap")
            if usercnb == 'бумага' and rndcnb1 == '✂️':
                await s(f"{nickname} поставил(а) 📜 , а Бот поставил ✂️. Победа Бота Lohich")

    @commands.command(name='BOOBS')
    async def boobs(self, ctx):
        nickname = ctx.author.name
        s = ctx.send
        boobs = random.randrange(0, 15, 1)
        await s(f"{nickname}, твои BOOBS {str(boobs)} размера YEP")

    @commands.command(name='вниз')
    async def vniz(self, ctx):
        s = ctx.send
        await s(AdditionalMethods.parse_simplefile_message(":point_down: {}", "down"))

    @commands.command(name='когда')
    async def kogda(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        await s(AdditionalMethods.parse_standartfile_message(nickname, "{nickname}, {messagestr} {filestr}",
                                                             message, "+когда", "kogda"))

    @commands.command(name='привет')
    async def privet(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        await s(AdditionalMethods.parse_standartfile_message(nickname,
                                                             "{nickname} передаёт {filestr} привет {messagestr} "
                                                             "peepoHey peepoLove",
                                                             message, "+привет", "privet"))

    @commands.command(name='гороскоп')
    async def goroskop(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        s = ctx.send
        goroskop = AdditionalMethods.get_goroskop(message, nickname)
        await s(goroskop)


subprocess.Popen([sys.executable, 'ChatBot.py'])
subprocess.Popen([sys.executable, 'CheckingStreamThread.py'])
bot = Bot()
bot.run()
