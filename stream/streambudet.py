from twitchio.ext import commands


with open('1.txt', 'r', encoding='utf_8') as t:
    global one
    one = list(set(t.read().split('\n')))
    
with open('2.txt', 'r', encoding='utf_8') as j:
    global two
    two = list(set(j.read().split('\n')))
    
with open('3.txt', 'r', encoding='utf_8') as k:
    global three
    three = list(set(k.read().split('\n')))
print(one, two, three)
bot = commands.Bot(
        irc_token='oauth:14y5qalllj1i65rg3m9dip1rpq5ugd',
        nick='SLONB0T',
        prefix='&',
        initial_channels=['jesusavgn'])

@bot.event
async def event_ready():
    global i
    i=0
    print("Бот запущен!")

@bot.event
async def event_message(ctx):
    global i
    mess = ctx.content.lower()
    nick = ctx.author.name
    if nick == 'slonb0t' or nick == 'moobot':
        pass
    else:
        if mess.find('!') != -1:
            pass
        else:
            if any(mess.find(x) != -1 for x in one):
                if any(mess.find(x) != -1 for x in two):
                    if any(mess.find(x) != -1 for x in three):
                        #await ctx.channel.send(ctx.author.display_name+", стрима сегодня не будет. Вся инфа в телеге - https://t.me/jesusavgntwitch PunOko")
                        await ctx.channel.send(ctx.author.display_name+", стрима сегодня не будет FeelsBadMan")
                        i += 1
                        print(i, end='\r')
    await bot.handle_commands(ctx)
            
bot.run()
