import sys
from abc import ABC
from github import Github
from twitchioc.ext import commands
from datetime import timedelta, datetime
from bs4 import BeautifulSoup
import requests
import AdditionalMethods
import Settings
import re
import random
import subprocess
import config
import json
from urllib.parse import quote
import asyncio
import time
import wikipedia

class CommandsBot(commands.Bot, ABC):

    def __init__(self):
        super().__init__(irc_token=f'oauth:{config.OAUTH}',
                         client_id=config.CLIENT_ID, nick=config.BOT, prefix='!',
                         initial_channels=config.CHANNELS)
        self.roulette_is_running = False
        self.roulette_nicknames = []
        self.duel_is_running = False
        self.duel_nicknames = []
        self.duel_user = ""
        self.duel_serious = True
        self.spammers = {}
        self.seekers = []
        self.logs = []
        self.japtest = {'kanji': '', 'tr': '', 'example': '', 'tr_example': '', 'active': False}
        
    async def event_command_error(self, ctx, error):
        pass
        
    async def duelent(self, socket):
        i: int = 0
        while len(self.duel_nicknames) == 1 and i < 200:
            i += 1
            await asyncio.sleep(0.1)
        if len(self.duel_nicknames) == 1:
            await socket.send_privmsg(config.CHAN, "Оппонент не принял дуэль MonkaHmm")
        else:
            if self.duel_serious:
                await socket.send_privmsg(config.CHAN, "Дуэлянты смотрят друг на друга monkaW . В любой момент они готовы достать револьвер из кобуры... PepeS ")
                randname = random.choice(self.duel_nicknames)
                self.duel_nicknames.remove(randname)
                await asyncio.sleep(8)
                with open(file='data/duel_rand.txt', mode='r', encoding='utf-8') as e:
                    data = json.loads(e.read())
                    randseq = random.choice(data)
                await socket.send_privmsg(config.CHAN, f"Хлопок! {self.duel_nicknames[0]} выстреливает в {randname}{randseq['text']}")
                if int(randseq['time']) > 1:
                    await socket.send_privmsg(config.CHAN, f"/timeout {randname} {randseq['time']}")
                elif int(randseq['time']) > 0:
                    await socket.send_privmsg(config.CHAN, f"/timeout {self.duel_nicknames[0]} 60")
            else:
                await socket.send_privmsg(config.CHAN,
                                          "Один из дуэлянтов бессмертен, поэтому они стреляют холостыми пулями monkaW . В любой момент они готовы достать револьвер из кобуры... PepeS")
                randname = random.choice(self.duel_nicknames)
                self.duel_nicknames.remove(randname)
                await asyncio.sleep(8)
                await socket.send_privmsg(config.CHAN,
                                          f"Хлопок! Точный выстрел заставляет {randname} сдаться. Самая быстрая рука дикого запада – {self.duel_nicknames[0]} EZ")
        self.duel_nicknames.clear()
        self.duel_is_running = False
    
    async def rand(self, socket):
        await asyncio.sleep(20)
        if len(self.roulette_nicknames) == 1:
            await socket.send_privmsg(config.CHAN, "Никто не участвует, ну и ладно PogO")
        else:
            await socket.send_privmsg(config.CHAN, "Кто же умрёт? Hmmm ...")
            randname = random.choice(self.roulette_nicknames)
            await asyncio.sleep(5)
            await socket.send_privmsg(config.CHAN, "А умирает сегодня " + randname + ", ББ!")
            await socket.send_privmsg(config.CHAN, f"/timeout {randname} 60")
        self.roulette_nicknames.clear()
        self.roulette_is_running = False

    async def event_ready(self):
        print(f'Ready {str(self.__class__.__name__)} | {self.nick} on {self.initial_channels}')
        global namess
        namess = []
        global ii
        ii = 0

    async def event_message(self, message):
        nickname = message.author.name
        global ii
        global namess
        namess.append(nickname)
        if ii < 100:
            ii+=1
        else:
            del namess[0]    
        if not AdditionalMethods.vip(message.author.is_mod, nickname) and not nickname == "slonb0t":
            docheck = True
            mod = Settings.get_mod()
            if mod != "all" and (mod == "skip" or mod == "skip_with"):
                with open(file='data/SMILES.txt', mode='r', encoding='utf-8') as e:
                    smiles = json.loads(e.read())
                if mod == "skip":
                    docheck = False
                    arraymess = str.split(message.content, " ")
                    for r in arraymess:
                        if not r in smiles:
                            docheck = True
                elif mod == "skip_with":
                    docheck = True
                    arraymess = str.split(message.content, " ")
                    for r in arraymess:
                        if r in smiles:
                            docheck = False
            if docheck:
                if nickname in self.spammers.keys():
                    self.spammers[nickname]["messes"] += 1
                    if self.spammers[nickname]["messes"] == 1:
                        self.spammers[nickname]["time"] = time.time()
                    self.spammers[nickname]["log"].append(
                        {"timenow": datetime.now().strftime("%H:%M:%S"), "messtime": round(time.time() - self.spammers[nickname]["time"], 2), "messes": self.spammers[nickname]['messes'], "content": message.content})
                else:
                    self.spammers[nickname] = {}
                    self.spammers[nickname]["time"] = time.time()
                    self.spammers[nickname]["messes"] = 1
                    self.spammers[nickname]["worned"] = 0
                    self.spammers[nickname]["log"] = [{"timenow": datetime.strftime(datetime.utcnow() + timedelta(hours=3), "%H:%M:%S"), "messtime": round(time.time() - self.spammers[nickname]["time"], 2), "messes": self.spammers[nickname]['messes'], "content": message.content}]

                if self.spammers[nickname]["messes"] > 1:
                    if time.time() - self.spammers[nickname]["time"] < Settings.get_norm() and self.spammers[nickname]["messes"] == Settings.get_max_messes():
                        self.spammers[nickname]["time"] = time.time()
                        self.spammers[nickname]["messes"] = 0
                        stringer = "|--------------------------------------------------|<br>"
                        stringer += nickname + ":<br>"
                        for r in self.spammers[nickname]["log"]:
                            stringer += f"{r['timenow']}: {r['content']} || time: {r['messtime']} || messes: {r['messes']}<br>"
                        if self.spammers[nickname]["worned"] == Settings.get_attentions():
                            self.spammers[nickname]["worned"] = 0
                            stringer += f"отлетел на {Settings.get_timeout()} с настройками: |norm: {Settings.get_norm()}, maxmesses: {Settings.get_max_messes()}, emojimode: {Settings.get_mod()}|"
                            for f in self.seekers:
                                await self._ws.send_privmsg(config.CHAN, f"/w {f} {nickname} отлетел на {Settings.get_timeout()}")
                            await self._ws.send_privmsg(config.CHAN,  f"/timeout {nickname} {Settings.get_timeout()} спам, automated by SLONB0T")
                            await self._ws.send_privmsg(config.CHAN,
                                                        f"/w {nickname} Вы получили слишком много предупреждений и временно отстраняетесь от чата MrDestructoid")
                        else:
                            self.spammers[nickname]["worned"] += 1
                            stringer += f"был предупреждён {self.spammers[nickname]['worned']} из {Settings.get_attentions()} раз с настройками: |norm: {Settings.get_norm()}, maxmesses: {Settings.get_max_messes()}, emojimode: {Settings.get_mod()}|"
                            for f in self.seekers:
                                await self._ws.send_privmsg(config.CHAN,
                                                      f"/w {f} {nickname} был предупреждён {self.spammers[nickname]['worned']} из {Settings.get_attentions()} раз")
                            await self._ws.send_privmsg(config.CHAN,
                                                        f"/w {nickname} вы слишком часто отправляете сообщения на канале jesusavgn, это {self.spammers[nickname]['worned']} из {Settings.get_attentions()} предупреждений MrDestructoid")
                        requests.post(config.api_url + "/logs/jesusavgn",
                                               data={"log": stringer.encode(
                                                   "utf-8"), "nickname": nickname, "warns": {self.spammers[nickname]['worned']}, "time": time.time()}, headers={"Authorization": "y5IArL6S&%%G(69G"})
                        self.spammers[nickname]["log"].clear()
                    elif time.time() - self.spammers[nickname]["time"] >= Settings.get_norm():
                        self.spammers[nickname]["time"] = time.time()
                        self.spammers[nickname]["log"].clear()
                        self.spammers[nickname]["messes"] = 0
        await self.handle_commands(message)

    @commands.command(name='seek')
    async def seek(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            if not nickname in self.seekers:
                self.seekers.append(nickname)
                AdditionalMethods.add_to_buffer("s",
                                                f"Вы подписаны на уведомления о спаме!",
                                                ctx.author,
                                                "seek")
            else:
                AdditionalMethods.add_to_buffer("s",
                                                f"Вы уже подписаны на уведомления о спаме ResidentSleeper",
                                                ctx.author,
                                                "seek")

    @commands.command(name='unseek')
    async def unseek(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            if not nickname in self.seekers:
                AdditionalMethods.add_to_buffer("s",
                                                f"Вы не подписаны на уведомления о спаме ResidentSleeper",
                                                ctx.author,
                                                "unseek")
            else:
                self.seekers.remove(nickname)
                AdditionalMethods.add_to_buffer("s",
                                                f"Вы отписаны от уведомлений о спаме!",
                                                ctx.author,
                                                "unseek")

    @commands.command(name='helpm')
    async def helpm(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            AdditionalMethods.add_to_buffer("s", f"!bufferdelay [time], !buffermax [time], !entertain [0-1], !settings, !norm [time], !maxmesses [int], !attentions [int], !emojimode [mod], !timeout []",
                                            ctx.author, "helpm")
    @commands.command(name='acduel')
    async def acduel(self, ctx):
        if self.duel_is_running:
            #print(self.duel_user)
            if ctx.author.name == self.duel_user:
                if self.duel_serious:
                    if ctx.author.is_mod:
                        self.duel_serious = False
                    else:
                        self.duel_serious = True
                self.duel_nicknames.append(ctx.author.name)

    @commands.command(name='duel')
    async def duel(self, ctx):
        nickname = ctx.author.name
        if not self.duel_is_running and (not AdditionalMethods.check_active() or AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name)) and not self.roulette_is_running:
            if ctx.author.is_mod:
                self.duel_serious = False
            else:
                self.duel_serious = True
            message = ctx.message.content
            message = str.replace(message, '!duel', '')
            message = message[1:len(message)]
            if len(message) > 1 and len(message) <= 26 and message.find(" ") == -1:
                self.duel_is_running = True
                self.duel_nicknames.append(ctx.author.name)
                self.duel_user = message.replace("@", "").lower()
                if nickname != self.duel_user:
                    await ctx.channel._ws.send_privmsg(config.CHAN,
                                                   f"{nickname} кидает перчатку в {message}, вызывая его на дуэль peepoCool . Чтобы принять вызов – напишите !acduel.")
                else:
                    await ctx.channel._ws.send_privmsg(config.CHAN,
                                                       f"{nickname} направил ствол на ... самого себя blushW . Если вы уверены в своём выборе, напишите !acduel.")
                asyncio.get_event_loop().create_task(self.duelent(self._ws))
            else:
                await ctx.channel._ws.send_privmsg(config.CHAN,
                                                   f"{nickname}, напишите никнейм правильно PepoG")
        elif self.duel_is_running:
            AdditionalMethods.add_to_buffer("s", f"{nickname}, сейчас идёт общая рулетка", ctx.author, "duel")

    @commands.command(name='accept')
    async def accept(self, ctx):
        if self.roulette_is_running:
            if not ctx.author.name in self.roulette_nicknames:
                self.roulette_nicknames.append(ctx.author.name)

    @commands.command(name='omgroulette')
    async def omgroulette(self, ctx):
        if not self.roulette_is_running and (not AdditionalMethods.check_active() or AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name)) and not self.duel_is_running:
            self.roulette_is_running = True
            self.roulette_nicknames.append(ctx.author.name)
            await ctx.channel._ws.send_privmsg(config.CHAN, "Рулетка началась! У вас есть 20 секунд! Чтобы учавствовать напишите !accept")
            asyncio.get_event_loop().create_task(self.rand(self._ws))
        elif self.duel_is_running:
            AdditionalMethods.add_to_buffer("s", f"{ctx.author.name}, сейчас идёт дуэль", ctx.author, "omgroulette")

    @commands.command(name='пирамида')
    async def piramide(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            word = str.replace(ctx.message.content, '!пирамида ', "")
            await self._ws.send_privmsg(config.CHAN, "/color Red")
            await self._ws.send_privmsg(config.CHAN, f"/me {word}")
            await self._ws.send_privmsg(config.CHAN, "/color OrangeRed")
            await self._ws.send_privmsg(config.CHAN, f"/me {word} {word}")
            await self._ws.send_privmsg(config.CHAN, "/color YellowGreen")
            await self._ws.send_privmsg(config.CHAN, f"/me {word} {word} {word}")
            await self._ws.send_privmsg(config.CHAN, "/color Green")
            await self._ws.send_privmsg(config.CHAN, f"/me {word} {word} {word} {word}")
            await self._ws.send_privmsg(config.CHAN, "/color CadetBlue")
            await self._ws.send_privmsg(config.CHAN, f"/me {word} {word} {word}")
            await self._ws.send_privmsg(config.CHAN, "/color Blue")
            await self._ws.send_privmsg(config.CHAN, f"/me {word} {word}")
            await self._ws.send_privmsg(config.CHAN, "/color BlueViolet")
            await self._ws.send_privmsg(config.CHAN, f"/me {word}")
            await self._ws.send_privmsg(config.CHAN, "/color orangered")
            
    @commands.command(name='ауф')
    async def auf(self, ctx):
        nickname = ctx.author.name
        r = requests.get('https://socratify.net/quotes/random')
        soup = BeautifulSoup(r.content, 'lxml')
        d = soup.find('h1', class_='b-quote__text').get_text()
        AdditionalMethods.add_to_buffer("e", f"{nickname}, {d} AUFFF", ctx.author, "ауф")

    @commands.command(name='porf')
    async def porf(self, ctx):
        nickname = ctx.author.name
        word = str.replace(ctx.message.content, '!porf ', "")
        url = "https://models.dobro.ai/gpt2/medium/"
        if word == "!porf":
            AdditionalMethods.add_to_buffer("e", f"{nickname}, Впишите какое-либо предложение", ctx.author, "porf")
        elif len(word) > 300:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, Бот может принимать максимум 300 символов", ctx.author, "porf")
        else:
            response = requests.post(url, json={'prompt': word, 'length': '30', 'num_samples': '5'})
            if response.text == "Service Unavailable":
                AdditionalMethods.add_to_buffer("e", f"{nickname}, на данный момент Порфирьевич не работает. Попробуйте позже roflanPominy", ctx.author, "porf")
            else:
                json_response = response.json()
                result = json_response['replies'][4]
                with open('data/osujdau.txt', 'r', encoding='utf-8') as f:
                    l = [line.strip() for line in f]
                while any(x in result.lower() for x in l):
                    response = requests.post(url, json={'prompt': word, 'length': '30', 'num_samples': '5'})
                    json_response = response.json()
                    result = json_response['replies'][4]
                AdditionalMethods.add_to_buffer("e", f"{nickname}, " + word + result, ctx.author, "porf")

    @commands.command(name='save')
    async def logs(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            with open(file='data/TRASHMASSIVE.txt', mode='r', encoding='utf-8') as q:
                strer = q.read()
                
            with open(file='data/settings.txt', mode='r', encoding='utf-8') as mm:
                settings = mm.read()
                
                
            g = Github("f0011283768114fac26230cd23b3208ed10d0a54")
            repo = g.search_repositories("slonb0t")[0]
            
            
            contents = repo.get_contents("data/TRASHMASSIVE.txt")
            repo.delete_file(contents.path, "", contents.sha)
            repo.create_file("data/TRASHMASSIVE.txt", "", strer)
            
            contents1 = repo.get_contents("data/settings.txt")
            repo.delete_file(contents1.path, "", contents1.sha)
            repo.create_file("data/settings.txt", "", settings)
            
            
            AdditionalMethods.add_to_buffer("s", "Синхронизация статистик произошла успешно", ctx.author, "save")

    @commands.command(name='slon')
    async def slon(self, ctx):
        nickname = ctx.author.name
        story = nickname + ", дело было летом 2019 года, хесус играл в майнкрафт без модов и смог приручить себе кота, которого мы прозвали Слон, в один прекрасный солнечный день, он залез под блок, где была вода, и, медленно задыхаясь, умер peepoSad , этот бот будет вечным напоминанием о трагедии, которую никто не забудет roflanPominy "
        AdditionalMethods.add_to_buffer("s", story, ctx.author, "slon")
        
    @commands.command(name='kogda')
    async def strim(self, ctx):
        AdditionalMethods.add_to_buffer("c", "Стрим через час Jebaited", ctx.author, "kogda")

    @commands.command(name='case')
    async def case(self, ctx):
        nickname = ctx.author.name
        randstr = random.randint(1, 178)
        r = requests.get('https://market.csgo.com/?s=name&r=&q=&p=' + str(randstr))
        soup = BeautifulSoup(r.content, 'lxml')
        d = soup.find_all('a', class_='item')
        skin = str(random.choice(d))
        skin = re.sub("\n", '', skin)
        soupskin = BeautifulSoup(skin, 'lxml')
        price = soupskin.find('div', class_='price').get_text().replace(' ','')
        name = soupskin.find('div', class_='name').get_text()
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
            price = str(price) + " ₽ monkaX"
        AdditionalMethods.add_to_buffer("e",
                                        f"{nickname}, вам выпал " + name + " Стоимость: " + price,
                                        ctx.author, "case")

    @commands.command(name='history')
    async def stream(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        message = str.replace(message, '!history', '')
        message = message[1:len(message)]
        while message[0:1] == "!" or message[0:1] == "/":
            message = message[1:len(message)]
        AdditionalMethods.add_to_buffer("c", AdditionalMethods.get_last_stream_stat(message, nickname, ctx.author),
                                        ctx.author, "history")

    @commands.command(name='archive')
    async def streamh(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        message = str.replace(message, '!archive', '')
        while message[0:1] == "!" or message[0:1] == "/":
            message = message[1:len(message)]
        try:
            id = int(message[1:2])
            if len(message[2:len(message)]) > 1:
                tag = str.replace(message, f' {id} ', '')
                while tag[0:1] == "!" or tag[0:1] == "/":
                    tag = tag[1:len(tag)]
            else:
                tag = ''
            AdditionalMethods.add_to_buffer("c", AdditionalMethods.get_archive_stream_stat(id, nickname, tag,
                                                                                           ctx.author).format(nickname, id), ctx.author, "history")
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
        AdditionalMethods.add_to_buffer("s", f"{name} - {receptt}", ctx.author, "рецепт")
        await asyncio.sleep(2)
        AdditionalMethods.add_to_buffer("s", f"С{recept1}", ctx.author, "рецепт")

    @commands.command(name='анекдот')
    async def anekdot(self, ctx):
        r = requests.get('http://anecdotica.ru/')
        soup = BeautifulSoup(r.content, 'lxml')
        anekdot = soup.find('div', class_='item_text').get_text()
        anekdott = (anekdot[:493] + '...') if len(anekdot) > 493 else anekdot
        AdditionalMethods.add_to_buffer("e", '{} KeK'.format(str.replace(anekdott, "\r\n", " ")), ctx.author, "анекдот")
        
    @commands.command(name='перевод')
    async def perevod(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        if message == "!перевод":
            AdditionalMethods.add_to_buffer("с", f"{nickname}, cсылка со всеми языками: https://pastebin.com/raw/nk1n1KxD", ctx.author, "перевод")
        else:
            try:
                userlang = message.split(" ")[1]
                word = message.replace("!перевод " + userlang,"")
                dataa = {"text":word}
                url = "https://translate.yandex.net/api/v1/tr.json/translate?id=c71cd46e.5f6b52d5.c8b396f8.74722d74657874-0-0&srv=tr-text&lang="+userlang.lower()+"&reason=auto&format=text"
                r = requests.get(url, data=dataa)
                if str(r.status_code) == "400":
                    AdditionalMethods.add_to_buffer("с", "Неправильно указаны языки. Ссылка со всеми языками: https://pastebin.com/raw/nk1n1KxD", ctx.author, "перевод")
                else:
                    resultat = str(r.text).partition('t":["')[-1].replace('"]}',"")
                    with open('data/osujdau.txt', 'r', encoding='utf_8') as f:
                        l = [line.strip() for line in f]
                    if any(x in resultat.lower() for x in l):
                        AdditionalMethods.add_to_buffer("с", f"{nickname}, в переводе мы обнаружили бан-ворд PepoG", ctx.author, "перевод")
                    else:
                        AdditionalMethods.add_to_buffer("с", f"{nickname}, {resultat}", ctx.author, "курс")
            except:
                AdditionalMethods.add_to_buffer("с", f"{nickname}, неправильно указаны параметры. Ссылка со всеми языками: https://pastebin.com/raw/nk1n1KxD", ctx.author, "перевод")

    @commands.command(name='курс')
    async def kurs(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        if message == "!курс":
            url = "https://free.currconv.com/api/v7/convert?q=USD_RUB,EUR_RUB&compact=ultra&apiKey=ee315cc429cbc167d4b7"
            url2 = "https://free.currconv.com/api/v7/convert?q=JPY_RUB,UAH_RUB&compact=ultra&apiKey=ee315cc429cbc167d4b7"
            r = requests.get(url)
            r2 = requests.get(url2)
            json_r = r.json()
            json_r2 = r2.json()
            now = datetime.now() + timedelta(hours=3)
            today = now.strftime("%d.%m")
            resik = f"Курс валют на {today}: USD = {round(json_r['USD_RUB'],2)} RUB | EUR = {round(json_r['EUR_RUB'],2)} RUB | JPY = {round(json_r2['JPY_RUB'],4)} RUB | UAH = {round(json_r2['UAH_RUB'],2)} RUB"
            AdditionalMethods.add_to_buffer("с", resik, ctx.author, "курс")
        else:
            userkurs = message.split(" ")[1]
            try:
                count = message.split(" ")[2]
            except:
                AdditionalMethods.add_to_buffer("с", f"{nickname}, введите число", ctx.author, "курс")
            url = "https://free.currconv.com/api/v7/convert?q="+ userkurs.replace("-","_").upper()+"&compact=ultra&apiKey=ee315cc429cbc167d4b7"
            r = requests.get(url)
            if r.text == "{}":
                AdditionalMethods.add_to_buffer("с", f"{nickname}, неправильно введены валюты. Вводите в международном формате (USD-RUB, RUB-JPY)", ctx.author, "курс")
            else:
                try:
                    json_r = r.json()
                    res = userkurs.replace("-","_").upper()
                    one = userkurs.split("-")[0]
                    two = userkurs.split("-")[1]
                    result = f"{nickname}, {count} {one.upper()} = {str(round(json_r[res] * float(count),2))} {two.upper()}"
                    AdditionalMethods.add_to_buffer("с", result, ctx.author, "курс")
                except KeyError:
                    AdditionalMethods.add_to_buffer("с",f"{nickname}, произошла ошибка конвертации. Скорее всего вы неправильно написали валюты. PepoG", ctx.author, "курс")

    @commands.command(name='clipever')
    async def topclipever(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!clipever ', '')
        top = re.sub("\n", '', top)
        if top == "!clipever":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(0, top, nickname), ctx.author, "clip")

    @commands.command(name='clipyear')
    async def topclipyear(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!clipyear ', '')
        top = re.sub("\n", '', top)
        if top == "!clipyear":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(365, top, nickname), ctx.author, "clip")

    @commands.command(name='clipweek')
    async def topclipweek(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!clipweek ', '')
        top = re.sub("\n", '', top)
        if top == "!clipweek":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(7, top, nickname), ctx.author, "clip")

    @commands.command(name='clipmonth')
    async def topclipmonth(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!clipmonth ', '')
        top = re.sub("\n", '', top)
        if top == "!clipmonth":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(30, top, nickname), ctx.author, "clip")

    @commands.command(name='cliptoday')
    async def topclipday(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.content
        top = str.replace(message, '!cliptoday ', '')
        top = re.sub("\n", '', top)
        if top == "!cliptoday":
            top = ""
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(1, top, nickname), ctx.author, "clip")

    @commands.command(name='abbreviations')
    async def abbreviations(self, ctx):
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("c", f"{nickname} Здесь вы можете посмотреть все доступные аббревиатуры для clip {config.abreviationsUrl}", ctx.author, "abbreviations")

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
        
    @commands.command(name='заебало')
    async def zaebalo(self, ctx):
        nickname = ctx.author.name
        url = "https://zaebalo.ru/?page=" + str(random.randrange(1,1600,1))
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        d = soup.find_all('div', align='left')
        res = random.choice(d)
        res = re.sub(r'<.*?>','',str(res)).replace("    ","")
        res = re.sub(r'\n','',res)
        with open('data/osujdau.txt', 'r', encoding='utf-8') as f:
            l = [line.strip() for line in f]
        while any(x in res.lower() for x in l):
            res = random.choice(d)
            res = re.sub(r'<.*?>','',str(res)).replace("    ","")
            res = re.sub(r'\n','',res)
        if len(res) > 500:
            res = res[:300] + '...'
            AdditionalMethods.add_to_buffer("e", f"{nickname}, {res}", ctx.author, "zaebalo")
        else:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, {res}", ctx.author, "zaebalo")
                                                            
    @commands.command(name='pastа')
    async def pasta(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_simplefile_message("{}", "nadya"), ctx.author, "pastа")
                                                        
    @commands.command(name='help')
    async def help(self, ctx):
        nickname = ctx.author.name
        AdditionalMethods.add_to_buffer("c", f"catJAM Ку, {nickname}, со списком команд можешь ознакомиться здесь {config.helpUrl} catJAM", ctx.author, "help")

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
                AdditionalMethods.add_to_buffer("s",
                                                f"max: {data['buffermax']}, delay: {data['bufferdelay']}, entertain: {data['entertain']}, norm: {data['norm']}, maxmesses: {data['maxmesses']}, attentions: {data['attentions']}, emojimode: {data['emojimode']}, timeout: {data['timeout']}",
                                                ctx.author, "settings")

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
                    AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author,
                                                    "bufferdelay")

    @commands.command(name='attentions')
    async def attentions(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            timeout = str.replace(ctx.message.content, '!attentions ', '')
            timeout = re.sub("\n", '', timeout)
            timeout = str.replace(timeout, ",", ".")
            try:
                with open('data/settings.txt', 'r', encoding='utf-8') as b:
                    data = json.loads(b.read())
            except:
                data = {}
            with open('data/settings.txt', 'w', encoding='utf-8') as b:
                try:
                    data["attentions"] = int(timeout)
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} attentions: {data['attentions']}, emojimode: {data['emojimode']}, timeout: {data['timeout']}",
                                                    ctx.author, "attentions")
                except:
                    AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author,
                                                    "attentions")

    @commands.command(name='emojimode')
    async def emojimode(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            timeout = str.replace(ctx.message.content, '!emojimode ', '')
            timeout = re.sub("\n", '', timeout)
            timeout = str.replace(timeout, ",", ".")
            try:
                with open('data/settings.txt', 'r', encoding='utf-8') as b:
                    data = json.loads(b.read())
            except:
                data = {}
            with open('data/settings.txt', 'w', encoding='utf-8') as b:
                if timeout == "all" or timeout == "skip" or timeout == "skip_with":
                    data["emojimode"] = timeout
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} attentions: {data['attentions']}, emojimode: {data['emojimode']}, timeout: {data['timeout']}",
                                                    ctx.author, "emojimode")
                else:
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname}, есть только три фильтра для emogy: all, skip, skip_with",
                                                    ctx.author, "emojimode")

    @commands.command(name='timeout')
    async def timeout(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            timeout = str.replace(ctx.message.content, '!timeout ', '')
            timeout = re.sub("\n", '', timeout)
            timeout = str.replace(timeout, ",", ".")
            try:
                with open('data/settings.txt', 'r', encoding='utf-8') as b:
                    data = json.loads(b.read())
            except:
                data = {}
            with open('data/settings.txt', 'w', encoding='utf-8') as b:
                try:
                    data["timeout"] = int(timeout)
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} attentions: {data['attentions']}, emojimode: {data['emojimode']}, timeout: {data['timeout']}",
                                                    ctx.author, "timeout")
                except:
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname}, не удалось прочесть число",
                                                    ctx.author, "timeout")

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
                    AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author,
                                                    "buffermax")

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

    @commands.command(name='maxmesses')
    async def maxmesses(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            timeout = str.replace(ctx.message.content, '!maxmesses ', '')
            timeout = re.sub("\n", '', timeout)
            timeout = str.replace(timeout, ",", ".")
            try:
                with open('data/settings.txt', 'r', encoding='utf-8') as b:
                    data = json.loads(b.read())
            except:
                data = {}
            with open('data/settings.txt', 'w', encoding='utf-8') as b:
                try:
                    data["maxmesses"] = int(timeout)
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} norm: {data['norm']},"
                                                    f" maxmesses: {data['maxmesses']}",
                                                    ctx.author, "maxmesses")
                except:
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname}, не удалось прочесть число (оно должно быть не дробным) PepoG ",
                                                    ctx.author,
                                                    "maxmesses")

    @commands.command(name='norm')
    async def norm(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            timeout = str.replace(ctx.message.content, '!norm ', '')
            timeout = re.sub("\n", '', timeout)
            timeout = str.replace(timeout, ",", ".")
            try:
                with open('data/settings.txt', 'r', encoding='utf-8') as b:
                    data = json.loads(b.read())
            except:
                data = {}
            with open('data/settings.txt', 'w', encoding='utf-8') as b:
                try:
                    data["norm"] = float(timeout)
                    b.write(json.dumps(data))
                    AdditionalMethods.add_to_buffer("s",
                                                    f"{nickname} norm: {data['norm']},"
                                                    f" maxmesses: {data['maxmesses']}",
                                                    ctx.author, "norm")
                except:
                    AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author,
                                                    "norm")

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
            AdditionalMethods.add_to_buffer("e", randomm.format(nickname), ctx.author, "me")
																										
    @commands.command(name='кто')
    async def kto(self, ctx):
	message = ctx.message.content
        ktoo = message.replace('!кто ','')
	global namess
	seet = set(namess)
	rand = random.choice(list(seet))
	AdditionalMethods.add_to_buffer("e", ktoo + ' - ' + rand + ' OpieOP', ctx.author, "кто")
																												
    @commands.command(name='do')
    async def do(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        if message == "!do":
            AdditionalMethods.add_to_buffer("e", f"{nickname}, введите !do [message]", ctx.author, "do")
        else:
            do = str.replace(message, '!do ', '')
            do = re.sub("\n", '', do)
            do = do.replace('@','')
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
            if len(bubu) < 117:
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
        nickname = ctx.author.name
        message = ctx.message.content
        if message == "!время":
            AdditionalMethods.add_to_buffer("c", datetime.strftime(datetime.now() + timedelta(hours=3),
                                                                   f"{nickname}, Чичас %H:%M по МСК Waiting"), ctx.author, "время")
        else:
            loc = str.replace(message, '!время ', '')
            url = "http://search.maps.sputnik.ru/search?q="
            response = requests.get(url + quote(loc))
            if response.text.find('"found":0') != -1:
                AdditionalMethods.add_to_buffer("c", f"{nickname}, не найден населённый пункт. Попробуйте другое название.", ctx.author, "время")
            else:
                try:
                    position = response.json()['result'][0]['position']
                    url = "http://api.timezonedb.com/v2.1/get-time-zone?key=APM2N08MFF2O&format=json&by=position&lat="
                    response1 = requests.get(url + str(position['lat']) + "&lng=" + str(position['lon']))
                    timestamp = response1.json()['timestamp']
                    dt_object = datetime.fromtimestamp(timestamp)
                    date = dt_object.strftime("%H:%M")
                    location = response.json()['result'][0]['title']
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, чичас {date} в «{location}» Waiting", ctx.author, "время")
                except:
                    AdditionalMethods.add_to_buffer("c", f"{nickname}, не удалось найти время для этого населённого пункта", ctx.author, "время")

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
                                                        
    @commands.command(name='japtest')
    async def japtest(self, ctx):
        nickname = ctx.author.name
        if not self.japtest['active']:
            self.japtest['active'] = True
            message = ctx.message.content
            category = str.split(message, " ")[1].lower()
            if category == "n1" or category == "n2" or category == "n3" or category == "n4" or category == "n5":
                with open('data/kanji.txt', 'r', encoding='utf_8') as f:
                    all = f.read()
                if category == "n5":
                    rd = random.randint(0, 103)
                elif category == "n4":
                    rd = random.randint(104, 284)
                elif category == "n3":
                    rd = random.randint(285, 650)
                elif category == "n2":
                    rd = random.randint(651, 1023)
                elif category == "n1":
                    rd = random.randint(1024, 1273)
                else:
                    rd = 0
                result = all[rd: rd + 1]
                print(result)
                i = 1
                r = requests.get(f"https://jlptsensei.com/page/{i}/?s={result}")
                soup = BeautifulSoup(r.content, 'lxml')
                mass = soup.findAll('a', class_='btn btn-dark')
                e = True
                url = ""
                if category != "n1":
                    while e:
                        for q in mass:
                            print(q)
                            if "learn-japanese-kanji" in q.get("href"):
                                url = q.get("href")
                                e = False
                        i += 1
                        await asyncio.sleep(0.2)
                        r = requests.get(f"https://jlptsensei.com/page/{i}/?s={result}")
                        print(f"https://jlptsensei.com/page/{i}/?s={result}")
                        soup = BeautifulSoup(r.content, 'lxml')
                        mass = soup.findAll('a', class_='btn btn-dark')
                        if soup.find('span', class_='jp'):
                            e = False
                print(url)
                if len(url) == 0:
                    dataa = {"text": result}
                    url = "https://translate.yandex.net/api/v1/tr.json/translate?id=9bade3aa.5f5e1930.ae218027.74722d74657874-5-0&srv=tr-text&lang=ja-en&reason=auto&format=text"
                    await asyncio.sleep(0.2)
                    r = requests.get(url, data=dataa)
                    resultat = str(r.text).partition('t":["')[-1].replace('"]}', "")
                    self.japtest['kanji'] = result
                    self.japtest['tr'] = resultat
                    AdditionalMethods.add_to_buffer("e", f"{nickname}, {result}, чтобы увидеть перевод напишите !tr", ctx.author, "japtest")
                else:
                    r = requests.get(url)
                    sp = BeautifulSoup(r.content, 'lxml')
                    translation = sp.find('p', class_='eng-definition p-lg').string
                    self.japtest['kanji'] = result
                    self.japtest['tr'] = translation
                    if sp.find('p', class_='m-0 jp'):
                        ex = sp.find('p', class_='m-0 jp').text
                        ex_translation = sp.find('div', class_='alert alert-primary').text
                        self.japtest['example'] = ex
                        self.japtest['tr_example'] = ex_translation
                    else:
                        self.japtest['example'] = ""
                        self.japtest['tr_example'] = ""
                    print(self.japtest)
                    if len(self.japtest['example']) > 0:
                        AdditionalMethods.add_to_buffer("e", f"{nickname}, {result}, example: {self.japtest['example']}, чтобы увидеть перевод напишите !tr",
                                                        ctx.author, "japtest")
                    else:
                        AdditionalMethods.add_to_buffer("e", f"{nickname}, {result}, чтобы увидеть перевод напишите !tr",
                                                        ctx.author, "japtest")
                    self.japtest['active'] = False
            else:
                AdditionalMethods.add_to_buffer("e", f"{nickname}, введите категорию кандзи японского языка 'n1-n5'", ctx.author, "japtest")
        else:
            AdditionalMethods.add_to_buffer("s", f"{nickname}, сейчас работает поиск другого кандзи PepoG",
                                            ctx.author, "japtest")

    @commands.command(name='tr')
    async def tr(self, ctx):
        nickname = ctx.author.name
        if len(self.japtest['kanji']) > 0:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, {self.japtest['kanji']} - {self.japtest['tr']}, example: {self.japtest['example']} - {self.japtest['tr_example']}",
                                            ctx.author, "japtest")
            self.japtest = {'kanji': '', 'tr': '', 'example': '', 'tr_example': '', 'active': False}
        else:
            AdditionalMethods.add_to_buffer("e",
                                            f"{nickname}, сейчас никаких кандзи нет в очереди PepoG",
                                            ctx.author, "japtest")

    @commands.command(name='wiki')
    async def wiki(self, ctx):
        content = ctx.message.content
        content = content.replace('!wiki ', '')
        wikipedia.set_lang("ru")
        try:
            info = wikipedia.summary(content, chars=300)
        except wikipedia.DisambiguationError as e:
            p = e.options
            s = random.choice(e.options)
            info = wikipedia.summary(content, chars=300)
        except wikipedia.exceptions.PageError:
            return
        info = re.sub(r"\([^()]*\)", "", info)
        finaly = f"{ctx.author.name}, {info}"
        AdditionalMethods.add_to_buffer("c", finaly, ctx.author, "wiki")

                                                        
                                                        
subprocess.Popen([sys.executable, 'ChatBot.py'])
subprocess.Popen([sys.executable, 'BufferCleaner.py'])
subprocess.Popen([sys.executable, 'CheckingStreamThread.py'])
bot = CommandsBot()
bot.run()
