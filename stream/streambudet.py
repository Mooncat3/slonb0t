from twitchio.ext import commands
from abc import ABC
import asyncio


class CommandsBot(commands.Bot, ABC):
    def __init__(self):
        super().__init__(irc_token='oauth:14y5qalllj1i65rg3m9dip1rpq5ugd',
                         client_id="gp762nuuoqcoxypju8c569th9wz7q5", nick="SLONB0T", prefix='!',
                         initial_channels=['mooncat3'])
                         
    async def event_ready(self):
        with open('1.txt', encoding='utf-8') as t:
            self.one = t.read().split('\n')
        with open('2.txt', encoding='utf-8') as j:
            self.two = j.read().split('\n')
        with open('3.txt', encoding='utf-8') as k:
            self.three = k.read().split('\n')
        with open('4.txt', encoding='utf-8') as nn:
            self.four = nn.read().split('\n')
        print('Бот запущен!')


    async def event_message(self, ctx):
        mess = ctx.content.lower()
        nick = ctx.author.name
        
        word = ctx.author.display_name+", стримов в ближающую неделю не будет. Вся информация в телеграм-канале - https://t.me/jesusavgntwitch FeelsBadMan"

        if nick == 'slonb0t' or nick == 'moobot':
            pass
        else:
            if mess[0] == '!':
                pass
            elif len(mess) < 80:
                if any(mess.find(x) != -1 for x in self.four):
                    print(mess, '| из списка |', '1')
                    if any(mess.find(x) != -1 for x in self.one):
                        print(mess, '| из списка |', 'Отправлено')
                        await ctx.channel.send(word)
                else:
                    if any(mess.find(x) != -1 for x in self.one):
                        print(mess, '1')
                        if any(mess.find(x) != -1 for x in self.two):
                            print(mess, '2')
                            if any(mess.find(x) != -1 for x in self.three):
                                print(mess, 'Отправлено')
                                await ctx.channel.send(word)
        await bot.handle_commands(ctx)

bot = CommandsBot()
bot.run()
