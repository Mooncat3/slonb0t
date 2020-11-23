from twitchio.ext import commands


with open('1.txt', 'r', encoding='utf_8') as t:
    global one
    one = t.read().split('\n')
    
with open('2.txt', 'r', encoding='utf_8') as j:
    global two
    two = j.read().split('\n')
    
with open('3.txt', 'r', encoding='utf_8') as k:
    global three
    three = k.read().split('\n')
    
with open('4.txt', 'r', encoding='utf_8') as nn:
    global four
    four = nn.read().split('\n')

bot = commands.Bot(
        irc_token='oauth:14y5qalllj1i65rg3m9dip1rpq5ugd',
        nick='SLONB0T',
        prefix='&',
        initial_channels=['mooncat3'])

@bot.event
async def event_ready():
    print("Бот запущен!")

@bot.event
async def event_message(ctx):
    mess = ctx.content.lower()
    nick = ctx.author.name
    
    word = ctx.author.display_name+", стримов в ближающую неделю не будет. Вся информация в телеграм-канале - https://t.me/jesusavgntwitch FeelsBadMan"

    if nick == 'slonb0t' or nick == 'moobot':
        pass
    else:
        if mess[0] == '!':
            pass
        elif len(mess) < 80:
            if any(mess.find(x) != -1 for x in four):
                print(mess, '| из списка |', '1')
                if any(mess.find(x) != -1 for x in one):
                    print(mess, '| из списка |', 'Отправлено')
                    await ctx.channel.send(word)
            else:
                if any(mess.find(x) != -1 for x in one):
                    print(mess, '1')
                    if any(mess.find(x) != -1 for x in two):
                        print(mess, '2')
                        if any(mess.find(x) != -1 for x in three):
                            print(mess, 'Отправлено')
                            await ctx.channel.send(word)
    await bot.handle_commands(ctx)

bot.run()
