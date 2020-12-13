import sys
import subprocess
import config
from abc import ABC
from twitchioc.ext import commands
import AdditionalMethods
import random
from collections import Counter
import json
import asyncio


class CommandsBot(commands.Bot, ABC):

    def __init__(self):
        super().__init__(irc_token=f'oauth:{config.OAUTH}',
                         client_id=config.CLIENT_ID, nick=config.BOT, prefix='!',
                         initial_channels=config.CHANNELS)
        self.smiles_is_running = False
        self.json_bal = {}
        self.smiles_nicknames = []
        self.name_cur = 'поинтов'
        self.smiles_list = json.loads(open('SMILES.txt').read())

    async def event_command_error(self, ctx, error):
        pass

    async def event_ready(self):
        print(f'Ready {str(self.__class__.__name__)} | {self.nick} on {self.initial_channels[0]}')

    async def event_message(self, ctx):
        self.json_bal = json.loads(open('money.json').read())
        self.add_points(ctx.author.display_name, len(ctx.content) // 2)
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

    @commands.command(name='transit')
    async def perevod(self, ctx):
        nickname = ctx.author.display_name
        mess = ctx.message.clean_content.replace('@', '').split()
        if len(mess) == 0:
            AdditionalMethods.add_to_buffer("s", f'{ctx.author.display_name}, введите !transit [nickname] [points]',
                                            ctx.author, "transit")
        elif not self.tran(nickname, mess[0], int(mess[-1])):
            AdditionalMethods.add_to_buffer("s", f'{ctx.author.display_name}, недостаточно {self.name_cur} для '
                                            f'перевода или введено число меньше нуля', ctx.author, "transit")
        else:
            AdditionalMethods.add_to_buffer("s", f'{ctx.author.display_name} перевёл {mess[0]} {mess[-1]} '
                                            f'{self.name_cur}', ctx.author, "transit")

    '''
    @commands.command(name='points')
    async def balance(self, ctx):
        nickname = ctx.author.display_name
        mess = ctx.message.clean_content.replace('@', '')
        if len(mess) != 0:
            nickname = mess
        check = self.check_balance(nickname)
        AdditionalMethods.add_to_buffer("s", f'Баланс {nickname}: {check} {self.name_cur}', ctx.author, "points")

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
                                                f'{nick} поставил {mess} на {casino_result[0]} (x{koef}), '
                                                f'выпало {casino_result_2[0]}, '
                                                f'выигрыш: {round(mess * koef) - mess} PogU', ctx.author, "казино")
                self.add_points(nick, mess * koef)
        else:
            AdditionalMethods.add_to_buffer("e",
                                            f'{nick}, недостаточно {self.name_cur} Sadge',
                                            ctx.author, "казино")
    '''

    @commands.command(name='bet')
    async def bet(self, ctx):
        nick = ctx.author.display_name
        if self.smiles_is_running:
            mess = ctx.message.clean_content
            mess_split = mess.split()
            count = mess_split[-1]
            smiles_user = mess.replace(f' {count}', '').split()
            if self.check_balance(nick) >= int(count) > 0 and len(smiles_user) < 4:
                coefficient = 5 / len(smiles_user)
                self.delete_points(nick, int(count))
                self.smiles_nicknames.append({'nick': nick, 'smiles': smiles_user,
                                              'count': int(count), 'coeff': coefficient})

    async def rand(self, socket):
        await asyncio.sleep(30)
        print('-' * 50)
        s = socket.send_privmsg
        if len(self.smiles_nicknames) < 2:
            if len(self.smiles_nicknames) == 1:
                self.add_points(self.smiles_nicknames[0]['nick'], self.smiles_nicknames[0]['count'])
            await s(config.CHAN, "Никто не участвует, ну и ладно Happy")
        else:
            winners = []
            smiles_result = random.sample(self.smiles_list, 3)
            for user in self.smiles_nicknames:
                i = 0
                for smile in user['smiles']:
                    for smile_2 in smiles_result:
                        if smile == smile_2:
                            i += user['coeff']
                res = round(user['count'] * i)
                print(user['nick'], res)
                self.add_points(user['nick'], res)
                if res != 0:
                    winners.append(user['nick'] + f' (x{round(i, 2)})')
                    await s(config.CHAN, f"/w {user['nick']} Вы выиграли {res} {self.name_cur}!"
                                         f" | Ваш баланс: {self.check_balance(user['nick'])}")
            if len(winners) != 0:
                win_res = (', '.join(winners)) + ' peepoClap'
            else:
                win_res = 'нет победителей'
            await socket.send_privmsg(config.CHAN, f'Выпало:  {" ".join(smiles_result)} Победители: {win_res}')
            self.smiles_nicknames.clear()
            self.smiles_is_running = False

    @commands.command(name='casinosmiles')
    async def casinosmiles(self, ctx):
        if AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
            self.smiles_is_running = True
            AdditionalMethods.add_to_buffer("e", "Рулетка смаилов началась! Чтобы сделать ставку, введите "
                                                 "!bet (1-3 FFZ смаила) (сумма)", ctx.author, "casinosmiles")
            asyncio.get_event_loop().create_task(self.rand(self._ws))

    @commands.command(name='points')
    async def points(self, ctx):
        nick = ctx.author.display_name
        if ctx.message.clean_content == 'top':
            top = Counter(self.json_bal).most_common(5)
            res = str(top).replace("[('", "").replace(")]", "]").replace("), ('", "], ").replace("', ", " [")
            AdditionalMethods.add_to_buffer("e", f'{nick}, топ 5 пользователей по поинтам: {res}',
                                            ctx.author, "pointstop")
        else:
            nickname = ctx.author.display_name
            mess = ctx.message.clean_content.replace('@', '')
            if len(mess) != 0:
                nickname = mess
            check = self.check_balance(nickname)
            AdditionalMethods.add_to_buffer("s", f'Баланс {nickname}: {check} {self.name_cur}', ctx.author, "points")


subprocess.Popen([sys.executable, 'BufferCleaner.py'])
bot = CommandsBot()
bot.run()
