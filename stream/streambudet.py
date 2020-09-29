from twitchio.ext import commands


with open('1.txt', 'r', encoding='utf_8') as t:
    global one
    one = [line.strip() for line in t]
    
with open('2.txt', 'r', encoding='utf_8') as j:
    global two
    two = [line.strip() for line in j]
    
with open('3.txt', 'r', encoding='utf_8') as k:
    global three
    three = [line.strip() for line in k]
    
    
bot = commands.Bot(
        irc_token='oauth:14y5qalllj1i65rg3m9dip1rpq5ugd',
        nick='SLONB0T',
        prefix='&',
        initial_channels=['jesusavgn'])

@bot.event
async def event_ready():
    print("Бот запущен!")

@bot.event
async def event_message(ctx):
    mess = ctx.content.lower()
    if any(x in mess for x in one):
        if any(x in mess for x in two):
            if any(x in mess for x in three):
                await ctx.channel.send(ctx.author.name+", стрима сегодня не будет. Вся инфа в телеге - https://t.me/jesusavgntwitch PunOko")
    await bot.handle_commands(ctx)
            
bot.run()
