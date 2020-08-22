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


@commands.command(name='love')
async def love(self, ctx):
    if not AdditionalMethods.check_active():
        message = ctx.message.content
        nickname = ctx.author.name
        if message == "!love":
            AdditionalMethods.add_to_buffer("e", f"{nickname}, введите !love [nickname]")
        else:
            procent = random.randrange(0, 100, 1)
            if AdditionalMethods.check_on_bans(message):
                love = str.replace(message, '!love ', '')
                love = re.sub("\n", '', love)
                AdditionalMethods.add_to_buffer("e", f"{nickname} любит {str(love)} на {str(procent)} %!")


@commands.command(name='COCK')
async def cock(self, ctx):
    nickname = ctx.author.name
    cock = random.randrange(1, 36, 1)
    AdditionalMethods.add_to_buffer("e", f"{nickname}, твой COCK равен {str(cock)} см! YEP", ctx.author)
    
    
@commands.command(name='BOOBS')
async def boobs(self, ctx):
    nickname = ctx.author.name
    boobs = random.randrange(0, 15, 1)
    AdditionalMethods.add_to_buffer("e", f"{nickname}, твои BOOBS {str(boobs)} размера YEP", ctx.author)
    
@commands.command(name='заебало')
    async def zaebalo(self, ctx):
        randpage = random.randrange(1, 1689, 1)
        r = requests.get("https://zaebalo.ru/?page=" + str(randpage))
        soup = BeautifulSoup(r.content, 'html.parser')
        d = soup.find_all('div', align='left')
        p = str(random.choice(d)).replace("</div>", "").replace("<br/>", "").replace("</p>", "").replace("<p>", "").replace(
            '<div align="left">', '').replace("<br>", "").replace("</br>", "").replace("\r     ", "")
        with open('data/osujdau.txt', 'r', encoding='utf-8') as c:
            List = list(c)
            for s in List:
                ban = ""
                s = s.replace("\n", "")
                for i in range(0, len(s)):
                    ban += "*"
                if p.find(s) != -1:
                    print(s)
                p = str.replace(p.lower(), s, ban)
        AdditionalMethods.add_to_buffer("e", AdditionalMethods.check_on_toomuchsimbols(p), ctx.author)
