from twitchio.ext import commands
from collections import Counter
import urllib.request
from multiprocessing import Process
import json
import time


channel = 'jesusavgn'
OAUTH = '14y5qalllj1i65rg3m9dip1rpq5ugd'


URL = 'https://api.twitch.tv/helix/streams?user_login=' + channel
Client_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
head = {'Authorization': f'Bearer {OAUTH}', 'Client-ID' : Client_ID}


def checkstream():
    while True:
        request = urllib.request.Request(url = URL, headers = head)
        response = urllib.request.urlopen(request).read()
        data = json.loads(response)
        if len(data['data']) > 0:
            with open('data/top/active.txt', 'w') as f:
                f.write("1")
                
                
            with open('data/top/title.txt', 'r', encoding='utf_8') as g:
                checktitile = g.read()
                
                
            title = str(data).partition("le': '")[-1].rpartition("', 'vi")[0]
            
            
            if checktitile != title:
                with open('data/top/title.txt', 'w') as u:
                    u.write(title) 
                with open('data/top/nicknames.txt', 'w') as ll:
                    ll.write("")
                print("Произведена чистка списка никнеймов!")
                
                
        else:
            with open('data/top/active.txt', 'w') as f:
                f.write("0")
                
                
        time.sleep(10)
   
     
def bott():
    bot = commands.Bot(
            irc_token=f'oauth:{OAUTH}',
            nick='SLONB0T',
            prefix='!',
            initial_channels=[f'{channel}'])

    @bot.event
    async def event_ready():
        print("Ready Top | SLONB0T on ['jesusavgn']")

    @bot.event
    async def event_command_error(ctx, error):
        pass

    @bot.event
    async def event_message(ctx):
        with open('data/top/active.txt', 'r') as d:
            check = d.read()
        if check == "1":
            if ctx.author.name == 'slonb0t' or ctx.author.name == 'moobot' or ctx.author.name == channel:
                pass
            else:
                with open('data/top/nicknames.txt', 'a', encoding='utf-8') as log:
                    log.write(ctx.author.name + "\n")
        await bot.handle_commands(ctx)

    @bot.command(name='top')
    async def top(ctx):
        try:
            with open('data/top/nicknames.txt', 'r', encoding='utf-8') as f:
                listtop = [line.strip() for line in f]
            if len(listtop) == 0 or listtop == " " or len(listtop) == 1:
                await ctx.channel.send(ctx.author.name +", на данный момент список пользователей пуст!")
            else:
                top = Counter(listtop).most_common(5)
                res = list(enumerate(top,1))
                res = str(res).replace("[(","").replace("))]","]").replace(", ('",") ").replace(")), (","], ").replace("', "," [")
                await ctx.channel.send(ctx.author.name +", топ 5 пользователей по сообщениям за стрим: " + res)
        except FileNotFoundError:
            await ctx.channel.send(ctx.author.name +", на данный момент список пользователей пуст!")

    bot.run()
    
    
if __name__ == '__main__':
    one = Process(target=checkstream)
    two = Process(target=bott)
    
    one.start()
    two.start()
