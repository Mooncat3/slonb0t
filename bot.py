from twitchio.ext import commands
import json
import requests
import forApiCalls
import re

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token='oauth:2ed7e435kk3dm1tpgo73gnu7xcjczy', client_id='9qmki7jzmtz6qnjj4z35yucfn29xb9', nick='SLONB0T', prefix='@', initial_channels=['jesusavgn'])

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    @commands.command(name='SLONB0T')
    async def privet(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        mess = str.replace(message, '@SLONB0T ', '')
        mess = re.sub("\n", '', mess)
        url = "https://aiproject.ru/api/"
        query = {"ask": mess, "userid": nickname, "key": ""}
        print(query)
        jsonquery = json.encoder.JSONEncoder.encode(self=json.encoder.JSONEncoder(), o=query)
        response = requests.post(url=url, data={"query": jsonquery})
        content = response.content.decode('utf8').replace("'", '"')
        data = json.loads(content)
        print(data)
        await s(nickname + ", " + forApiCalls.parse_response_query(data))

    @commands.command(name='slonb0t,')
    async def privet1(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        s = ctx.send
        mess = str.replace(message, '@slonb0t ', '')
        mess = re.sub("\n", '', mess)
        url = "https://aiproject.ru/api/"
        query = {"ask": mess, "userid": nickname, "key": ""}
        print(query)
        jsonquery = json.encoder.JSONEncoder.encode(self=json.encoder.JSONEncoder(), o=query)
        response = requests.post(url=url, data={"query": jsonquery})
        content = response.content.decode('utf8').replace("'", '"')
        data = json.loads(content)
        print(data)
        await s(nickname + ", " + forApiCalls.parse_response_query(data))

bot = Bot()
bot.run()
