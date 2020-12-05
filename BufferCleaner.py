import uuid
from abc import ABC
from twitchioc import Client
import asyncio
import AdditionalMethods
import Settings
import config
import json
import time

from twitchioc.websocket import WebsocketConnection


def parse_kd_comand(kd: dict, cmd: str):
    if cmd in kd.keys():
        return kd[cmd]
    else:
        return 0

class BufferCleaner(Client, ABC):

    def __init__(self):
        super().__init__(irc_token=f'oauth:{config.OAUTH}',
                         client_id=config.CLIENT_ID, api_token=config.OAUTH)
        self._ws = WebsocketConnection(bot=self, loop=self.loop, http=self.http, irc_token=f'oauth:{config.OAUTH}',
                                       nick=config.BOT, initial_channels=config.CHANNELS)
        self.loop.create_task(self.listen_to_buffer_delaied())
        self.loop.create_task(self.listen_to_buffer_undelaied())
        self.messes = []
        self.times = {}
        self.kd = {"porf": 15, "когда": 15, "анекдот": 15, "iq": 15, "me": 15, "do": 15, "кто": 15, "steal": 15, "try": 15, "обнять": 5, "kogda": 15, "привет": 15}
        for r in self.kd.keys():
            if not r in self.times.keys():
                self.times[str(self.kd[r])] = 0
        self.times['0'] = 0

    async def event_webhook(self, data):
        pass

    async def event_raw_pubsub(self, data):
        pass

    async def event_pubsub(self, data):
        raise NotImplementedError

    async def pubsub_subscribe(self, token: str, *topics):
        nonce = uuid.uuid4().hex

        connection = await self._ws.pubsub_pool.delegate(*topics)
        await connection.subscribe(token, nonce, *topics)

        return nonce

    async def event_command_error(self, ctx, error):
        pass

    async def event_mode(self, channel, user, status):
        pass

    async def event_userstate(self, user):
        pass

    async def event_raw_usernotice(self, channel, tags: dict):
        pass

    async def event_usernotice_subscription(self, metadata):
        pass

    async def event_part(self, user):
        pass

    async def event_join(self, user):
        pass

    async def event_message(self, message):
        pass

    async def event_error(self, error: Exception, data=None):
        pass

    async def event_ready(self):
        print(f'Ready {str(self.__class__.__name__)} | {config.BOT} on {config.CHANNELS[0]}')
        pass

    async def event_raw_data(self, data):
        pass

    def run(self):
        loop = self.loop or asyncio.get_event_loop()

        loop.run_until_complete(self._ws._connect())

        try:
            loop.run_until_complete(self._ws._listen())
        except KeyboardInterrupt:
            pass
        finally:
            self._ws.teardown()

    async def start(self):
        await self._ws._connect()

        try:
            await self._ws._listen()
        except KeyboardInterrupt:
            pass
        finally:
            self._ws.teardown()

    async def listen_to_buffer_undelaied(self):
        recepttime = 0.0
        ondeleting = []
        dopbol = True
        while True:
            async def send_mess(sock, resert, rest):
                mess = str(resert['mes'])
                while sock._websocket is None:
                    await asyncio.sleep(0.1)
                print(str(parse_kd_comand(self.kd, res['command'])))
                print(self.times)
                if rest['vip'] and rest['type'] != "s":
                    await sock.send_privmsg(config.CHAN, mess)
                elif rest['type'] == "s" or x - excluding >= Settings.get_bufer_max() or time.time() - self.times[str(parse_kd_comand(self.kd, res['command']))] < parse_kd_comand(self.kd, res['command']):
                    await sock.send_privmsg(config.CHAN, f"/w {rest['nickname']} !{resert['cmd']} ▶ {mess}")
                else:
                    pass
            await asyncio.sleep(0.2)
            with open(file='data/buffer.txt', mode='r', encoding='utf-8') as e:
                try:
                    dat = json.loads(e.read())
                except:
                    dat = []
                if len(dat) > 0:
                    excluding = 0
                    for x in range(0, len(dat)):
                        res = dat[x]
                        if res['vip'] or res['type'] == "s":
                            excluding += 1
                        if res['vip'] or res['type'] == "s" or x - excluding >= Settings.get_bufer_max() or (time.time() - self.times[str(parse_kd_comand(self.kd, res['command']))] < parse_kd_comand(self.kd, res['command']) and time.time() - self.times[str(parse_kd_comand(self.kd, res['command']))] > 0.5):
                            ondeleting.append(res)
                            if res['type'] != "r":
                                reser = {"mes": res['message'], "cmd": res['command'], "timeout": 0.0}
                                await send_mess(self._ws, reser, res)
                            elif res['type'] == "r":
                                if time.time() - recepttime > 20:
                                    if dopbol:
                                        dopbol = False
                                        reser = {"mes": res['message'], "cmd": res['command'], "timeout": 0.0}
                                        await send_mess(self._ws, reser, res)
                                    else:
                                        dopbol = True
                                        reser = {"mes": res['message'], "cmd": res['command'], "timeout": 2.0}
                                        recepttime = time.time()
                                        await send_mess(self._ws, reser, res)
            if len(ondeleting) > 0:
                while config.buferchanged:
                    await asyncio.sleep(0.1)
                config.buferchanged = True
                with open(file='data/buffer.txt', mode='r', encoding='utf-8') as e:
                    dat = json.loads(e.read())
                    for delet in ondeleting:
                        dat.remove(delet)
                    ondeleting = []
                with open(file='data/buffer.txt', mode='w', encoding='utf-8') as q:
                    if len(dat) == 0:
                        q.write("[]")
                    else:
                        q.write(json.dumps(dat))
                config.buferchanged = False

    async def listen_to_buffer_delaied(self):
        tttime = time.time()
        timer = 0.0
        recepttime = 0.0
        ondeleting = []
        dopbol = True
        while True:
            async def send_mess(sock, resert, rest):
                mess = resert['mes']
                while sock._websocket is None:
                    await asyncio.sleep(0.1)
                if rest['type'] == "e" or rest['type'] == "r":
                    if not AdditionalMethods.check_active():
                        await asyncio.sleep(resert['timeout'])
                        dat.remove(rest)
                        await sock.send_privmsg(config.CHAN, mess)
                    else:
                        await sock.send_privmsg(config.CHAN, f"/w {rest['nickname']} !{resert['cmd']} ▶ На данный момент идёт стрим, либо развлекательные команды отключены!")
                elif rest['type'] == "r":
                    await asyncio.sleep(resert['timeout'])
                    dat.remove(rest)
                    await sock.send_privmsg(config.CHAN, mess)
                else:
                    await asyncio.sleep(resert['timeout'])
                    dat.remove(rest)
                    await sock.send_privmsg(config.CHAN, mess)
            await asyncio.sleep(0.2)
            if time.time() - (tttime + timer) > Settings.get_bufer_timeout():
                tttime = time.time()
                timer = 0.0
            with open(file='data/buffer.txt', mode='r', encoding='utf-8') as e:
                try:
                    dat = json.loads(e.read())
                except:
                    dat = []
                if len(dat) > 0:
                    while len(dat) > Settings.get_bufer_max():
                        await asyncio.sleep(0.2)
                        with open(file='data/buffer.txt', mode='r', encoding='utf-8') as e:
                            try:
                                dat = json.loads(e.read())
                            except:
                                dat = []
                    if len(dat) > 0:
                        res = dat[0]
                        print(str(parse_kd_comand(self.kd, res['command'])))
                        print(self.times)
                        if not res['vip'] and res['type'] != "s" and time.time() - self.times[str(parse_kd_comand(self.kd, res['command']))] > parse_kd_comand(self.kd, res['command']):
                            self.times[str(parse_kd_comand(self.kd, res['command']))] = time.time()
                            ondeleting.append(res)
                            if res['type'] != "r":
                                reser = {"timeout": timer, "mes": res['message'], "cmd": res['command']}
                                timer = Settings.get_bufer_timeout()
                                tttime = time.time()
                                await send_mess(self._ws, reser, res)
                            else:
                                if time.time() - recepttime > 20:
                                    if dopbol:
                                        dopbol = False
                                        reser = {"timeout": timer, "mes": res['message'], "cmd": res['command']}
                                        timer = Settings.get_bufer_timeout()
                                        tttime = time.time()
                                        await send_mess(self._ws, reser, res)
                                    else:
                                        dopbol = True
                                        timer = 2.0
                                        reser = {"timeout": timer, "mes": res['message'], "cmd": res['command']}
                                        tttime = time.time()
                                        recepttime = time.time()
                                        await send_mess(self._ws, reser, res)
            if len(ondeleting) > 0:
                while config.buferchanged:
                    await asyncio.sleep(0.1)
                config.buferchanged = True
                with open(file='data/buffer.txt', mode='r', encoding='utf-8') as e:
                    dat = json.loads(e.read())
                    for delet in ondeleting:
                        dat.remove(delet)
                    ondeleting = []
                with open(file='data/buffer.txt', mode='w', encoding='utf-8') as q:
                    if len(dat) == 0:
                        q.write("[]")
                    else:
                        q.write(json.dumps(dat))
                config.buferchanged = False


bot = BufferCleaner()
bot.run()
