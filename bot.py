import sys
from abc import ABC
from twitchio.ext import commands
from datetime import timedelta, datetime
from bs4 import BeautifulSoup
import requests
import AdditionalMethods
import re
import random
import subprocess
import config
import json
import time


class Bot(commands.Bot, ABC):
    
    def __init__(self):
        super().__init__(irc_token=f'oauth:{config.OAUTH}',
                         client_id=config.CLIENT_ID, nick=config.BOT, prefix='!',
                         initial_channels=config.CHANNELS)

    async def event_ready(self):
        print(f'Ready CommandsBot | {self.nick} on {self.initial_channels}')

    @commands.command(name='history')
    async def stream(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        message = str.replace(message, '!history', '')
        if AdditionalMethods.check_on_bans(message, ctx.author):
            AdditionalMethods.add_to_buffer("c", AdditionalMethods.get_last_stream_stat(message[1:len(message)], nickname), ctx.author)

    @commands.command(name='archive')
    async def streamh(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        message = str.replace(message, '!archive', '')
        print(message)
        try:
            id=int(message[1:2])
            if len(message[2:len(message)]) > 1:
                tag = str.replace(message, f' {id} ', '')
            else:
                tag = ''
            if AdditionalMethods.check_on_bans(message, ctx.author):
                AdditionalMethods.add_to_buffer("c", AdditionalMethods.get_archive_stream_stat(id, nickname, tag).format(nickname, id), ctx.author)
        except:
            AdditionalMethods.add_to_buffer("c", f'{nickname} !archive [0-9]', ctx.author)
            
    @commands.command(name='рецепт')
    async def recept(self, ctx):
        if not AdditionalMethods.check_active():
            nickname = ctx.author.name
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
            print("ТЫ ПЬЯНЫЙ?")
            AdditionalMethods.add_to_buffer("r", f"{name} - {receptt}", ctx.author)
            AdditionalMethods.add_to_buffer("r", f"С{recept1}", ctx.author)

    @commands.command(name='анекдот')
    async def anekdot(self, ctx):
        if not AdditionalMethods.check_active():
            nickname = ctx.author.name
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
            AdditionalMethods.add_to_buffer("e", f"{anekdott} KeK", ctx.author)

    @commands.command(name='курс')
    async def kurs(self, ctx):
        nickname = ctx.author.name
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

        if message == "!курс":
            AdditionalMethods.add_to_buffer("c", f"Курс валют на {today}: USD = {dollar} RUB | EURO = {euro} RUB", ctx.author)
        else:
            try:
                if message.find('!курс доллар-рубль') != -1:
                    kurs = str.replace(message, '!курс доллар-рубль ', '')
                    result = float(kurs) * float(dollar)
                    result = round(result, 2)
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, {kurs} USD = {result} RUB", ctx.author)

                if message.find('!курс рубль-доллар') != -1:
                    kurs = str.replace(message, '!курс рубль-доллар ', '')
                    result = float(kurs) / float(dollar)
                    result = round(result, 2)
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, {kurs} RUB = {result} USD", ctx.author)

                if message.find('!курс евро-рубль') != -1:
                    kurs = str.replace(message, '!курс евро-рубль ', '')
                    result = float(kurs) * float(euro)
                    result = round(result, 2)
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, {kurs} EUR = {result} RUB", ctx.author)

                if message.find('!курс рубль-евро') != -1:
                    kurs = str.replace(message, '!курс рубль-евро ', '')
                    result = float(kurs) / float(euro)
                    result = round(result, 2)
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, {kurs} RUB = {result} EUR", ctx.author)
            except OverflowError:
                AdditionalMethods.add_to_buffer("c", "Число слишком большое WeirdChamp", ctx.author)

    @commands.command(name='topclipever')
    async def topclipever(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipever ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipever":
            top = ""
        if AdditionalMethods.check_on_bans(top, ctx.author):
            AdditionalMethods.add_to_buffer("c", AdditionalMethods.gettopclip(0, top, nickname), ctx.author)

    @commands.command(name='topclipyear')
    async def topclipyear(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipyear ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipyear":
            top = ""
        if AdditionalMethods.check_on_bans(top, ctx.author):
            AdditionalMethods.add_to_buffer("c", AdditionalMethods.gettopclip(365, top, nickname), ctx.author)

    @commands.command(name='topclipmonth')
    async def topclipmonth(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipmonth ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipmonth":
            top = ""
        if AdditionalMethods.check_on_bans(top, ctx.author):
            AdditionalMethods.add_to_buffer("c", AdditionalMethods.gettopclip(30, top, nickname), ctx.author)

    @commands.command(name='topclipday')
    async def topclipday(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipday ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipday":
            top = ""
        if AdditionalMethods.check_on_bans(top, ctx.author):
            AdditionalMethods.add_to_buffer("c", AdditionalMethods.gettopclip(1, top, nickname), ctx.author)

    @commands.command(name='iq')
    async def iq(self, ctx):
        if not AdditionalMethods.check_active():
            nickname = ctx.author.name
            iq = random.randrange(55, 180, 1)
            if iq == 110:
                AdditionalMethods.add_to_buffer("e", f"{nickname}, ваш IQ = {str(iq)}! Вы Хесус?! PogU", ctx.author)
            if iq == 89:
                AdditionalMethods.add_to_buffer("e", f"{nickname}, ваш IQ = {str(iq)}! Вы Братишкин?! PogU", ctx.author)
            else:
                if 110 > iq > 70:
                    AdditionalMethods.add_to_buffer("e", f"{nickname}, ваш IQ = {str(iq)}! Надо же, у стримера больше IQ чем у вас KeK", ctx.author)
                if 110 < iq < 135:
                    AdditionalMethods.add_to_buffer("e", f"{nickname}, ваш IQ = {str(iq)}! Ого, а вы не глупый человек ThumbUp", ctx.author)
                if iq < 70:
                    AdditionalMethods.add_to_buffer("e", f"{nickname}, ваш IQ = {str(iq)}! Чел... сходи книгу почитай WeirdChamp", ctx.author)
                if iq >= 135:
                    AdditionalMethods.add_to_buffer("e", f"{nickname}, ваш IQ = {str(iq)}! Внимание! В чате гений WAYTOOSMART Clap", ctx.author)

    @commands.command(name='паста')
    async def pasta(self, ctx):
        if not AdditionalMethods.check_active():
            AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_simplefile_message("{}", "nadya"), ctx.author)

    @commands.command(name='help')
    async def help(self, ctx):
        nickname = ctx.author.name
        if ctx.message.content != "!help":
            helper = str.replace(ctx.message.content, '!help ', '')
            helper = re.sub("\n", '', helper)
            with open('data/documentation.txt', 'r', encoding='utf-8') as w:
                data = json.loads(w.read())
                if helper in data:
                    prefix = "!"
                    if helper == "slonb0t" or helper == "SLONB0T":
                        prefix = "@"
                    AdditionalMethods.add_to_buffer("c", f"{nickname} {prefix}{helper} - {data[helper]}", ctx.author)
                else:
                    AdditionalMethods.add_to_buffer("c", f"{nickname} такой команды нет PepoG ", ctx.author)
        else:
            AdditionalMethods.add_to_buffer("c", f"{nickname}, Ку catJAM , меня зовут slonb0t catJAM , вот что я умею: страница 1: !help [command], !history [nickname], !archive [id] [nickname]"
            f", !topclipever [category], !topclipyear ["
            f"category], !topclipmonth [category], !topclipday [category] Чтобы перейти на следующую страницу введите !help1 catJAM ", ctx.author)

    @commands.command(name='help1')
    async def help1(self, ctx):
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("c", f"{nickname}, страница 2: !время, !гороскоп [знак зодиака], !анекдот, !рецепт, !привет [nickname], !try [action]"
            f", !кнб [камень, ножницы или бумага], !когда [message], !обнять [nickname], @slonb0t, @SLONB0T, "
            f" Чтобы перейти на следующую страницу введите !help2"
        , ctx.author)

    @commands.command(name='help2')
    async def help2(self, ctx):
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("c", f"{nickname}, страница 3: !паста, !курс ['изначальная валюта'-'переводимая валюта'(доллар-рубль, евро-рубль и наоборот)] [число], !iq, !temp"
                                             f", !бубу [message], !steal [nickname], !COCK, !BOOBS, !вниз, Чтобы перейти на следующую страницу введите !helpm", ctx.author)

    @commands.command(name='helpm')
    async def help3(self, ctx):
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("c", f"{nickname}, страница 4 (управление ботом, доступно модераторам и узкому кругу лиц): !usertimeout [time], !buferdelay [time]", ctx.author)

    @commands.command(name='usertimeout')
    async def usetime(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            timeout = str.replace(ctx.message.content, '!usertimeout ', '')
            timeout = re.sub("\n", '', timeout)
            timeout = str.replace(timeout, ",", ".")
            try:
                with open('data/settings.txt', 'r', encoding='utf-8') as b:
                    data = json.loads(b.read())
            except:
                data = {}
            with open('data/settings.txt', 'w', encoding='utf-8') as b:
                try:
                    data["usertimeout"] = float(timeout)
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s", f"{nickname}, ThumbUp", ctx.author)
                except:
                    AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author)

    @commands.command(name='buferdelay')
    async def bufedelay(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            timeout = str.replace(ctx.message.content, '!buferdelay ', '')
            timeout = re.sub("\n", '', timeout)
            timeout = str.replace(timeout, ",", ".")
            try:
                with open('data/settings.txt', 'r', encoding='utf-8') as b:
                    data = json.loads(b.read())
            except:
                data = {}
            with open('data/settings.txt', 'w', encoding='utf-8') as b:
                try:
                    data["buferdelay"] = float(timeout)
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s", f"{nickname}, ThumbUp", ctx.author)
                except:
                    AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author)

    @commands.command(name='temp')
    async def temp(self, ctx):
        if not AdditionalMethods.check_active():
            nickname = ctx.author.name
            tempp = random.uniform(25, 45)
            temp = round(tempp, 1)
            if 35.7 <= temp <= 37:
                AdditionalMethods.add_to_buffer("e", f"{nickname}, ваша температура {str(temp)} °C! У вас температура в норме ThumbUp", ctx.author)
            else:
                if 37 < temp < 40 or 35.7 > temp >= 32:
                    AdditionalMethods.add_to_buffer("e", f"{nickname}, ваша температура {str(temp)} °C! У вас вирус? PepeS", ctx.author)
                else:
                    if temp > 40 or temp < 32:
                        AdditionalMethods.add_to_buffer("e", f"{nickname}, ваша температура {str(temp)} °C! Вызывайте дурку! Durka", ctx.author)

    @commands.command(name='me')
    async def me(self, ctx):
        if not AdditionalMethods.check_active():
            nickname = ctx.author.name
            with open('data/me.txt', 'r', encoding='utf-8') as b:
                listme = list(b)
                randomm = random.choice(listme)
                randomm = re.sub("\n", '', randomm)
                AdditionalMethods.add_to_buffer("e", randomm.format(nickname), ctx.author)

    @commands.command(name='do')
    async def do(self, ctx):
        if not AdditionalMethods.check_active():
            message = ctx.message.content
            nickname = ctx.author.name
            if message == "!do":
                AdditionalMethods.add_to_buffer("e", f"{nickname}, введите !do [message]", ctx.author)
            else:
                do = str.replace(message, '!do ', '')
                do = re.sub("\n", '', do)
                if AdditionalMethods.check_on_bans(do, ctx.author):
                    with open('data/do.txt', 'r', encoding='utf-8') as c:
                        listme = list(c)
                        randomdo = random.choice(listme)
                        randomdo = re.sub("\n", '', randomdo)
                        AdditionalMethods.add_to_buffer("e", randomdo.format(nickname, do), ctx.author)

    @commands.command(name='бубу')
    async def bubu(self, ctx):
        if not AdditionalMethods.check_active():
            message = ctx.message.content
            nickname = ctx.author.name
            if message == "!бубу":
                AdditionalMethods.add_to_buffer("e", f"{nickname}, введите !бубу [something]", ctx.author)
            else:
                if AdditionalMethods.check_on_bans(message, ctx.author):
                    bubu = str.replace(message, '!бубу ', '')
                    bubu = re.sub("\n", '', bubu)
                    if len(bubu) < 235:
                        AdditionalMethods.add_to_buffer("e", f"Ну {str(bubu)} и {str(bubu)} Чё бубнить-то? ThumbUp", ctx.author)
                    else:
                        AdditionalMethods.add_to_buffer("e", "Слишком длинное бубу WeirdChamp ", ctx.author)

    @commands.command(name='steal')
    async def steal(self, ctx):
        if not AdditionalMethods.check_active():
            message = ctx.message.content
            nickname = ctx.author.name
            if message == "!steal":
                AdditionalMethods.add_to_buffer("e", f"{nickname}, введите !steal [nickname]", ctx.author)
            else:
                procent = random.randrange(0, 100, 1)
                ruble = random.randrange(0, 2000, 1)
                if AdditionalMethods.check_on_bans(message, ctx.author):
                    steal = str.replace(message, '!steal ', '')
                    steal = re.sub("\n", '', steal)
                    if procent >= 33:
                        AdditionalMethods.add_to_buffer("e", f"{nickname} украл у {str(steal)} {str(ruble)} руб. BOP", ctx.author)
                    else:
                        AdditionalMethods.add_to_buffer("e", f"{nickname} ничего не украл у {str(steal)} KeK Lohich", ctx.author)

    @commands.command(name='try')
    async def ttry(self, ctx):
        if not AdditionalMethods.check_active():
            message = ctx.message.content
            nickname = ctx.author.name
            if AdditionalMethods.check_on_bans(message, ctx.author):
                AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_standartfile_message(nickname, "{nickname} попробовал {messagestr}... {filestr}",
                                                             message, "!try", "try"), ctx.author)

    @commands.command(name='время')
    async def time(self, ctx):
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("c", datetime.strftime(datetime.now() + timedelta(hours=3), "Чичас %H:%M по МСК Waiting"), ctx.author)

    @commands.command(name='обнять')
    async def hug(self, ctx):
        if not AdditionalMethods.check_active():
            message = ctx.message.content
            nickname = ctx.author.name
            if AdditionalMethods.check_on_bans(message, ctx.author):
                AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_standartfile_message(nickname, "{nickname} {filestr} обнимает {messagestr} "
                                                                           "VoHiYo",
                                                                 message, "!обнять", "hug"), ctx.author)

    @commands.command(name='COCK')
    async def cock(self, ctx):
        if not AdditionalMethods.check_active():
            nickname = ctx.author.name
            cock = random.randrange(1, 36, 1)
            AdditionalMethods.add_to_buffer("e", f"{nickname}, твой COCK равен {str(cock)} см! YEP", ctx.author)

    @commands.command(name='кнб')
    async def cnb(self, ctx):
        if not AdditionalMethods.check_active():
            message = ctx.message.content
            nickname = ctx.author.name
            listcnb = ['⛰', '✂️', '📜']
            usercnb = str.replace(message, '!кнб ', '')
            rndcnb1 = random.choice(listcnb)
            if message == '!кнб':
                AdditionalMethods.add_to_buffer("e", f"{nickname}, введите !кнб [камень, ножницы, бумага]", ctx.author)
            else:
                if AdditionalMethods.check_on_bans(message, ctx.author):
                    if usercnb == 'камень' and rndcnb1 == '⛰':
                        AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) ⛰ , а Бот поставил ⛰ . Ничья! ThumbUp", ctx.author)
                    if usercnb == 'ножницы' and rndcnb1 == '✂️':
                        AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) ✂️ , а Бот поставил ✂️ . Ничья! ThumbUp", ctx.author)
                    if usercnb == 'бумага' and rndcnb1 == '📜':
                        AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) 📜 , а Бот поставил 📜 . Ничья! ThumbUp", ctx.author)
                    if usercnb == 'бумага' and rndcnb1 == '⛰':
                        AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) 📜 , а Бот поставил ⛰ . Победа {nickname} EZ Clap", ctx.author)
                    if usercnb == 'камень' and rndcnb1 == '📜':
                        AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) ⛰ , а Бот поставил 📜 . Победа Бота Lohich", ctx.author)
                    if usercnb == 'камень' and rndcnb1 == '✂️':
                        AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) ⛰ , а Бот поставил ✂️ . Победа {nickname} EZ Clap", ctx.author)
                    if usercnb == 'ножницы' and rndcnb1 == '⛰':
                        AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) ✂️ , а Бот поставил ⛰ . Победа Бота Lohich", ctx.author)
                    if usercnb == 'ножницы' and rndcnb1 == '📜':
                        AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) ✂️ , а Бот поставил 📜 . Победа {nickname} EZ Clap", ctx.author)
                    if usercnb == 'бумага' and rndcnb1 == '✂️':
                        AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) 📜 , а Бот поставил ✂️ . Победа Бота Lohich", ctx.author)

    @commands.command(name='BOOBS')
    async def boobs(self, ctx):
        if not AdditionalMethods.check_active():
            nickname = ctx.author.name
            boobs = random.randrange(0, 15, 1)
            AdditionalMethods.add_to_buffer("e", f"{nickname}, твои BOOBS {str(boobs)} размера YEP", ctx.author)

    @commands.command(name='вниз')
    async def vniz(self, ctx):
        if not AdditionalMethods.check_active():
            nickname = ctx.author.name
            AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_simplefile_message(":point_down: {}", "down"), ctx.author)

    @commands.command(name='когда')
    async def kogda(self, ctx):
        if not AdditionalMethods.check_active():
            message = ctx.message.content
            nickname = ctx.author.name
            if AdditionalMethods.check_on_bans(message, ctx.author):
                AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_standartfile_message(nickname, "{nickname}, {messagestr} {filestr}",
                                                                 message, "!когда", "kogda"), ctx.author)

    @commands.command(name='привет')
    async def privet(self, ctx):
        if not AdditionalMethods.check_active():
            message = ctx.message.content
            nickname = ctx.author.name
            if AdditionalMethods.check_on_bans(message, ctx.author):
                AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_standartfile_message(nickname,
                                                                     "{nickname} передаёт {filestr} привет {messagestr} "
                                                                     "peepoHey peepoLove",
                                                                     message, "!привет", "privet"), ctx.author)

    @commands.command(name='гороскоп')
    async def goroskop(self, ctx):
        if not AdditionalMethods.check_active():
            nickname = ctx.author.name
            message = ctx.message.content
            goroskop = AdditionalMethods.get_goroskop(message, nickname)
            AdditionalMethods.add_to_buffer("e", goroskop, ctx.author)


subprocess.Popen([sys.executable, 'ChatBot.py'])
subprocess.Popen([sys.executable, 'CheckingStreamThread.py'])
subprocess.Popen([sys.executable, 'buffer.py'])
bot = Bot()
bot.run()
