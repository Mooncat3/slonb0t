from twitchio.ext import commands
import asyncio


class stream(commands.Bot):
    def __init__(self):
        super().__init__(irc_token='oauth:14y5qalllj1i65rg3m9dip1rpq5ugd',
                         client_id="gp762nuuoqcoxypju8c569th9wz7q5", nick="SLONB0T", prefix='!',
                         initial_channels=['jesusavgn'])

    async def event_ready(self):
        self.one = open('1.txt', encoding='utf-8').read().split('\n')
        self.two = open('2.txt', encoding='utf-8').read().split('\n')
        self.three = open('3.txt', encoding='utf-8').read().split('\n')
        self.four = open('4.txt', encoding='utf-8').read().split('\n')
        print('Бот запущен!')

    async def event_command_error(self, ctx, error):
        pass

    async def event_message(self, ctx):
        mess_orig = ctx.content
        mess = mess_orig.lower()
        nick = ctx.author.name
        nick_dis = ctx.author.display_name
        send = ctx.channel.send
        
        word = f"{nick_dis}, стримов в ближающую неделю не будет. Вся информация в телеграм-канале - https://t.me/jesusavgntwitch FeelsBadMan"

        if nick == 'slonb0t' or nick == 'moobot' or mess[0] == '!' or len(mess) > 100 or nick == 'kryabot':
            pass
        elif any(mess.find(x) != -1 for x in self.four):
            print(mess_orig, '| СПИСОК | 1')
            if any(mess.find(x) != -1 for x in self.one):
                print(mess_orig, '| СПИСОК | 2 |', 'Отправлено!')
                await send(word)
        elif any(mess.find(x) != -1 for x in self.one):
            print(mess_orig, '| 1')
            if any(mess.find(x) != -1 for x in self.two):
                print(mess_orig, '| 2')
                if any(mess.find(x) != -1 for x in self.three):
                    print(mess_orig, '| 3 | Отправлено!')
                    await send(word)
        await bot.handle_commands(ctx)

bot = stream()
bot.run()
