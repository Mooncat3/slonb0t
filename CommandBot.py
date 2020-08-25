# -*- coding: utf8 -*-
import sys
from abc import ABC
from github import Github
from twitchioc.ext import commands
from datetime import timedelta, datetime
from bs4 import BeautifulSoup
import requests
import AdditionalMethods
import re
import random
import subprocess
import config
import json


class CommandsBot(commands.Bot, ABC):

    def __init__(self):
        super().__init__(irc_token=f'oauth:{config.OAUTH}',
                         client_id=config.CLIENT_ID, nick=config.BOT, prefix='!',
                         initial_channels=config.CHANNELS)

    async def event_ready(self):
        print(f'Ready {str(self.__class__.__name__)} | {self.nick} on {self.initial_channels}')
       
    @commands.command(name='porf')
    async def dev(self, ctx):
        nickname = ctx.author.name
        word = str.replace(ctx.message.content, '!porf ', "")
        url = "https://models.dobro.ai/gpt2/medium/"
        if word == "!porf":
            AdditionalMethods.add_to_buffer("e", f"{nickname}, Впишите какое-либо предложение", ctx.author, "porf")
        elif len(word) > 300:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, Бот может принимать максимум 300 символов", ctx.author, "porf")
        else:
            response = requests.post(url, json={'prompt': word, 'length': '30', 'num_samples': '5'})
            result = str(response.text).replace('{"replies":["', '').replace('"]}', '').rpartition('","')[2]
            AdditionalMethods.add_to_buffer("e", AdditionalMethods.check_on_toomuchsimbols(f"{nickname}, " + word + result), ctx.author, "porf")

    @commands.command(name='save')
    async def logs(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            with open(file='data/TRASHMASSIVE.txt', mode='r', encoding='utf-8') as q:
                strer = q.read()
            g = Github("f0011283768114fac26230cd23b3208ed10d0a54")
            repo = g.search_repositories("slonb0t")[0]
            contents = repo.get_contents("data/TRASHMASSIVE.txt")
            repo.delete_file(contents.path, "", contents.sha)
            repo.create_file("data/TRASHMASSIVE.txt", "", strer)
            AdditionalMethods.add_to_buffer("s", "Синхронизация статистик произошла успешно", ctx.author, "save")

    @commands.command(name='slon')
    async def slon(self, ctx):
        nickname = ctx.author.name
        story = nickname + ", дело было летом 2019 года, хесус играл в майнкрафт без модов и смог приручить себе кота, которого мы прозвали Слон, в один прекрасный солнечный день, он залез под блок, где была вода, и, медленно задыхаясь, умер peepoSad , этот бот будет вечным напоминанием о трагедии, которую никто не забудет roflanPominy "
        AdditionalMethods.add_to_buffer("e", story, ctx.author, "slon")

    @commands.command(name='case')
    async def case(self, ctx):
        nickname = ctx.author.name
        randstr = random.randint(1, 179)
        r = requests.get('https://market.csgo.com/?s=name&r=&q=&p=' + str(randstr) + '&h=&fst=0')
        soup = BeautifulSoup(r.content, 'lxml')
        d = soup.find_all('a', class_='item')
        skin = str(random.choice(d)).partition(';"></div>')[2]
        skinorig = re.sub('<div class="price">', '', skin)
        skinorig = re.sub("\n", '', skinorig)
        skin = skinorig.partition(';">')[2].replace('</div></a>', '')
        price = skinorig.rpartition('<s')[0]
        price = re.sub(" ", '', price)
        if float(price) < 100:
            price = str(price) + " ₽ Lohich"
        elif float(price) < 500:
            price = str(price) + " ₽ SeemsGood"
        elif float(price) < 1000:
            price = str(price) + " ₽ dedU"
        elif float(price) < 5000:
            price = str(price) + " ₽ PogU"
        elif float(price) < 10000:
            price = str(price) + " ₽ PogChamp"
        elif float(price) < 100000:
            price = str(price) + " ₽ Pog"
        elif float(price) > 100000:
            price = str(price) + " ₽ Pog Clap"
        AdditionalMethods.add_to_buffer("e",
                                        f"{nickname}, вам выпал " + skin + " Стоимость: " + price,
                                        ctx.author, "case")

    @commands.command(name='history')
    async def stream(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        message = str.replace(message, '!history', '')
        AdditionalMethods.add_to_buffer("e", AdditionalMethods.get_last_stream_stat(message[1:len(message)], nickname, ctx.author), ctx.author, "history")

    @commands.command(name='archive')
    async def streamh(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        message = str.replace(message, '!archive', '')
        try:
            id=int(message[1:2])
            if len(message[2:len(message)]) > 1:
                tag = str.replace(message, f' {id} ', '')
            else:
                tag = ''
            AdditionalMethods.add_to_buffer("c", AdditionalMethods.get_archive_stream_stat(id, nickname, tag, ctx.author).format(nickname, id), ctx.author, "archive")
        except:
            AdditionalMethods.add_to_buffer("с", f'{nickname} !archive [0-9]', ctx.author, "archive")

    @commands.command(name='рецепт')
    async def recept(self, ctx):
        r = requests.get('http://culinar.ivest.kz/randomMenu')
        soup = BeautifulSoup(r.content, 'lxml')
        name = soup.find('a', class_='rec_name').get_text()
        recept = soup.find('div', class_='randome_recept_right').get_text()
        receptt = 'Способ приготовления:'.join(recept.split('Способ приготовления:')[:-1])
        recept1 = recept[recept.find("Способ приготовления:") + 1:]
        recept1 = (recept1[:495] + '...') if len(recept1) > 495 else recept1
        AdditionalMethods.add_to_buffer("r", f"{name} - {receptt}", ctx.author, "рецепт")
        AdditionalMethods.add_to_buffer("r", f"С{recept1}", ctx.author, "рецепт")

    @commands.command(name='анекдот')
    async def anekdot(self, ctx):
        r = requests.get('http://anecdotica.ru/')
        soup = BeautifulSoup(r.content, 'lxml')
        anekdot = soup.find('div', class_='item_text').get_text()
        anekdott = (anekdot[:493] + '...') if len(anekdot) > 493 else anekdot
        AdditionalMethods.add_to_buffer("e", '{} KeK'.format(str.replace(anekdott, "\r\n", " ")), ctx.author, "анекдот")

    @commands.command(name='курс')
    async def kurs(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        r = requests.get('https://fortrader.org/quotes/usdrur')
        r1 = requests.get('https://fortrader.org/quotes/eurrur')
        r2 = requests.get('https://fortrader.org/currencyrates/jpy')
        r3 = requests.get('https://fortrader.org/currencyrates/uah')
        
        soup = BeautifulSoup(r.content, 'lxml')
        soup1 = BeautifulSoup(r1.content, 'lxml')
        soup2 = BeautifulSoup(r2.content, 'lxml')
        soup3 = BeautifulSoup(r3.content, 'lxml')
        
        dollar = soup.find('p', class_='rates_box1_inner pid-USDRUR-bid').get_text()
        euro = soup1.find('p', class_='rates_box1_inner pid-EURRUR-bid').get_text()
        jpy = soup2.find('input', class_='converter_form_inp converterInpTo').get(key="value")
        uah = soup3.find('input', class_='converter_form_inp converterInpTo').get(key="value")

        now = datetime.now() + timedelta(hours=3)
        today = now.strftime("%d.%m")

        if message == "!курс":
            AdditionalMethods.add_to_buffer("c",
                                            f"Курс валют на {today}: USD = {dollar} RUB | EUR = {euro} RUB | JPY = {jpy} RUB | UAH = {uah} RUB",
                                            ctx.author, "")
        else:
            try:
                if message.find(' ', message.find('-')) != -1:
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, {AdditionalMethods.summvalue(message[message.find(' ') + 1:message.find('-')], message[message.find('-') + 1:message.find(' ', message.find('-'))], float(message[message.find(' ', message.find('-')) + 1:len(message)]), float(dollar), float(euro), float(jpy), float(uah))}", ctx.author, "курс")
                else:
                    AdditionalMethods.add_to_buffer("c",
                                                    f"{nickname}, впишите количество переводимой валюты",
                                                    ctx.author, "курс")
            except OverflowError:
                AdditionalMethods.add_to_buffer("с", f"{nickname} Число слишком большое WeirdChamp", ctx.author, "курс")
            except ValueError:
                AdditionalMethods.add_to_buffer("с", f"{nickname} Это не число WeirdChamp", ctx.author, "курс")

    @commands.command(name='topclipever')
    async def topclipever(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipever ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipever":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(0, top, nickname), ctx.author, "topclip")

    @commands.command(name='topclipyear')
    async def topclipyear(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipyear ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipyear":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(365, top, nickname), ctx.author, "topclip")

    @commands.command(name='topclipweek')
    async def topclipweek(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipweek ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipweek":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(7, top, nickname), ctx.author, "topclip")

    @commands.command(name='topclipmonth')
    async def topclipmonth(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipmonth ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipmonth":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(30, top, nickname), ctx.author, "topclip")

    @commands.command(name='topclipday')
    async def topclipday(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipday ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipday":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(1, top, nickname), ctx.author, "topclip")

    @commands.command(name='abbreviations')
    async def abbreviations(self, ctx):
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("c", f"{nickname} Здесь вы можете посмотреть все доступные аббревиатуры в topclip {config.abreviationsUrl}", ctx.author, "abbreviations")

    @commands.command(name='iq')
    async def iq(self, ctx):
        nickname = ctx.author.name
        iq = random.randrange(55, 180, 1)
        if iq == 110:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, ваш IQ = {str(iq)}! Вы Хесус?! PogU", ctx.author, "iq")
        if iq == 89:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, ваш IQ = {str(iq)}! Вы Братишкин?! PogU", ctx.author, "iq")
        else:
            if 110 > iq > 70:
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname}, ваш IQ = {str(iq)}! Надо же, у стримера больше IQ чем у вас KeK",
                                                ctx.author, "iq")
            if 110 < iq < 135:
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname}, ваш IQ = {str(iq)}! Ого, а вы не глупый человек ThumbUp",
                                                ctx.author, "iq")
            if iq < 70:
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname}, ваш IQ = {str(iq)}! Чел... сходи книгу почитай WeirdChamp",
                                                ctx.author, "iq")
            if iq >= 135:
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname}, ваш IQ = {str(iq)}! Внимание! В чате гений WAYTOOSMART Clap",
                                                ctx.author, "iq")
                                                    
    @commands.command(name='паста')
    async def pasta(self, ctx):
        AdditionalMethods.add_to_buffer("s", AdditionalMethods.parse_simplefile_message("{}", "nadya"), ctx.author, "паста")

    @commands.command(name='help')
    async def help(self, ctx):
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("c", f"catJAM Ку, {nickname}, меня зовут SLONB0T catJAM , моя история довольно короткая и грустная BibleThump (если хочешь её увидеть введи !slon), но я воскрес, чтобы жить вечно AngelThump со списком команд можешь ознакомиться здесь {config.helpUrl}", ctx.author, "help")

    @commands.command(name='helpm')
    async def helpm(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            AdditionalMethods.add_to_buffer("s", f"!bufferdelay [time], !buffermax [time], !entertain [0-1], !settings", ctx.author, "helpm")

    @commands.command(name='bufferdelay')
    async def bufedelay(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            timeout = str.replace(ctx.message.content, '!bufferdelay ', '')
            timeout = re.sub("\n", '', timeout)
            timeout = str.replace(timeout, ",", ".")
            try:
                with open('data/settings.txt', 'r', encoding='utf-8') as b:
                    data = json.loads(b.read())
            except:
                data = {}
            with open('data/settings.txt', 'w', encoding='utf-8') as b:
                try:
                    data["bufferdelay"] = float(timeout)
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} delay: {data['bufferdelay']},"
                                                    f" max: {data['buffermax']}",
                                                    ctx.author, "bufferdelay")
                except:
                    AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author, "bufferdelay")

    @commands.command(name='buffermax')
    async def bufermax(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            timeout = str.replace(ctx.message.content, '!buffermax ', '')
            timeout = re.sub("\n", '', timeout)
            timeout = str.replace(timeout, ",", ".")
            try:
                with open('data/settings.txt', 'r', encoding='utf-8') as b:
                    data = json.loads(b.read())
            except:
                data = {}
            with open('data/settings.txt', 'w', encoding='utf-8') as b:
                try:
                    data["buffermax"] = int(timeout)
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} max: {data['buffermax']}, delay: {data['bufferdelay']}",
                                                    ctx.author, "buffermax")
                except:
                    AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author, "buffermax")

    @commands.command(name='entertain')
    async def usetime(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            timeout = str.replace(ctx.message.content, '!entertain ', '')
            timeout = re.sub("\n", '', timeout)
            try:
                with open('data/settings.txt', 'r', encoding='utf-8') as b:
                    data = json.loads(b.read())
            except:
                data = {}
            with open('data/settings.txt', 'w', encoding='utf-8') as b:
                if timeout == "0":
                    data["entertain"] = False
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} бот игнорирует развлекательные команды",
                                                    ctx.author, "entertain")
                elif timeout == "1":
                    data["entertain"] = True
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} бот принимает развлекательные команды",
                                                    ctx.author, "entertain")
                else:
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} !entertain [0,1]",
                                                    ctx.author, "entertain")

    @commands.command(name='settings')
    async def settings(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            try:
                with open('data/settings.txt', 'r', encoding='utf-8') as b:
                    data = json.loads(b.read())
            except:
                data = {}
            if len(data) == 0:
                AdditionalMethods.add_to_buffer("s", f"Настройки пустые", ctx.author, "settings")
            else:
                AdditionalMethods.add_to_buffer("s", f"max: {data['buffermax']}, delay: {data['bufferdelay']}, entertain: {data['entertain']}", ctx.author, "settings")

    @commands.command(name='temp')
    async def temp(self, ctx):
        nickname = ctx.author.name
        tempp = random.uniform(25, 45)
        temp = round(tempp, 1)
        if 35.7 <= temp <= 37:
            AdditionalMethods.add_to_buffer("e",
                                            f"{nickname}, ваша температура {str(temp)} °C! У вас температура в норме ThumbUp",
                                            ctx.author, "temp")
        else:
            if 37 < temp < 40 or 35.7 > temp >= 32:
                AdditionalMethods.add_to_buffer("e", f"{nickname}, ваша температура {str(temp)} °C! У вас вирус? PepeS",
                                                ctx.author, "temp")
            else:
                if temp > 40 or temp < 32:
                    AdditionalMethods.add_to_buffer("e",
                                                    f"{nickname}, ваша температура {str(temp)} °C! Вызывайте дурку! Durka",
                                                    ctx.author, "temp")

    @commands.command(name='me')
    async def me(self, ctx):
        nickname = ctx.author.name
        with open('data/me.txt', 'r', encoding='utf-8') as b:
            listme = list(b)
            randomm = random.choice(listme)
            randomm = re.sub("\n", '', randomm)
            print("каво")
            AdditionalMethods.add_to_buffer("e", randomm.format(nickname), ctx.author, "me")

    @commands.command(name='do')
    async def do(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        if message == "!do":
            AdditionalMethods.add_to_buffer("c", f"{nickname}, введите !do [message]", ctx.author, "do")
        else:
            do = str.replace(message, '!do ', '')
            do = re.sub("\n", '', do)
            with open('data/do.txt', 'r', encoding='utf-8') as c:
                listme = list(c)
                randomdo = random.choice(listme)
                randomdo = re.sub("\n", '', randomdo)
                result = randomdo.format(nickname, do)
                if not AdditionalMethods.check_on_toomuchbool(result):
                    AdditionalMethods.add_to_buffer("e", randomdo.format(nickname, do), ctx.author, "do")
                else:
                    AdditionalMethods.add_to_buffer("e", f"{nickname}, пишите меньше символов WeirdChamp ", ctx.author, "do")

    @commands.command(name='бубу')
    async def bubu(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        if message == "!бубу":
            AdditionalMethods.add_to_buffer("e", f"{nickname}, введите !бубу [something]", ctx.author, "")
        else:
            bubu = str.replace(message, '!бубу ', '')
            bubu = re.sub("\n", '', bubu)
            if len(bubu) < 235:
                AdditionalMethods.add_to_buffer("e", f"Ну {str(bubu)} и {str(bubu)} Чё бубнить-то? ThumbUp", ctx.author, "бубу")
            else:
                AdditionalMethods.add_to_buffer("e", "Слишком длинное бубу WeirdChamp ", ctx.author, "бубу")

    @commands.command(name='steal')
    async def steal(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        if message == "!steal":
            AdditionalMethods.add_to_buffer("e", f"{nickname}, введите !steal [nickname]", ctx.author, "steal")
        else:
            procent = random.randrange(0, 100, 1)
            ruble = random.randrange(0, 2000, 1)
            steal = str.replace(message, '!steal ', '')
            steal = re.sub("\n", '', steal)
            if procent >= 33:
                if not AdditionalMethods.check_on_toomuchbool(f"{nickname} украл у {str(steal)} {str(ruble)} руб. BOP"):
                    AdditionalMethods.add_to_buffer("e", f"{nickname} украл у {str(steal)} {str(ruble)} руб. BOP",
                                                    ctx.author, "steal")
                else:
                    AdditionalMethods.add_to_buffer("e", f"{nickname} пишите меньше символов WeirdChamp",
                                                    ctx.author, "steal")
            else:
                if not AdditionalMethods.check_on_toomuchbool(f"{nickname} ничего не украл у {str(steal)} KeK Lohich"):
                    AdditionalMethods.add_to_buffer("e", f"{nickname} ничего не украл у {str(steal)} KeK Lohich",
                                                ctx.author, "steal")
                else:
                    AdditionalMethods.add_to_buffer("e", f"{nickname}, пишите меньше символов WeirdChamp",
                                                ctx.author, "steal")

    @commands.command(name='try')
    async def ttry(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        result = AdditionalMethods.parse_standartfile_message(nickname, "{nickname} попробовал {messagestr}... {filestr}",
                                                                                          message, "!try", "try")
        if not AdditionalMethods.check_on_toomuchbool(result):
            AdditionalMethods.add_to_buffer("e", result, ctx.author, "try")
        else:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, пишите меньше символов WeirdChamp",
                                            ctx.author, "try")

    @commands.command(name='время')
    async def time(self, ctx):
        AdditionalMethods.add_to_buffer("c", datetime.strftime(datetime.now() + timedelta(hours=3),
                                                               "Чичас %H:%M по МСК Waiting"), ctx.author, "время")

    @commands.command(name='обнять')
    async def hug(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        result = AdditionalMethods.parse_standartfile_message(nickname, "{nickname} {filestr} обнимает {messagestr} "
                                                                                          "VoHiYo",
                                                                                          message, "!обнять", "hug")
        if not AdditionalMethods.check_on_toomuchbool(result):
            AdditionalMethods.add_to_buffer("e", result, ctx.author, "обнять")
        else:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, пишите меньше символов WeirdChamp", ctx.author, "обнять")

    @commands.command(name='кнб')
    async def cnb(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        listcnb = ['⛰', '✂️', '📜']
        usercnb = str.replace(message, '!кнб ', '')
        rndcnb1 = random.choice(listcnb)
        if message == '!кнб':
            AdditionalMethods.add_to_buffer("e", f"{nickname}, введите !кнб [камень, ножницы, бумага]", ctx.author, "кнб")
        else:
            if usercnb == 'камень' and rndcnb1 == '⛰':
                AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) ⛰ , а Бот поставил ⛰ . Ничья! ThumbUp",
                                                ctx.author, "кнб")
            if usercnb == 'ножницы' and rndcnb1 == '✂️':
                AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) ✂️ , а Бот поставил ✂️ . Ничья! ThumbUp",
                                                ctx.author, "кнб")
            if usercnb == 'бумага' and rndcnb1 == '📜':
                AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) 📜 , а Бот поставил 📜 . Ничья! ThumbUp",
                                                ctx.author, "кнб")
            if usercnb == 'бумага' and rndcnb1 == '⛰':
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname} поставил(а) 📜 , а Бот поставил ⛰ . Победа {nickname} EZ Clap",
                                                ctx.author, "кнб")
            if usercnb == 'камень' and rndcnb1 == '📜':
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname} поставил(а) ⛰ , а Бот поставил 📜 . Победа Бота Lohich",
                                                ctx.author, "кнб")
            if usercnb == 'камень' and rndcnb1 == '✂️':
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname} поставил(а) ⛰ , а Бот поставил ✂️ . Победа {nickname} EZ Clap",
                                                ctx.author, "кнб")
            if usercnb == 'ножницы' and rndcnb1 == '⛰':
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname} поставил(а) ✂️ , а Бот поставил ⛰ . Победа Бота Lohich",
                                                ctx.author, "")
            if usercnb == 'ножницы' and rndcnb1 == '📜':
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname} поставил(а) ✂️ , а Бот поставил 📜 . Победа {nickname} EZ Clap",
                                                ctx.author, "кнб")
            if usercnb == 'бумага' and rndcnb1 == '✂️':
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname} поставил(а) 📜 , а Бот поставил ✂️ . Победа Бота Lohich",
                                                ctx.author, "кнб")

    @commands.command(name='когда')
    async def kogda(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        result = AdditionalMethods.parse_standartfile_message(nickname, "{nickname}, когда {messagestr}? Hmmm {filestr}", message, "!когда", "kogda")
        if not AdditionalMethods.check_on_toomuchbool(result):
            AdditionalMethods.add_to_buffer("e", result, ctx.author, "когда")
        else:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, пишите меньше символов WeirdChamp", ctx.author, "когда")

    @commands.command(name='привет')
    async def privet(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        result = AdditionalMethods.parse_standartfile_message(nickname,
                                                                                          "{nickname} {filestr} приветствует {messagestr} "
                                                                                          "peepoHey peepoLove",
                                                                                          message, "!привет", "privet")
        if not AdditionalMethods.check_on_toomuchbool(result):
            AdditionalMethods.add_to_buffer("e", result, ctx.author, "привет")
        else:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, пишите меньше символов WeirdChamp", ctx.author, "привет")

    @commands.command(name='гороскоп')
    async def goroskop(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        goroskop = AdditionalMethods.get_goroskop(message, nickname)
        AdditionalMethods.add_to_buffer("e", goroskop, ctx.author, "гороскоп")


subprocess.Popen([sys.executable, 'ChatBot.py'])
subprocess.Popen([sys.executable, 'BufferCleaner.py'])
subprocess.Popen([sys.executable, 'CheckingStreamThread.py'])
bot = CommandsBot()
bot.run()
