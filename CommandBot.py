import sys
from abc import ABC
from github import Github
from twitchioc.ext import commands
from datetime import timedelta, datetime, date
from bs4 import BeautifulSoup
import requests
import AdditionalMethods
import Settings
import re
import random
import subprocess
import config
import json
import emoji
from urllib.parse import quote
import asyncio
import time
import lyricsgenius as lg
import entertain_functions


# вместо ctx.message.content ctx.message.clean_content, он выводит только текст после комманды
# использовать ctx.author.display_name, но только там, где ники выводятся


class CommandsBot(commands.Bot, ABC):

    def __init__(self):
        super().__init__(irc_token=f'oauth:{config.OAUTH}',
                         client_id=config.CLIENT_ID, nick=config.BOT, prefix='!',
                         initial_channels=config.CHANNELS)
        self.roulette_is_running = False
        self.roulette_nicknames = []
        self.omgroulette_kd = 10
        self.omgroulette_last_use = 0
        self.duel_is_running = False
        self.duel_nicknames = []
        self.duel_user = ""
        self.duel_serious = True
        self.spammers = {}
        self.seekers = []
        self.logs = []
        self.namess = []
        self.names_exp = self.initial_channels
        self.blbl = []
        self.ii = 0
        with open('data/blacklist.txt', encoding='utf-8') as f:
            self.blacklist = [x for x in f.read().split('\n') if len(x) > 1]
        self.genius = lg.Genius("5Pj7QcUoV5Khbd-Hq5jSve8OzCQILJkY8nWojIIxqH30ItpsmXC7UmCRcgjmTVPY")
        print('Blacklist:', self.blacklist)
    
    async def event_command_error(self, ctx, error):
        pass
    
    async def duelent(self, socket):
        i: int = 0
        while len(self.duel_nicknames) == 1 and i < 200:
            i += 1
            await asyncio.sleep(0.1)
        if len(self.duel_nicknames) == 1:
            await socket.send_privmsg(config.CHAN, "Оппонент не принял дуэль monkaHmm")
        else:
            if self.duel_serious:
                await socket.send_privmsg(config.CHAN,
                                          "Дуэлянты смотрят друг на друга monkaW . В любой момент они готовы достать "
                                          "револьвер из кобуры... PepeS ")
                randname = random.choice(self.duel_nicknames)
                self.duel_nicknames.remove(randname)
                await asyncio.sleep(8)
                with open(file='data/duel_rand.txt', mode='r', encoding='utf-8') as e:
                    data = json.loads(e.read())
                randseq = random.choice(data)
                await socket.send_privmsg(config.CHAN,
                                          f"Хлопок! {self.duel_nicknames[0]['label']} выстреливает в {randname['label']}{randseq['text']}")
                if int(randseq['time']) > 1:
                    await asyncio.sleep(0.5)
                    await socket.send_privmsg(config.CHAN, f"/timeout {randname['str_id']} {randseq['time']}")
                elif int(randseq['time']) > 0:
                    await socket.send_privmsg(config.CHAN, f"/timeout {self.duel_nicknames[0]['str_id']} 60")
            else:
                await socket.send_privmsg(config.CHAN,
                                          "Один из дуэлянтов бессмертен, поэтому они стреляют холостыми пулями monkaW "
                                          ". В любой момент они готовы достать револьвер из кобуры... PepeS")
                randname = random.choice(self.duel_nicknames)
                self.duel_nicknames.remove(randname)
                await asyncio.sleep(8)
                await socket.send_privmsg(config.CHAN,
                                          f"Хлопок! Точный выстрел заставляет {randname['label']} сдаться. Самая быстрая рука дикого запада – {self.duel_nicknames[0]['label']} EZ")
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
            await socket.send_privmsg(config.CHAN, "А умирает сегодня " + randname['label'] + ", ББ!")
            await socket.send_privmsg(config.CHAN, f"/timeout {randname['str_id']} 60")
        self.roulette_nicknames.clear()
        self.roulette_is_running = False
        self.omgroulette_last_use = time.time()
    
    async def check_mess(self, user, socket, nick):
        try:
            requests.post(f"https://sl0n.herokuapp.com/stats/{self.initial_channels[0]}", data={'type': 'clear', 'nickname': user}, headers=config.head)
            Client_ID = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
            OAUTH = 'l4tt0z3a94edvjo3kbs0c3s4qimpsp'
            url = 'https://api.twitch.tv/gql'
            head = {'Authorization': f'OAuth {OAUTH}', 'Client-ID': Client_ID}
            head_2 = {'Authorization': f'Bearer {OAUTH}', 'Client-ID': Client_ID}
            hash_name = '2c484f8a5ff63f06732707c8ca989083e46b2aa81a03b02e7ac7b9aa9fcba9a2'
            url_2 = f'https://api.twitch.tv/helix/users?login={nickname}'
            mess_count = 0
            try:
                sender = requests.get(url_2, headers=head_2).json()['data'][0]['id']
            except IndexError:
                sender = 0
            data_loop = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ|0')
            while True:
                try:
                    json_msg = [{"operationName":"ViewerCardModLogsMessagesBySender","variables":{"senderID":sender,"channelLogin":self.initial_channels[0],"cursor":data_loop,"includeAutoModCaughtMessages":True},"extensions":{"persistedQuery":{"version":1,"sha256Hash":hash_name}}}]
                    r = requests.post(url, headers=head, json=json_msg).json()[0]['data']['channel']['modLogs']['messagesBySender']['edges']
                    if len(r) == 0:
                        break
                    a = [b['cursor'] for b in r if 'sentAt' in b['node']]
                    data_loop = a[-1]
                    mess_count += len(a)
                except:
                    break
            requests.post(f"https://sl0n.herokuapp.com/stats/{self.initial_channels[0]}", data={'type': 'add', 'nickname': user, 'count': mess_count}, headers=config.head)
            await socket.send_privmsg(config.CHAN, f'{nick}, Пользователь {user} написал {mess_count} сообщений в чате!')
        except KeyError:
            await socket.send_privmsg(config.CHAN, f'{nick}, попробуйте другой ник WeirdChamp')
                                      
    async def event_ready(self):
        print(f'Ready {str(self.__class__.__name__)} | {self.nick} on {self.initial_channels[0]}')
        #await self.synch()

    async def synch(self):
        self.seekers = requests.get(config.api_url + f"/seekers/{self.initial_channels[0]}", headers=config.head).json()['answer']

    async def event_message(self, message):
        nickname = message.author.name
        nnn = message.author.display_name
        if nnn not in self.namess and nickname != 'moobot' and nickname != 'slonb0t' and nickname != 'kryabot':
            if self.ii > 5:
                del self.namess[0]
            self.namess.append(nnn)
            self.ii += 1
        if nnn not in self.names_exp:
            self.names_exp.append(nnn)
        try:
            badge = message.author.tags['badges'][:3]
        except KeyError:
            badge = ''
        if not AdditionalMethods.vip(message.author.is_mod, nickname) and not nickname == "slonb0t" and not badge == 'vip':
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
                        {"timenow": datetime.strftime(datetime.utcnow() + timedelta(hours=3), "%H:%M:%S"),
                         "messtime": round(time.time() - self.spammers[nickname]["time"], 2),
                         "messes": self.spammers[nickname]['messes'], "content": message.content})
                else:
                    self.spammers[nickname] = {}
                    self.spammers[nickname]["time"] = time.time()
                    self.spammers[nickname]["messes"] = 1
                    self.spammers[nickname]["worned"] = 0
                    self.spammers[nickname]["log"] = [
                        {"timenow": datetime.strftime(datetime.utcnow() + timedelta(hours=3), "%H:%M:%S"),
                         "messtime": round(time.time() - self.spammers[nickname]["time"], 2),
                         "messes": self.spammers[nickname]['messes'], "content": message.content}]

                if self.spammers[nickname]["messes"] > 1:
                    if time.time() - self.spammers[nickname]["time"] < Settings.get_norm() and self.spammers[nickname][
                        "messes"] == Settings.get_max_messes():
                        if "warntime" in self.spammers[nickname].keys():
                            if time.time() - self.spammers[nickname]["warntime"] > Settings.get_forget_kd():
                                self.spammers[nickname]["worned"] = 0
                            self.spammers[nickname]["warntime"] = time.time()
                        else:
                            self.spammers[nickname]["warntime"] = time.time()
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
                                await self._ws.send_privmsg(config.CHAN,
                                                            f"/w {f} {nickname} отлетел на {Settings.get_timeout()}")
                            await self._ws.send_privmsg(config.CHAN,
                                                        f"/timeout {nickname} {Settings.get_timeout()} Spam, automated by SLONB0T")
                            await self._ws.send_privmsg(config.CHAN,
                                                        f"/w {nickname} Вы получили слишком много предупреждений и временно отстраняетесь от чата")
                        else:
                            self.spammers[nickname]["worned"] += 1
                            stringer += f"был предупреждён {self.spammers[nickname]['worned']} из {Settings.get_attentions()} раз с настройками: |norm: {Settings.get_norm()}, maxmesses: {Settings.get_max_messes()}, emojimode: {Settings.get_mod()}|"
                            for f in self.seekers:
                                await self._ws.send_privmsg(config.CHAN,
                                                            f"/w {f} {nickname} был предупреждён {self.spammers[nickname]['worned']} из {Settings.get_attentions()} раз")
                            await self._ws.send_privmsg(config.CHAN,
                                                        f"/w {nickname} Вы слишком часто отправляете сообщения на канале {self.initial_channels[0]}, это {self.spammers[nickname]['worned']} из {Settings.get_attentions()} предупреждений!")
                        requests.post(config.api_url + f"/logs/{self.initial_channels[0]}",
                                      data={"log": stringer.encode(
                                          "utf-8"), "nickname": nickname, "warns": {self.spammers[nickname]['worned']},
                                          "time": time.time()}, headers=config.head)
                        self.spammers[nickname]["log"].clear()
                    elif time.time() - self.spammers[nickname]["time"] >= Settings.get_norm():
                        self.spammers[nickname]["time"] = time.time()
                        self.spammers[nickname]["log"].clear()
                        self.spammers[nickname]["messes"] = 0
        if message.content[0:2] == "! " or nickname in self.blacklist or nickname in self.blbl or 'all' in self.blbl:
            if not AdditionalMethods.vip(message.author.is_mod, nickname):
                return
        await self.handle_commands(message)
    '''
    @commands.command(name="stat")
    async def stat(self, ctx):
        nickname = ctx.author.name
        message = ctx.message.clean_content.replace('@', '').lower()
        if len(message) == 0:
            message = nickname
        answer = json.loads(requests.get(config.api_url + f"/stats/{self.initial_channels[0]}?nickname={message}", headers=config.head).content.decode("utf-8"))
        if answer['type'] == 'success':
            if ctx.message.clean_content == "info":
                AdditionalMethods.add_to_buffer("c", ctx.author.display_name + f", Данные бота актуальны с {answer['start_date']}, сообщения актуальны с 2016 года", ctx.author, "stat")
            else:
                answer_str = ""
                if 'count' in answer['answer'].keys():
                    answer_str += "Пользователь " + message + " написал " + str(answer['answer']['count']) + " сообщений в чат | "
                if 'watch_time_offline' in answer['answer'].keys():
                    answer_str += "Оффлайн: " + AdditionalMethods.parse_time(answer['answer']['watch_time_offline'] * 60) + " | "
                if 'watch_time_online' in answer['answer'].keys():
                    answer_str += "Онлайн: " + AdditionalMethods.parse_time(answer['answer']['watch_time_online'] * 60) + " | "
                AdditionalMethods.add_to_buffer("c", ctx.author.display_name + f", {answer_str[:-3]}", ctx.author, "stat")
        else:
            AdditionalMethods.add_to_buffer("s",f"{nickname}, {message} не найден, поставлен на сканирование peepoJuiceSpin", ctx.author, "stat")
            asyncio.get_event_loop().create_task(self.check_mess(message, self._ws, nickname))
    '''
    @commands.command(name='кто')	
    async def kto(self, ctx):	
        message = ctx.message.clean_content.replace('@', '')[:80]
        random.seed(message)
        name = random.choice(self.namess)
        random.seed()
        for nick in self.names_exp:	
            for word in message.split():	
                if str(word).lower().find(str(nick).lower()) != -1:	
                    message = message.replace(word, nick)	
        AdditionalMethods.add_to_buffer("e",f'{name} {message} OpieOP', ctx.author, "кто")

    @commands.command(name='mute')
    async def mute(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            messagee = ctx.message.clean_content.replace('@','')
            with open('data/blacklist.txt', mode='a', encoding='utf-8') as text:
                text.write(messagee.lower()+'\n')
            self.blbl.append(messagee.lower())
            AdditionalMethods.add_to_buffer("s", f"Пользователь {messagee} теперь в чёрном списке бота!", ctx.author,"mute")
    
    @commands.command(name='unmute')
    async def unmute(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            messagee = ctx.message.clean_content.replace('@','')
            if messagee.lower() in self.blbl:
                del self.blbl[self.blbl.index(messagee.lower())]
            with open('data/blacklist.txt', mode='r', encoding='utf-8') as textr:
                text_pre = textr.read()
            if text_pre.find(messagee.lower()) != -1:
                text_pre = text_pre.replace(messagee.lower()+'\n', '')
            with open('data/blacklist.txt', mode='w', encoding='utf-8') as textw:
                textw.write(text_pre)
            AdditionalMethods.add_to_buffer("s", f"Пользователь {messagee} удалён из чёрного списка бота!", ctx.author,"unmute")
    
    @commands.command(name='seek')
    async def seek(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            if not nickname in self.seekers:
                self.seekers.append(nickname)
                if requests.post(config.api_url + f"/seekers/{self.initial_channels[0]}", data={'nick': nickname, 'enabled': 1}, headers=config.head).json()['type'] == "error":
                    AdditionalMethods.add_to_buffer("s",
                                                    f"Вы подписаны на уведомления о спаме! (это изменение не было сохраненно в постоянную базу данных)",
                                                    ctx.author,
                                                    "seek")
                else:
                    AdditionalMethods.add_to_buffer("s", f"Вы подписаны на уведомления о спаме!", ctx.author, "seek")
            else:
                AdditionalMethods.add_to_buffer("s", f"Вы уже подписаны на уведомления о спаме ResidentSleeper", ctx.author, "seek")

    @commands.command(name='unseek')
    async def unseek(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.name
            if not nickname in self.seekers:
                AdditionalMethods.add_to_buffer("s", f"Вы не подписаны на уведомления о спаме ResidentSleeper", ctx.author, "unseek")
            else:
                self.seekers.remove(nickname)
                if requests.post(config.api_url + f"/seekers/{self.initial_channels[0]}", data={'nick': nickname, 'enabled': 0},
                                 headers=config.head).json()['type'] == "error":
                    AdditionalMethods.add_to_buffer("s",
                                                    f"Вы отписаны от уведомлений о спаме! (это изменение не было сохраненно в постоянную базу данных)",
                                                    ctx.author,
                                                    "unseek")
                else:
                    AdditionalMethods.add_to_buffer("s", f"Вы отписаны от уведомлений о спаме!", ctx.author, "unseek")

    @commands.command(name='helpm')
    async def helpm(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            AdditionalMethods.add_to_buffer("s",
                                            f"!bufferdelay [time], !buffermax [int], !entertain [0-1], !settings, !norm [time], !maxmesses [int], !attentions [int], !mode [all,skip,skip_with], !timeout [int], !forget [time]",
                                            ctx.author, "helpm")

    @commands.command(name='acduel')
    async def acduel(self, ctx):
        if self.duel_is_running:
            if ctx.author.display_name.lower() == self.duel_user.lower() or ctx.author.name.lower() == self.duel_user.lower():
                if self.duel_serious:
                    if ctx.author.is_mod:
                        self.duel_serious = False
                    else:
                        self.duel_serious = True
                self.duel_nicknames.append({"label": ctx.author.display_name, "str_id": ctx.author.name})

    @commands.command(name='duel')
    async def duel(self, ctx):
        nickname = ctx.author.display_name
        if not self.duel_is_running and (
                not AdditionalMethods.check_active() or AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name)) and not self.roulette_is_running:
            if ctx.author.is_mod:
                self.duel_serious = False
            else:
                self.duel_serious = True
            message = ctx.message.clean_content.replace('@', '')
            if len(message) > 1 and len(message) <= 26 and message.find(" ") == -1:
                self.duel_is_running = True
                self.duel_nicknames.append({"label": ctx.author.display_name, "str_id": ctx.author.name})
                self.duel_user = message.replace("@", "")
                if nickname.lower() != self.duel_user.lower():
                    await ctx.channel._ws.send_privmsg(config.CHAN,
                                                       f"{nickname} кидает перчатку в {message.replace('@', '')}, вызывая его на дуэль peepoCool . Чтобы принять вызов – напишите !acduel.")
                else:
                    await ctx.channel._ws.send_privmsg(config.CHAN,
                                                       f"{nickname} направил ствол на ... самого себя blushW . Если вы уверены в своём выборе, напишите !acduel.")
                asyncio.get_event_loop().create_task(self.duelent(self._ws))
            else:
                await ctx.channel._ws.send_privmsg(config.CHAN,
                                                   f"{nickname}, напишите никнейм правильно PepoG")
        elif self.duel_is_running:
            AdditionalMethods.add_to_buffer("s", f"{ctx.author.name}, сейчас уже идёт дуэль", ctx.author, "duel")
        elif self.roulette_is_running:
            AdditionalMethods.add_to_buffer("s", f"{ctx.author.name}, сейчас идёт общая рулетка", ctx.author, "duel")

    @commands.command(name='accept')
    async def accept(self, ctx):
        if self.roulette_is_running:
            if not {"label": ctx.author.display_name, "str_id": ctx.author.name} in self.roulette_nicknames:
                self.roulette_nicknames.append({"label": ctx.author.display_name, "str_id": ctx.author.name})

    @commands.command(name='omgroulette')
    async def omgroulette(self, ctx):
        if not self.roulette_is_running and (
                (not AdditionalMethods.check_active() and time.time() - self.omgroulette_last_use > self.omgroulette_kd) or AdditionalMethods.vip(
                    ctx.author.is_mod, ctx.author.name)
                        ) and not self.duel_is_running:
            self.roulette_is_running = True
            self.roulette_nicknames.append({"label": ctx.author.display_name, "str_id": ctx.author.name})
            await ctx.channel._ws.send_privmsg(config.CHAN,
                                               "Рулетка началась! У вас есть 20 секунд! Чтобы учавствовать напишите !accept")
            asyncio.get_event_loop().create_task(self.rand(self._ws))
        elif self.duel_is_running:
            AdditionalMethods.add_to_buffer("s", f"{ctx.author.name}, сейчас идёт дуэль", ctx.author, "omgroulette")
        elif self.roulette_is_running:
            AdditionalMethods.add_to_buffer("s", f"{ctx.author.name}, сейчас уже идёт общая рулетка", ctx.author, "omgroulette")
        elif time.time() - self.omgroulette_last_use < self.omgroulette_kd:
            AdditionalMethods.add_to_buffer("s", f"{ctx.author.name}, эту команду можно использовать только раз в {self.omgroulette_kd} секунд!", ctx.author,
                "omgroulette")
                                                       
    @commands.command(name='пирамида')
    async def piramide(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            word = ctx.message.clean_content
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
            await self._ws.send_privmsg(config.CHAN, "/color SpringGreen")

    @commands.command(name='ауф')
    async def auf(self, ctx):
        nickname = ctx.author.display_name
        r = requests.get('https://socratify.net/quotes/random')
        d = BeautifulSoup(r.content, 'lxml').find('h1', class_='b-quote__text').get_text()
        while len(d) > 80:
            r = requests.get('https://socratify.net/quotes/random')
            d = BeautifulSoup(r.content, 'lxml').find('h1', class_='b-quote__text').get_text()
        AdditionalMethods.add_to_buffer("e", f"{nickname}, {d} AUFFF", ctx.author, "ауф")

    @commands.command(name='porf')
    async def porf(self, ctx):
        nickname = ctx.author.display_name
        words = ctx.message.clean_content.replace('@', '')
        url = "https://pelevin.gpt.dobro.ai/generate/"
        if len(words) == 0:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, Впишите какое-либо предложение", ctx.author, "porf")
        elif len(words) > 200:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, Бот может принимать максимум 200 символов", ctx.author,
                                            "porf")
        else:
            words += ' '
            response = requests.post(url, json={'prompt': words, 'length': '20', 'num_samples': '5'})
            if response.text == "Service Unavailable":
                AdditionalMethods.add_to_buffer("e",
                                                f"{nickname}, на данный момент Порфирьевич не работает. Попробуйте позже roflanPominy",
                                                ctx.author, "porf")
            else:
                json_response = response.json()
                result = json_response['replies'][4]
                with open('data/osujdau2.txt') as f:
                    osu = [x for x in f.read().split('\n') if len(x) > 1]
                res_prov = re.sub(r'[^\w ]', '', result)
                for word in res_prov.split():
                    for asu in osu:
                        if word.lower().find(asu) != -1:
                            result = result.replace(word, '*' * len(word))
                if len(result) > 40 and len(words) > 30:
                    AdditionalMethods.add_to_buffer("e", f"{nickname}, {result}", ctx.author, "porf")
                else:
                    AdditionalMethods.add_to_buffer("e", f"{nickname}, {words}{result}", ctx.author, "porf")
                                                       
    @commands.command(name='save')
    async def logs(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            with open(file='data/TRASHMASSIVE.txt', mode='r', encoding='utf-8') as q:
                strer = q.read()

            with open(file='data/settings.txt', mode='r', encoding='utf-8') as mm:
                settings = mm.read()
                                                       
            with open(file='data/blacklist.txt', mode='r', encoding='utf-8') as bl:
                black = bl.read()

            g = Github("f0011283768114fac26230cd23b3208ed10d0a54")
            repo = g.search_repositories("slonb0t")[0]

            contents = repo.get_contents("data/TRASHMASSIVE.txt")
            repo.delete_file(contents.path, "", contents.sha)
            repo.create_file("data/TRASHMASSIVE.txt", "", strer)

            contents1 = repo.get_contents("data/settings.txt")
            repo.delete_file(contents1.path, "", contents1.sha)
            repo.create_file("data/settings.txt", "", settings)
                                                       
            contents1 = repo.get_contents("data/blacklist.txt")
            repo.delete_file(contents1.path, "", contents1.sha)
            repo.create_file("data/blacklist.txt", "", black)

            AdditionalMethods.add_to_buffer("s", "Синхронизация статистик произошла успешно", ctx.author, "save")

    @commands.command(name='kogda')
    async def strim(self, ctx):
        AdditionalMethods.add_to_buffer("c", "Стрим через час Jebaited", ctx.author, "kogda")

    @commands.command(name='history')
    async def stream(self, ctx):
        nickname = ctx.author.display_name
        message = ctx.message.clean_content.replace('@', '')
        while message[0:1] == "!" or message[0:1] == "/":
            message = message[1:len(message)]
        AdditionalMethods.add_to_buffer("c", AdditionalMethods.get_last_stream_stat(message, nickname, ctx.author),
                                        ctx.author, "history")

    @commands.command(name='archive')
    async def streamh(self, ctx):
        nickname = ctx.author.display_name
        message = ctx.message.clean_content.replace('@', '')
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
            AdditionalMethods.add_to_buffer("c", AdditionalMethods.get_archive_stream_stat(id, nickname, tag, ctx.author).format(nickname, id), ctx.author, "archive")
        except:
            AdditionalMethods.add_to_buffer("с", f'{nickname} !archive [0-9]', ctx.author, "archive")

    @commands.command(name='рецепт')
    async def recept(self, ctx):
        r = requests.get('http://culinar.ivest.kz/randomMenu')
        soup = BeautifulSoup(r.content, 'lxml')
        name = soup.find('a', class_='rec_name').get_text()
        recept = soup.find('div', class_='randome_recept_right').get_text()
        receptt = recept.partition('Способ приготовления:')[0]
        recept1 = recept.partition('Способ приготовления:')[2]
        AdditionalMethods.add_to_buffer("s", f"{name} - {receptt}", ctx.author, "рецепт")
        await asyncio.sleep(1)
        AdditionalMethods.add_to_buffer("s", f"Способ приготовления: {recept1}", ctx.author, "рецепт")

    @commands.command(name='нг')
    async def ng(self, ctx):
        nickname = ctx.author.display_name
        new_year = datetime(2020, 12, 31, 23, 59, 59)
        t = datetime.today()
        res = (new_year - timedelta(days=t.day, minutes=t.minute, hours=t.hour)) - timedelta(hours=3)
        AdditionalMethods.add_to_buffer("e", f'{nickname}, Новый Год через {res.day} дней {res.hour} часов и {res.minute} минут FeelsRainMan', ctx.author, "нг")
                                                       
    @commands.command(name='анекдот')
    async def anekdot(self, ctx):
        r = requests.get('http://anecdotica.ru/')
        soup = BeautifulSoup(r.content, 'lxml')
        anekdot = soup.find('div', class_='item_text').get_text()
        while len(anekdot) > 100:
            r = requests.get('http://anecdotica.ru/')
            anekdot = BeautifulSoup(r.content, 'lxml').find('div', class_='item_text').get_text()
        AdditionalMethods.add_to_buffer("e", f'{anekdott} KEKL', ctx.author, "анекдот")

    @commands.command(name='перевод')
    async def perevod(self, ctx):
        nickname = ctx.author.display_name
        message = ctx.message.content
        if len(message) == 0:
            AdditionalMethods.add_to_buffer("с",
                                            f"{nickname}, cсылка со всеми языками: https://pastebin.com/raw/nk1n1KxD",
                                            ctx.author, "перевод")
        else:
            try:
                userlang = message.split(" ")[1]
                word = message.replace("!перевод " + userlang, "")
                dataa = {"text": word}
                key = '3a68ec8e.5fdcccb2.31b3d49b.74722d74657874-0-0'
                url = "https://translate.yandex.net/api/v1/tr.json/translate?id="+key+"&srv=tr-text&lang=" + userlang.lower() + "&reason=auto&format=text"
                r = requests.get(url, data=dataa)
                if r.status_code == 400:
                    AdditionalMethods.add_to_buffer("с",
                                                    "Неправильно указаны языки. Ссылка со всеми языками: https://pastebin.com/raw/nk1n1KxD",
                                                    ctx.author, "перевод")
                else:
                    resultat = str(r.text).partition('t":["')[-1].replace('"]}', "")
                    with open('data/osujdau2.txt', 'r', encoding='utf-8') as f:
                        osu = [x for x in f.read().split('\n') if len(x) > 1]
                    res_prov = re.sub(r'\W+', ' ', resultat)
                    for word in res_prov.split():
                        for asu in osu:
                            if word.lower().find(asu) != -1:
                                resultat = resultat.replace(word, '*' * len(word))
                    AdditionalMethods.add_to_buffer("с", f"{nickname}, {resultat[:100]}", ctx.author, "перевод")
            except:
                AdditionalMethods.add_to_buffer("с",
                                                f"{nickname}, неправильно указаны параметры. Ссылка со всеми языками: https://pastebin.com/raw/nk1n1KxD",
                                                ctx.author, "перевод")

    @commands.command(name='курс')
    async def kurs(self, ctx):
        nickname = ctx.author.display_name
        message = ctx.message.clean_content
        if len(message) == 0:
            r = requests.get("https://free.currconv.com/api/v7/convert?q=USD_RUB,EUR_RUB&compact=ultra&apiKey=ee315cc429cbc167d4b7").json()
            r2 = requests.get("https://free.currconv.com/api/v7/convert?q=BTC_RUB,UAH_RUB&compact=ultra&apiKey=ee315cc429cbc167d4b7").json()
            print(r, r2)
            today = (datetime.now() + timedelta(hours=3)).strftime("%d.%m")
            try:
                kurs = f'Курс валют на {today}: USD = {round(r["USD_RUB"], 2)} RUB | EUR = {round(r["EUR_RUB"], 2)} RUB | BTC = {round(r2["BTC_RUB"])} RUB | UAH = {round(r2["UAH_RUB"], 2)} RUB'
                AdditionalMethods.add_to_buffer("с", kurs, ctx.author, "курс")
            except KeyError:
                AdditionalMethods.add_to_buffer("с", f"{nickname}, не удаётся получить курс валют, попробуйте позже Waiting", ctx.author, "курс")
        else:
            try:
                userkurs = message.split()[0]
                count = message.split()[1]
            except:
                AdditionalMethods.add_to_buffer("с", f"{nickname}, введите число PepoG", ctx.author, "курс")
            json_r = requests.get(f"https://free.currconv.com/api/v7/convert?q={userkurs.replace('-', '_')}&compact=ultra&apiKey=ee315cc429cbc167d4b7").json()
            if len(json_r) == 0:
                AdditionalMethods.add_to_buffer("с", f"{nickname}, неправильно введены валюты. Вводите в международном формате (USD-RUB, RUB-JPY)", ctx.author, "курс")
            else:
                try:
                    res = userkurs.replace("-", "_").upper()
                    one = userkurs.split("-")[0]
                    two = userkurs.split("-")[1]
                    AdditionalMethods.add_to_buffer("с", f"{nickname}, {count} {one.upper()} = {round(json_r[res] * float(count), 2)} {two.upper()}", ctx.author, "курс")
                except KeyError:
                    AdditionalMethods.add_to_buffer("с",f"{nickname}, произошла ошибка конвертации. Скорее всего вы неправильно написали валюты. PepoG", ctx.author, "курс")

    @commands.command(name='clipever')
    async def topclipever(self, ctx):
        nickname = ctx.author.display_name
        message = ctx.message.clean_content.replace('@', '')
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(0, message, nickname), ctx.author, "clip")

    @commands.command(name='clipyear')
    async def topclipyear(self, ctx):
        nickname = ctx.author.display_name
        message = ctx.message.clean_content.replace('@', '')
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(365, message, nickname), ctx.author, "clip")

    @commands.command(name='clipweek')
    async def topclipweek(self, ctx):
        nickname = ctx.author.display_name
        message = ctx.message.clean_content.replace('@', '')
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(7, message, nickname), ctx.author, "clip")

    @commands.command(name='clipmonth')
    async def topclipmonth(self, ctx):
        nickname = ctx.author.display_name
        message = ctx.message.clean_content.replace('@', '')
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(30, message, nickname), ctx.author, "clip")

    @commands.command(name='cliptoday')
    async def topclipday(self, ctx):
        nickname = ctx.author.display_name
        message = ctx.message.clean_content.replace('@', '')
        AdditionalMethods.add_to_buffer("c", await AdditionalMethods.gettopclip(1, message, nickname), ctx.author, "clip")

    @commands.command(name='abbreviations')
    async def abbreviations(self, ctx):
        nickname = ctx.author.display_name
        AdditionalMethods.add_to_buffer("c", f"{nickname} Здесь вы можете посмотреть все доступные аббревиатуры для clip {config.abreviationsUrl}",
                                        ctx.author, "abbreviations")

    @commands.command(name='iq')
    async def iq(self, ctx):
        nickname = ctx.author.display_name
        iq = random.randint(40, 190)
        if iq == 110:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, ваш IQ = {str(iq)}! Вы Хесус?! PogU", ctx.author, "iq")
        if iq == 89:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, ваш IQ = {str(iq)}! Вы Братишкин?! PogU", ctx.author,
                                            "iq")
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
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.display_name
            url = "https://zaebalo.ru/?page=" + str(random.randrange(1, 1710, 1))
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'lxml')
            d = soup.find_all('div', align='left')
            res = random.choice(d).get_text()
            res = re.sub(r'\n', '', res)
            with open('data/osujdau2.txt') as f:
                osu = [x for x in f.read().split('\n') if len(x) > 1]
            res_prov = re.sub(r'[^\w ]', '', res)
            for word in res_prov.split():
                for asu in osu:
                    if word.lower().find(asu) != -1:
                        res = res.replace(word, '*' * len(word))
            AdditionalMethods.add_to_buffer("e", f"{nickname}, {res[:150]}", ctx.author, "zaebalo")

    @commands.command(name='pastа')
    async def pasta(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            AdditionalMethods.add_to_buffer("e", AdditionalMethods.parse_simplefile_message("{}", "nadya")[:499], ctx.author, "pastа")

    @commands.command(name='help')
    async def help(self, ctx):
        nickname = ctx.author.display_name
        AdditionalMethods.add_to_buffer("c",
                                        f"catJAM Ку, {nickname}, со списком команд можешь ознакомиться здесь {config.helpUrl} catJAM",
                                        ctx.author, "help")

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
            nickname = ctx.author.display_name
            try:
                chislo = float(ctx.message.clean_content)
                AdditionalMethods.add_to_buffer("s", f"{nickname}, {Settings.change_set(Settings.BUFFERDELAY, chislo)}",
                                                ctx.author, "bufferdelay")
            except:
                AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author,
                                                "bufferdelay")

    @commands.command(name='attentions')
    async def attentions(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.display_name
            try:
                chislo = int(ctx.message.clean_content)
                AdditionalMethods.add_to_buffer("s", f"{nickname}, {Settings.change_set(Settings.ATTENTIONS, chislo)}",
                                                ctx.author,
                                                "attentions")
            except:
                AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author,
                                                "attentions")

    @commands.command(name='mode')
    async def mode(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.display_name
            AdditionalMethods.add_to_buffer("s",
                                            f"{nickname}, {Settings.change_set(Settings.MODE, ctx.message.clean_content)}",
                                            ctx.author,
                                            "mode")

    @commands.command(name='timeout')
    async def timeout(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.display_name
            try:
                chislo = int(ctx.message.clean_content)
                AdditionalMethods.add_to_buffer("s", f"{nickname}, {Settings.change_set(Settings.TIMEOUT, chislo)}",
                                                ctx.author,
                                                "timeout")
            except:
                AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author,
                                                "timeout")

    @commands.command(name='buffermax')
    async def bufermax(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.display_name
            try:
                chislo = int(ctx.message.clean_content)
                AdditionalMethods.add_to_buffer("s", f"{nickname}, {Settings.change_set(Settings.BUFFERMAX, chislo)}",
                                                ctx.author,
                                                "buffermax")
            except:
                AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author,
                                                "buffermax")

    @commands.command(name='entertain')
    async def entertain(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.display_name
            AdditionalMethods.add_to_buffer("s",
                                            f"{nickname}, {Settings.change_set(Settings.ENTERTAIN, int(ctx.message.clean_content))}",
                                            ctx.author,
                                            "entertain")

    @commands.command(name='maxmesses')
    async def maxmesses(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.display_name
            try:
                chislo = int(ctx.message.clean_content)
                AdditionalMethods.add_to_buffer("s", f"{nickname}, {Settings.change_set(Settings.MAXMESSES, chislo)}",
                                                ctx.author,
                                                "maxmesses")
            except:
                AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author,
                                                "maxmesses")

    @commands.command(name='norm')
    async def norm(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.display_name
            try:
                chislo = float(ctx.message.clean_content)
                AdditionalMethods.add_to_buffer("s", f"{nickname}, {Settings.change_set(Settings.NORM, chislo)}",
                                                ctx.author,
                                                "norm")
            except:
                AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author,
                                                "norm")

    @commands.command(name='forget')
    async def forget(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            nickname = ctx.author.display_name
            try:
                chislo = float(ctx.message.clean_content)
                AdditionalMethods.add_to_buffer("s", f"{nickname}, {Settings.change_set(Settings.FORGET, chislo)}",
                                                ctx.author,
                                                "forget")
            except:
                AdditionalMethods.add_to_buffer("s", f"{nickname}, не удалось прочесть число PepoG ", ctx.author,
                                                "forget")

    @commands.command(name='temp')
    async def temp(self, ctx):
        nickname = ctx.author.display_name
        temp = round(random.uniform(25, 45), 1)
        if 35.7 <= temp <= 37:
            AdditionalMethods.add_to_buffer("e",
                                            f"{nickname}, ваша температура {str(temp)} °C! У вас температура в норме "
                                            f"ThumbUp",
                                            ctx.author, "temp")
        elif 37 < temp < 40 or 35.7 > temp >= 32:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, ваша температура {str(temp)} °C! У вас вирус? PepeS",
                                            ctx.author, "temp")
        elif temp > 40 or temp < 32:
            AdditionalMethods.add_to_buffer("e", f"{nickname}, ваша температура {str(temp)} °C! Вызывайте дурку! Durka",
                                            ctx.author, "temp")

    @commands.command(name='me', aliases=['я', 'йа', 'ya'])
    async def me(self, ctx):
        nickname = ctx.author.display_name
        answer = entertain_functions.me(nickname, self.namess)
        AdditionalMethods.add_to_buffer("e", answer, ctx.author, "me")

    @commands.command(name='do')
    async def do(self, ctx):
        message = ctx.message.clean_content.replace('@', '')[:80]
        nickname = ctx.author.display_name
        if len(message) != 0:
            for nick in self.names_exp:
                for word in message.split():
                    if str(word).lower().find(str(nick).lower()) != -1:
                        message = message.replace(word, nick)
            answer = entertain_functions.do(nickname, message, self.namess)
            AdditionalMethods.add_to_buffer("e", answer, ctx.author, "do")

    @commands.command(name='steal')
    async def steal(self, ctx):
        message = ctx.message.clean_content.replace('@', '')[:80]
        nickname = ctx.author.display_name
        if len(message) != 0:
            for nick in self.names_exp:
                for word in message.split():
                    if str(word).lower().find(str(nick).lower()) != -1:
                        message = message.replace(word, nick)
            answer = entertain_functions.steal(nickname, message)
            AdditionalMethods.add_to_buffer("e", answer, ctx.author, "steal")

    @commands.command(name='try')
    async def ttry(self, ctx):
        message = ctx.message.clean_content.replace('@', '')[:80]
        nickname = ctx.author.display_name
        if len(message) != 0:
            for nick in self.names_exp:
                for word in message.split():
                    if str(word).lower().find(str(nick).lower()) != -1:
                        message = message.replace(word, nick)
            result = AdditionalMethods.parse_standartfile_message(nickname, "{nickname} попробовал {messagestr}... {filestr}", message, "!try", "try")
            AdditionalMethods.add_to_buffer("e", result, ctx.author, "try")

    @commands.command(name='время')
    async def time(self, ctx):
        nickname = ctx.author.display_name
        loc = ctx.message.clean_content
        if len(loc) == 0:
            AdditionalMethods.add_to_buffer("c", datetime.strftime(datetime.now() + timedelta(hours=3),
                                                                   f"{nickname}, Чичас %H:%M по МСК Waiting"),
                                            ctx.author, "время")
        else:
            url = "http://search.maps.sputnik.ru/search?q="
            response = requests.get(url + quote(loc))
            if response.text.find('"found":0') != -1:
                AdditionalMethods.add_to_buffer("e", f"{nickname}, не найден населённый пункт. Попробуйте другое название.", ctx.author, "время")
            else:
                try:
                    position = response.json()['result'][0]['position']
                    url = "http://api.timezonedb.com/v2.1/get-time-zone?key=APM2N08MFF2O&format=json&by=position&lat="
                    response1 = requests.get(url + str(position['lat']) + "&lng=" + str(position['lon']))
                    timestamp = response1.json()['timestamp']
                    dt_object = datetime.fromtimestamp(timestamp)
                    date = dt_object.strftime("%H:%M")
                    location = response.json()['result'][0]['title']
                    AdditionalMethods.add_to_buffer("e", f"{nickname}, чичас {date} в «{location}» Waiting", ctx.author, "время")
                except:
                    AdditionalMethods.add_to_buffer("e", f"{nickname}, не удалось найти время для этого населённого пункта", ctx.author, "время")
    
    @commands.command(name='обнять')
    async def hug(self, ctx):
        message = ctx.message.clean_content.replace('@', '')[:80]
        nickname = ctx.author.display_name
        if len(message) != 0:
            for nick in self.names_exp:
                for word in message.split():
                    if str(word).lower().find(str(nick).lower()) != -1:
                        message = message.replace(word, nick)
            result = AdditionalMethods.parse_standartfile_message(nickname, "{nickname} {filestr} обнимает {messagestr} VoHiYo", message, "!обнять", "hug")
            AdditionalMethods.add_to_buffer("e", result, ctx.author, "обнять")

    @commands.command(name='когда')
    async def kogda(self, ctx):
        message = ctx.message.clean_content.replace('@', '')[:80]
        nickname = ctx.author.display_name
        if len(message) != 0:
            for nick in self.names_exp:
                for word in message.split():
                    if str(word).lower().find(str(nick).lower()) != -1:
                        message = message.replace(word, nick)
            result = AdditionalMethods.parse_standartfile_message(nickname, "{nickname}, когда {messagestr}? Thonk {filestr}", message, "!когда", "kogda")
            AdditionalMethods.add_to_buffer("e", result, ctx.author, "когда")

    @commands.command(name='привет')
    async def privet(self, ctx):
        message = ctx.message.clean_content.replace('@', '')[:80]
        nickname = ctx.author.display_name
        if len(message) != 0:
            for nick in self.names_exp:
                for word in message.split():
                    if str(word).lower().find(str(nick).lower()) != -1:
                        message = message.replace(word, nick)
            result = AdditionalMethods.parse_standartfile_message(nickname, "{nickname} {filestr} приветствует {messagestr} peepoHey peepoLove", message, "!привет", "privet")
            AdditionalMethods.add_to_buffer("e", result, ctx.author, "привет")

    @commands.command(name='гороскоп')
    async def goroskop(self, ctx):
        AdditionalMethods.add_to_buffer("s", AdditionalMethods.get_goroskop(ctx.message.content, ctx.author.display_name), ctx.author, "гороскоп")

    @commands.command(name='music')
    async def music(self, ctx):
        try:
            nick = ctx.author.display_name
            message = ctx.message.clean_content.replace('@', '')
            if len(message) != 0:
                mess = message.split()
                emote = mess[len(mess) - 1]
                with open('data/SMILES.txt', encoding='utf-8') as g:
                    list_emotes = json.loads(g.read())
                if emote not in list_emotes and len([c for c in message if c in emoji.UNICODE_EMOJI]) == 0:
                    pass
                else:
                    song_lyric = message.replace(f' {emote}', '')
                    emote = f' {emote} '
                    song = self.genius.search_song(song_lyric).lyrics
                    res = [x for x in song.split('\n') if len(x) > 2]
                    with open('data/Pripev', 'r', encoding='utf-8') as f:
                        pripev = [x for x in f.read().split('\n') if len(x) > 1]
                    flag = False
                    for stroka in res:
                        for strr in stroka.split():
                            for prip in pripev:
                                if stroka.find(f'[{prip}') != -1:
                                    res = res[res.index(stroka)+1:]
                                    flag = True
                                    break
                            if flag:
                                break
                        if flag:
                            break
                    res = [x for x in [re.sub(r'[\[].*?[\]]', '', i) for i in res] if len(x) > 1]
                    res = emote.join(res[:3])
                    with open('data/osujdau2.txt', 'r', encoding='utf-8') as f:
                        osu = [x for x in f.read().split('\n') if len(x) > 1]
                    res_prov = re.sub(r'\W+', ' ', res)
                    for word in res_prov.split():
                        for asu in osu:
                            if word.lower().find(asu) != -1:
                                res = res.replace(word, '*' * len(word))
                    AdditionalMethods.add_to_buffer("e", f'{emote} {res[:180]} {emote}', ctx.author, 'music')
        except AttributeError:
            pass
        except TypeError:
            pass

subprocess.Popen([sys.executable, 'ChatBot.py'])
subprocess.Popen([sys.executable, 'BufferCleaner.py'])
subprocess.Popen([sys.executable, 'CheckingStreamThread.py'])
bot = CommandsBot()
bot.run()
