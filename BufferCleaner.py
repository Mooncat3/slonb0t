import sys
import traceback
import uuid
from abc import ABC
from twitchioc import Client
import asyncio

import AdditionalMethods
import config
import json
import time

from twitchioc.websocket import WebsocketConnection


class BufferCleaner(Client, ABC):

    def __init__(self):
        super().__init__(irc_token=f'oauth:{config.OAUTH}',
                         client_id=config.CLIENT_ID, api_token=config.OAUTH)
        self._ws = WebsocketConnection(bot=self, loop=self.loop, http=self.http, irc_token=f'oauth:{config.OAUTH}',
                                       nick=config.BOT, initial_channels=config.CHANNELS)
        self.loop.create_task(self.listen_to_buffer())


    async def event_webhook(self, data):
        pass

    async def event_raw_pubsub(self, data):
        pass

    async def event_pubsub(self, data):
        raise NotImplementedError

    async def pubsub_subscribe(self, token: str, *topics):
        nonce = uuid.uuid4().hex

        connection = await self._ws._pubsub_pool.delegate(*topics)
        await connection.subscribe(token, nonce, *topics)

        return nonce

    async def event_command_error(self, ctx, error):
        print('Ignoring exception in command: {0}:'.format(error), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

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
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    async def event_ready(self):
        print(f'Ready {str(self.__class__.__name__)} | {self._ws.nick} on {self._ws._initial_channels}')
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

    async def listen_to_buffer(self):
        tttime = 0.0
        timer = 0.0
        users = {}
        reser = {}
        ondeleting = []
        buffercols = 0
        ifbadtimes = False
        while True:
            await asyncio.sleep(0.1)
            if time.time() - (tttime + timer) > 5:
                tttime = time.time()
                timer = 0.0
                recept = False
            with open(file='data/buffer.txt', mode='r', encoding='utf-8') as e:
                try:
                    dat = json.loads(e.read())
                except:
                    dat = []
                if len(dat) > 0:
                    for res in dat:
                        buffercols += 1
                        ondeleting.append(res)
                        if res['nickname'] in users and not res['vip']:
                            if time.time() - users[res['nickname']]['time'] < AdditionalMethods.get_user_timeout() and res['type'] != "r":
                                users[res['nickname']]['time'] = time.time()
                                if not users[res['nickname']]['got']:
                                    users[res['nickname']]['got'] = True
                                    timer = AdditionalMethods.get_bufer_timeout()
                                    tttime = time.time()
                                    reser = {"timeout": 0.0, "mes": "{} WeirdChamp STOP SPAM".format(res['nickname'])}
                                ifbadtimes = True
                            else:
                                users[res['nickname']] = {"time": time.time(), "got": False}
                                if res['type'] != "r":
                                    reser = {"timeout": timer, "mes": res['message']}
                                    timer = AdditionalMethods.get_bufer_timeout()
                                    tttime = time.time()
                                else:
                                    if not recept:
                                        if dopbol:
                                            dopbol = False
                                            reser = {"timeout": timer, "mes": res['message']}
                                            timer = AdditionalMethods.get_bufer_timeout()
                                            tttime = time.time()
                                        else:
                                            recept = True
                                            dopbol = True
                                            reser = {"timeout": timer, "mes": res['message']}
                                            timer = AdditionalMethods.get_bufer_timeout() + 2.0
                                            tttime = time.time()
                        else:
                            users[res['nickname']] = {"time": time.time(), "got": False}
                            if res['type'] != "r":
                                reser = {"timeout": timer, "mes": res['message']}
                                timer = AdditionalMethods.get_bufer_timeout()
                                tttime = time.time()
                            else:
                                if not recept:
                                    if dopbol:
                                        dopbol = False
                                        reser = {"timeout": timer, "mes": res['message']}
                                        timer = AdditionalMethods.get_bufer_timeout()
                                        tttime = time.time()
                                    else:
                                        recept = True
                                        dopbol = True
                                        reser = {"timeout": timer, "mes": res['message']}
                                        timer = AdditionalMethods.get_bufer_timeout() + 2.0
                                        tttime = time.time()
                        mess = reser['mes']
                        while self._ws._websocket is None:
                            await asyncio.sleep(1)
                        if res['type'] == "e":
                            if not AdditionalMethods.check_active() or res['vip']:
                                if (len(dat) > AdditionalMethods.get_bufer_max() and not res['vip']) or ifbadtimes:
                                    ifbadtimes = False
                                    await self._ws.send_privmsg(config.CHAN, f"/w {res['nickname']} {mess}")
                                else:
                                    await asyncio.sleep(reser['timeout'])
                                    dat.remove(res)
                                    await self._ws.send_privmsg(config.CHAN, mess)
                        else:
                            if (len(dat) > AdditionalMethods.get_bufer_max() and not res['vip']) or res['type'] == "s" or ifbadtimes:
                                ifbadtimes = False
                                await self._ws.send_privmsg(config.CHAN, f"/w {res['nickname']} {mess}")
                            else:
                                await asyncio.sleep(reser['timeout'])
                                dat.remove(res)
                                await self._ws.send_privmsg(config.CHAN, mess)
            if len(ondeleting) > 0:
                while config.buferchanged:
                    await asyncio.sleep(0.1)
                with open(file='data/buffer.txt', mode='r', encoding='utf-8') as e:
                    dat = json.loads(e.read())
                    for delet in ondeleting:
                        dat.remove(delet)
                    ondeleting = []
                config.buferchanged = True
                with open(file='data/buffer.txt', mode='w', encoding='utf-8') as q:
                    if len(dat) == 0:
                        q.write("[]")
                    else:
                        q.write(json.dumps(dat))
                config.buferchanged = False


bot = BufferCleaner()
bot.run()