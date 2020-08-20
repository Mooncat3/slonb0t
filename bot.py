import sys
from abc import ABC
from twitchioc.ext import commands
import asyncio
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

    @commands.command(name='case')
    async def case(self, ctx):
        nickname = ctx.author.name
        randstr = random.randint(1, 179)
        r = requests.get('https://market.csgo.com/?s=name&r=&q=&p=' + str(randstr) + '&h=&fst=0')
        soup = BeautifulSoup(r.content, 'html.parser')
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
                                        ctx.author)

        """""
    @commands.command(name='history')
    async def stream(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        message = str.replace(message, '!history', '')
        AdditionalMethods.add_to_buffer("e", AdditionalMethods.get_last_stream_stat(message[1:len(message)], nickname), ctx.author)

    @commands.command(name='archive')
    async def streamh(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        message = str.replace(message, '!archive', '')
        #try:
        id=int(message[1:2])
        if len(message[2:len(message)]) > 1:
            tag = str.replace(message, f' {id} ', '')
        else:
            tag = ''
        AdditionalMethods.add_to_buffer("c", AdditionalMethods.get_archive_stream_stat(id, nickname, tag).format(nickname, id), ctx.author)
        #except:
           # AdditionalMethods.add_to_buffer("с", f'{nickname} !archive [0-9]', ctx.author)
           
        """""

    @commands.command(name='рецепт')
    async def recept(self, ctx):
        r = requests.get('http://culinar.ivest.kz/randomMenu')
        soup = BeautifulSoup(r.content, 'html.parser')
        name = soup.find('a', class_='rec_name').get_text()
        recept = soup.find('div', class_='randome_recept_right').get_text()
        receptt = 'Способ приготовления:'.join(recept.split('Способ приготовления:')[:-1])
        recept1 = recept[recept.find("Способ приготовления:") + 1:]
        recept1 = (recept1[:495] + '...') if len(recept1) > 495 else recept1
        AdditionalMethods.add_to_buffer("r", f"{name} - {receptt}", ctx.author)
        AdditionalMethods.add_to_buffer("r", f"С{recept1}", ctx.author)

    @commands.command(name='анекдот')
    async def anekdot(self, ctx):
        r = requests.get('http://anecdotica.ru/')
        soup = BeautifulSoup(r.content, 'html.parser')
        anekdot = soup.find('div', class_='item_text').get_text()
        anekdott = (anekdot[:493] + '...') if len(anekdot) > 493 else anekdot
        AdditionalMethods.add_to_buffer("e", '{} KeK'.format(str.replace(anekdott, "\r\n", " ")), ctx.author)

    @commands.command(name='курс')
    async def kurs(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        r = requests.get('https://fortrader.org/quotes/usdrur')
        r1 = requests.get('https://fortrader.org/quotes/eurrur')
        r2 = requests.get('https://fortrader.org/currencyrates/jpy')
        soup = BeautifulSoup(r.content, 'html.parser')
        soup1 = BeautifulSoup(r1.content, 'html.parser')
        soup2 = BeautifulSoup(r2.content, 'html.parser')
        dollar = soup.find('p', class_='rates_box1_inner pid-USDRUR-bid').get_text()
        euro = soup1.find('p', class_='rates_box1_inner pid-EURRUR-bid').get_text()
        jpy = soup2.find('input', class_='converter_form_inp converterInpTo').get(key="value")
        now = datetime.now() + timedelta(hours=3)
        today = now.strftime("%d.%m")

        if message == "!курс":
            AdditionalMethods.add_to_buffer("c",
                                            f"Курс валют на {today}: USD = {dollar} RUB | EURO = {euro} RUB | JPY = {jpy} RUB",
                                            ctx.author)
        else:
            try:
                if message.find('!курс доллар-рубль') != -1:
                    kurs = str.replace(message, '!курс доллар-рубль ', '')
                    result = float(kurs) * float(dollar)
                    result = round(result, 2)
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, {kurs} USD = {result} RUB", ctx.author)
                elif message.find('!курс рубль-доллар') != -1:
                    kurs = str.replace(message, '!курс рубль-доллар ', '')
                    result = float(kurs) / float(dollar)
                    result = round(result, 2)
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, {kurs} RUB = {result} USD", ctx.author)
                elif message.find('!курс евро-рубль') != -1:
                    kurs = str.replace(message, '!курс евро-рубль ', '')
                    result = float(kurs) * float(euro)
                    result = round(result, 2)
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, {kurs} EUR = {result} RUB", ctx.author)
                elif message.find('!курс рубль-евро') != -1:
                    kurs = str.replace(message, '!курс рубль-евро ', '')
                    result = float(kurs) / float(euro)
                    result = round(result, 2)
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, {kurs} RUB = {result} EUR", ctx.author)
                elif message.find('!курс йена-рубль') != -1:
                    kurs = str.replace(message, '!курс йена-рубль ', '')
                    result = float(kurs) * float(jpy)
                    result = round(result, 2)
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, {kurs} JPY = {result} RUB", ctx.author)
                elif message.find('!курс рубль-йена') != -1:
                    kurs = str.replace(message, '!курс рубль-йена ', '')
                    result = float(kurs) / float(jpy)
                    result = round(result, 2)
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, {kurs} RUB = {result} JPY", ctx.author)
                else:
                    AdditionalMethods.add_to_buffer("c",
                                                    f"{nickname}, неккоректно написаны валюты, пишите в именительном падеже (рубль-доллар и т.д.)",
                                                    ctx.author)
            except OverflowError:
                AdditionalMethods.add_to_buffer("с", f"{nickname} Число слишком большое WeirdChamp", ctx.author)
            except ValueError:
                AdditionalMethods.add_to_buffer("с", f"{nickname} Это не число WeirdChamp", ctx.author)

    @commands.command(name='topclipever')
    async def topclipever(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipever ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipever":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(0, top, nickname), ctx.author)

    @commands.command(name='topclipyear')
    async def topclipyear(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipyear ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipyear":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(365, top, nickname), ctx.author)

    @commands.command(name='topclipmonth')
    async def topclipmonth(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipmonth ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipmonth":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(30, top, nickname), ctx.author)

    @commands.command(name='topclipday')
    async def topclipday(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!topclipday ', '')
        top = re.sub("\n", '', top)
        if top == "!topclipday":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(1, top, nickname), ctx.author)

    @commands.command(name='iq')
    async def iq(self, ctx):
        nickname = ctx.author.name
        iq = random.randrange(55, 180, 1)
        if iq == 110:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, ваш IQ = {str(iq)}! Вы Хесус?! PogU", ctx.author)
        if iq == 89:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, ваш IQ = {str(iq)}! Вы Братишкин?! PogU", ctx.author)
        else:
            if 110 > iq > 70:
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname}, ваш IQ = {str(iq)}! Надо же, у стримера больше IQ чем у вас KeK",
                                                ctx.author)
            if 110 < iq < 135:
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname}, ваш IQ = {str(iq)}! Ого, а вы не глупый человек ThumbUp",
                                                ctx.author)
            if iq < 70:
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname}, ваш IQ = {str(iq)}! Чел... сходи книгу почитай WeirdChamp",
                                                ctx.author)
            if iq >= 135:
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname}, ваш IQ = {str(iq)}! Внимание! В чате гений WAYTOOSMART Clap",
                                                ctx.author)

    @commands.command(name='паста')
    async def pasta(self, ctx):
        AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_simplefile_message("{}", "nadya"), ctx.author)

    @commands.command(name='help')
    async def help(self, ctx):
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("c", f"Ку, {nickname}, меня зовут SLONB0T catJAM , список всех моих команд: https://pastebin.com/raw/hZ4GGw4z catJAM", ctx.author)

    @commands.command(name='helpm')
    async def helpm(self, ctx):
        nickname = ctx.author.name
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            AdditionalMethods.add_to_buffer("s", f"{nickname}, страница 4 (управление ботом, доступно модераторам и узкому кругу лиц): !bufferdelay [time], !buffermax [time], !chkstreamactive [time]", ctx.author)

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
                                                    f"{nickname} теперь задержка между сообщениями будет составлять {data['bufferdelay']}",
                                                    ctx.author)
                except:
                    AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author)

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
                                                    f"{nickname} теперь, если в очереди на вывод будет {data['buffermax']} сообщений, бот будет писать в лс",
                                                    ctx.author)
                except:
                    AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author)

    @commands.command(name='chkstreamactive')
    async def usetime(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            timeout = str.replace(ctx.message.content, '!chkstreamactive ', '')
            timeout = re.sub("\n", '', timeout)
            try:
                with open('data/settings.txt', 'r', encoding='utf-8') as b:
                    data = json.loads(b.read())
            except:
                data = {}
            with open('data/settings.txt', 'w', encoding='utf-8') as b:
                if timeout == "0":
                    data["checkStreamActive"] = False
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} бот теперь не будет игнорировать развлекательные команды от не вип-пользователей во время стрима",
                                                    ctx.author)
                elif timeout == "1":
                    data["checkStreamActive"] = True
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} бот теперь будет игнорировать развлекательные команды от не вип-пользователей во время стрима",
                                                    ctx.author)
                else:
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} !chkstreamactive [0,1]",
                                                    ctx.author)

    @commands.command(name='temp')
    async def temp(self, ctx):
        nickname = ctx.author.name
        tempp = random.uniform(25, 45)
        temp = round(tempp, 1)
        if 35.7 <= temp <= 37:
            AdditionalMethods.add_to_buffer("e",
                                            f"{nickname}, ваша температура {str(temp)} °C! У вас температура в норме ThumbUp",
                                            ctx.author)
        else:
            if 37 < temp < 40 or 35.7 > temp >= 32:
                AdditionalMethods.add_to_buffer("e", f"{nickname}, ваша температура {str(temp)} °C! У вас вирус? PepeS",
                                                ctx.author)
            else:
                if temp > 40 or temp < 32:
                    AdditionalMethods.add_to_buffer("e",
                                                    f"{nickname}, ваша температура {str(temp)} °C! Вызывайте дурку! Durka",
                                                    ctx.author)

    @commands.command(name='me')
    async def me(self, ctx):
        nickname = ctx.author.name
        with open('data/me.txt', 'r', encoding='utf-8') as b:
            listme = list(b)
            randomm = random.choice(listme)
            randomm = re.sub("\n", '', randomm)
            AdditionalMethods.add_to_buffer("e", randomm.format(nickname), ctx.author)

    @commands.command(name='do')
    async def do(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        if message == "!do":
            AdditionalMethods.add_to_buffer("c", f"{nickname}, введите !do [message]", ctx.author)
        else:
            do = str.replace(message, '!do ', '')
            do = re.sub("\n", '', do)
            with open('data/do.txt', 'r', encoding='utf-8') as c:
                listme = list(c)
                randomdo = random.choice(listme)
                randomdo = re.sub("\n", '', randomdo)
                AdditionalMethods.add_to_buffer("e", randomdo.format(nickname, do), ctx.author)

    @commands.command(name='бубу')
    async def bubu(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        if message == "!бубу":
            AdditionalMethods.add_to_buffer("c", f"{nickname}, введите !бубу [something]", ctx.author)
        else:
            bubu = str.replace(message, '!бубу ', '')
            bubu = re.sub("\n", '', bubu)
            if len(bubu) < 235:
                AdditionalMethods.add_to_buffer("e", f"Ну {str(bubu)} и {str(bubu)} Чё бубнить-то? ThumbUp", ctx.author)
            else:
                AdditionalMethods.add_to_buffer("e", "Слишком длинное бубу WeirdChamp ", ctx.author)

    @commands.command(name='steal')
    async def steal(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        if message == "!steal":
            AdditionalMethods.add_to_buffer("c", f"{nickname}, введите !steal [nickname]", ctx.author)
        else:
            procent = random.randrange(0, 100, 1)
            ruble = random.randrange(0, 2000, 1)
            steal = str.replace(message, '!steal ', '')
            steal = re.sub("\n", '', steal)
            if procent >= 33:
                AdditionalMethods.add_to_buffer("e", f"{nickname} украл у {str(steal)} {str(ruble)} руб. BOP",
                                                ctx.author)
            else:
                AdditionalMethods.add_to_buffer("e", f"{nickname} ничего не украл у {str(steal)} KeK Lohich",
                                                ctx.author)

    @commands.command(name='try')
    async def ttry(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_standartfile_message(nickname,
                                                                                          "{nickname} попробовал {messagestr}... {filestr}",
                                                                                          message, "!try", "try"),
                                        ctx.author)

    @commands.command(name='время')
    async def time(self, ctx):
        AdditionalMethods.add_to_buffer("c", datetime.strftime(datetime.now() + timedelta(hours=3),
                                                               "Чичас %H:%M по МСК Waiting"), ctx.author)

    @commands.command(name='обнять')
    async def hug(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_standartfile_message(nickname,
                                                                                          "{nickname} {filestr} обнимает {messagestr} "
                                                                                          "VoHiYo",
                                                                                          message, "!обнять", "hug"), ctx.author)

    @commands.command(name='кнб')
    async def cnb(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        listcnb = ['⛰', '✂️', '📜']
        usercnb = str.replace(message, '!кнб ', '')
        rndcnb1 = random.choice(listcnb)
        if message == '!кнб':
            AdditionalMethods.add_to_buffer("c", f"{nickname}, введите !кнб [камень, ножницы, бумага]", ctx.author)
        else:
            if usercnb == 'камень' and rndcnb1 == '⛰':
                AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) ⛰ , а Бот поставил ⛰ . Ничья! ThumbUp",
                                                ctx.author)
            if usercnb == 'ножницы' and rndcnb1 == '✂️':
                AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) ✂️ , а Бот поставил ✂️ . Ничья! ThumbUp",
                                                ctx.author)
            if usercnb == 'бумага' and rndcnb1 == '📜':
                AdditionalMethods.add_to_buffer("e", f"{nickname} поставил(а) 📜 , а Бот поставил 📜 . Ничья! ThumbUp",
                                                ctx.author)
            if usercnb == 'бумага' and rndcnb1 == '⛰':
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname} поставил(а) 📜 , а Бот поставил ⛰ . Победа {nickname} EZ Clap",
                                                ctx.author)
            if usercnb == 'камень' and rndcnb1 == '📜':
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname} поставил(а) ⛰ , а Бот поставил 📜 . Победа Бота Lohich",
                                                ctx.author)
            if usercnb == 'камень' and rndcnb1 == '✂️':
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname} поставил(а) ⛰ , а Бот поставил ✂️ . Победа {nickname} EZ Clap",
                                                ctx.author)
            if usercnb == 'ножницы' and rndcnb1 == '⛰':
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname} поставил(а) ✂️ , а Бот поставил ⛰ . Победа Бота Lohich",
                                                ctx.author)
            if usercnb == 'ножницы' and rndcnb1 == '📜':
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname} поставил(а) ✂️ , а Бот поставил 📜 . Победа {nickname} EZ Clap",
                                                ctx.author)
            if usercnb == 'бумага' and rndcnb1 == '✂️':
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname} поставил(а) 📜 , а Бот поставил ✂️ . Победа Бота Lohich",
                                                ctx.author)
                
    @commands.command(name='когда')
    async def kogda(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_standartfile_message(nickname,
                                                                                          "{nickname}, {messagestr} {filestr}",
                                                                                          message, "!когда", "kogda"),
                                        ctx.author)

    @commands.command(name='привет')
    async def privet(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_standartfile_message(nickname,
                                                                                          "{nickname} передаёт {filestr} привет {messagestr} "
                                                                                          "peepoHey peepoLove",
                                                                                          message, "!привет", "privet"), ctx.author)

    @commands.command(name='заебало')
    async def zaebalo(self, ctx):
        randpage = random.randrange(1, 1689, 1)
        r = requests.get("https://zaebalo.ru/?page=" + str(randpage))
        soup = BeautifulSoup(r.content, 'html.parser')
        d = soup.find_all('div', align='left')
        p = str(random.choice(d)).replace("</div>", "").replace("<br/>", "").replace("</p>", "").replace("<p>",
                                                                                                         "").replace(
            '<div align="left">', '').replace("<br>", "").replace("</br>", "").replace("\r     ", "")
        with open('data/osujdau.txt', 'r', encoding='utf-8') as c:
            List = list(c)
            for s in List:
                ban = ""
                s = s.replace("\n", "")
                for i in range(0, len(s)):
                    ban += "*"
                if p.find(s) != -1:
                    print(s)
                p = str.replace(p.lower(), s, ban)
        AdditionalMethods.add_to_buffer("e", AdditionalMethods.check_on_toomuchsimbols(p), ctx.author)

    @commands.command(name='гороскоп')
    async def goroskop(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        goroskop = AdditionalMethods.get_goroskop(message, nickname)
        AdditionalMethods.add_to_buffer("e", goroskop, ctx.author)


# subprocess.Popen([sys.executable, 'ChatBot.py'])
subprocess.Popen([sys.executable, 'BufferCleaner.py'])
subprocess.Popen([sys.executable, 'CheckingStreamThread.py'])
bot = CommandsBot()
bot.run()
