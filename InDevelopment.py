"""
@commands.command(name='игры')
async def hug(self, ctx):
nickname = ctx.author.name
s = ctx.send
await s(nickname + ", cписок всех мини-игр у бота: +угадать число")


@commands.command(name='угадать число')
async def chislo(self, ctx):
nickname = ctx.author.name
s = ctx.send
await s("Правила: бот загадывает число от 0 до 20. Ваша задача угадать это число. У вас есть минута. Pog нали!")
number = random.randrange(0, 20, 1)
for i in range(600, 0, -1):
    time.sleep(0.1)
    rubles = random.randrange(0, 5000, 1)
    if message.find(str(number)) != -1:
        await s(nickname + ", поздравляю! Ты победил! Приз " + str(rubles) + " руб. PepoParty ")
await s("Чат проиграл, время вышло Sadge ")
"""