from twitchio.ext import commands
import json
import requests
import re

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token='oauth:2ed7e435kk3dm1tpgo73gnu7xcjczy', client_id=forApiCalls.CLIENT_ID, nick='SLONB0T', prefix='@', initial_channels=['danantur'])

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        await self.handle_commands(message)

    @commands.command(name='SLONB0T')
    async def privet(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        url = "https://aiproject.ru/api/"
        query = {"ask": message, "userid": nickname, "key": ""}
        jsonquery = json.encoder.JSONEncoder.encode(self=json.encoder.JSONEncoder(), o=query)
        response = requests.post(url=url, data={"query": jsonquery})
        content = response.content.decode('utf8').replace("'", '"')
        data = json.loads(content)
        await s(nickname + ", " + data['aiml'])
        
    @commands.command(name='slonb0t, ')
    async def privet1(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        url = "https://aiproject.ru/api/"
        query = {"ask": message, "userid": nickname, "key": ""}
        jsonquery = json.encoder.JSONEncoder.encode(self=json.encoder.JSONEncoder(), o=query)
        response = requests.post(url=url, data={"query": jsonquery})
        content = response.content.decode('utf8').replace("'", '"')
        data = json.loads(content)
        await s(nickname + ", " + data['aiml'])   
   

bot = Bot()
bot.run()

if __name__ == '__main__':
    main()
