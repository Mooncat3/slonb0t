from twitchio.ext import commands
from datetime import datetime, timedelta
import forApiCalls
import json
import requests
import re
import random

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token='oauth:{}'.format(forApiCalls.OAUTH), client_id=forApiCalls.CLIENT_ID, nick='SLONB0T', prefix='@', initial_channels=['danantur'])

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
        print(jsonquery)
        response = requests.post(url=url, data={"query": jsonquery})

        content = response.content.decode('utf8').replace("'", '"')

        print(content)

        data = json.loads(content)

        await s(data['aiml'])





def main():
    bot = Bot()
    bot.run()

if __name__ == '__main__':
    main()