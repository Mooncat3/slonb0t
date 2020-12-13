import sys
import subprocess
import config
from abc import ABC
from twitchioc.ext import commands
import AdditionalMethods
import random
import json
import asyncio


class CommandsBot(commands.Bot, ABC):

    def __init__(self):
        super().__init__(irc_token=f'oauth:{config.OAUTH}',
                         client_id=config.CLIENT_ID, nick=config.BOT, prefix='!',
                         initial_channels=config.CHANNELS)
        self.json_bal = {}
        self.roulette_is_running = False
        self.roulette_nicknames = []
        self.name_cur = 'поинтов'
        self.black = []
        self.red = []
        self.yellow = []
        self.green = []

    # async def event_command_error(self, ctx, error):
    # pass

    async def event_ready(self):
        print(f'Ready {str(self.__class__.__name__)} | {self.nick} on {self.initial_channels[0]}')

    async def rand(self, socket):
        await asyncio.sleep(30)
        if len(self.roulette_nicknames) < 2:
            if len(self.roulette_nicknames) == 1:
                self.add_points(self.roulette_nicknames[0][0], self.roulette_nicknames[0][1])
            await socket.send_privmsg(config.CHAN, "Никто не участвует, ну и ладно Happy")
        else:
            koef = 0
            res_list = []
            result = ''
            v = random.randint(0, 100)
            if 0 < v <= 50:
                result = 'чёрное'
                koef = 2
                res_list = self.black
            if 50 < v <= 80:
                result = 'жёлтое'
                koef = 3
                res_list = self.yellow
            if 80 < v <= 95:
                result = 'красное'
                koef = 5
                res_list = self.red
            if 95 < v <= 100:
                result = 'зелёное'
                koef = 50
                res_list = self.green
            for names in res_list:
                self.add_points(names['nick'], names['count'] * koef)
            winners = [user['nick'] for user in res_list]
            if len(winners) != 0:
                winners = (', '.join(winners)) + ' peepoClap'
            else:
                winners = 'нет победителей Sadge'
            await socket.send_privmsg(config.CHAN,
                                      f"Выпадает {result} (x{koef}) | Победители: {winners}")
        self.roulette_nicknames.clear()
        self.roulette_is_running = False
        self.black.clear()
        self.red.clear()
        self.yellow.clear()
        self.green.clear()

    async def event_message(self, ctx):
        self.json_bal = json.loads(open('money.json').read())
        self.add_points(ctx.author.display_name, len(ctx.content)//2)
        await self.handle_commands(ctx)

    def minus(self, nick, count):
        with open('money.json', 'w') as f:
            self.json_bal[nick] -= count
            json.dump(self.json_bal, f)
        return self.json_bal[nick]

    def plus(self, nick, count):
        with open('money.json', 'w') as f:
            self.json_bal[nick] += count
            json.dump(self.json_bal, f)
        return self.json_bal[nick]

    def add_user(self, nick, count):
        with open('money.json', 'w') as f:
            self.json_bal.update({nick: count})
            json.dump(self.json_bal, f)

    def tran(self, nick, nick_2, count):
        if count < 0 or self.check_balance(nick) < count:
            return False
        if (nick in self.json_bal and nick_2 in self.json_bal) or nick_2 not in self.json_bal:
            self.delete_points(nick, count)
            self.add_points(nick_2, count)
        return self.json_bal[nick]

    def delete_points(self, nick, count):
        if nick in self.json_bal:
            return self.minus(nick, count)

    def add_points(self, nick, count):
        if nick in self.json_bal:
            return self.plus(nick, count)
        else:
            self.add_user(nick, count)

    def check_balance(self, nick):
        if nick in self.json_bal:
            return self.json_bal[nick]
        else:
            return 0

    @commands.command(name='add')
    async def add(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            s = ctx.message.clean_content.split()
            self.add_points(s[0], int(s[1]))

    @commands.command(name='delete')
    async def delete(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            s = ctx.message.clean_content.split()
            self.delete_points(s[0], int(s[1]))

    @commands.command(name='перевести')
    async def perevod(self, ctx):
        nickname = ctx.author.display_name
        mess = ctx.message.clean_content.replace('@', '').split()
        t = self.tran(nickname, mess[0], int(mess[-1]))
        if not t:
            AdditionalMethods.add_to_buffer("s",
                                            f'{ctx.author.display_name}, недостаточно {self.name_cur} для перевода или '
                                            f'введено число меньше нуля',
                                            ctx.author, "перевести")
        else:
            AdditionalMethods.add_to_buffer("s",
                                            f'{ctx.author.display_name} перевёл {mess[0]} {mess[-1]} {self.name_cur}',
                                            ctx.author, "перевести")

    @commands.command(name='баланс')
    async def balance(self, ctx):
        nickname = ctx.author.display_name
        mess = ctx.message.clean_content.replace('@', '')
        if len(mess) != 0:
            nickname = mess
        check = self.check_balance(nickname)
        AdditionalMethods.add_to_buffer("s",
                                        f'Баланс {nickname}: {check} {self.name_cur}',
                                        ctx.author, "баланс")

    @commands.command(name='казино')
    async def casino(self, ctx):
        nick = ctx.author.display_name
        mess = int(ctx.message.clean_content.replace('@', ''))
        t = [('чёрное', 2), ('красное', 5), ('зелёное', 50), ('жёлтое', 3)]
        casino_result = random.choice(t)
        casino_result_2 = random.choice(t)
        if self.check_balance(nick) >= mess > 0:
            self.delete_points(nick, mess)
            if casino_result_2[0] == casino_result[0]:
                koef = casino_result_2[1]
                AdditionalMethods.add_to_buffer("e",
                                                f'{nick} поставил на {casino_result[0]}, выпало {casino_result_2[0]}, '
                                                f'выигрыш: {round(mess * koef) - mess} PogU',
                                                ctx.author, "казино")
                self.add_points(nick, mess * koef)
            else:
                '''
                AdditionalMethods.add_to_buffer("s",
                                                f'{nick} поставил на {casino_result[0]}, выпало {casino_result_2[0]} '
                                                f'Lohich',
                                                ctx.author, "казино")
                '''
                pass
        else:
            AdditionalMethods.add_to_buffer("e",
                                            f'{nick}, недостаточно {self.name_cur} Sadge',
                                            ctx.author, "казино")

    @commands.command(name='roulettepoints')
    async def roulette(self, ctx):
        self.roulette_is_running = True
        AdditionalMethods.add_to_buffer("e",
                                        "Рулетка началась! У вас есть 20 секунд! Чтобы сделать ставку, введите "
                                        "!bet на (чёрное, жёлтое, красное, зелёное) (сумма)",
                                        ctx.author, "roulettepoints")
        asyncio.get_event_loop().create_task(self.rand(self._ws))

    @commands.command(name='bet')
    async def bet(self, ctx):
        mess = ctx.message.clean_content.replace('ё', 'е')
        nick = ctx.author.display_name
        stavka_num = int(mess.split()[-1])
        stavka_word = mess.replace(f' {stavka_num}', '')
        b = self.check_balance(nick)
        if 0 < stavka_num <= b and self.roulette_is_running and (nick, stavka_num) not in self.roulette_nicknames:
            if stavka_word == 'на черное':
                self.black.append({'nick': nick, 'count': stavka_num})
            if stavka_word == 'на желтое':
                self.yellow.append({'nick': nick, 'count': stavka_num})
            if stavka_word == 'на красное':
                self.red.append({'nick': nick, 'count': stavka_num})
            if stavka_word == 'на зеленое':
                self.green.append({'nick': nick, 'count': stavka_num})
            self.delete_points(nick, stavka_num)
            self.roulette_nicknames.append((nick, stavka_num))


subprocess.Popen([sys.executable, 'BufferCleaner.py'])
bot = CommandsBot()
bot.run()
