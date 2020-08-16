from twitchio.ext import commands
import json
import AdditionalMethods
import re
import requests
import config


class ChatBot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=f'oauth:{config.OAUTH}',
                         client_id=config.CLIENT_ID, nick=config.BOT, prefix='@', initial_channels=config.CHANNELS)

    async def event_ready(self):
        print(f'Ready ChatBot | {self.nick} on {self.initial_channels}')

    @commands.command(name='SLONB0T')
    async def privet(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        mess = str.replace(message, '@SLONB0T ', '')
        mess = re.sub("\n", '', mess)
        if AdditionalMethods.check_on_bans(mess, ctx.author):
            url = "https://aiproject.ru/api/"
            query = {"ask": mess, "userid": nickname, "key": ""}
            jsonquery = json.encoder.JSONEncoder.encode(self=json.encoder.JSONEncoder(), o=query)
            response = requests.post(url=url, data={"query": jsonquery})
            content = response.content.decode('utf8').replace("'", '"')
            data = json.loads(content)
            AdditionalMethods.add_to_buffer("e", nickname + ", " + AdditionalMethods.parse_response_query(data), ctx.author)

    @commands.command(name='slonb0t')
    async def privet1(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        mess = str.replace(message, '@slonb0t ', '')
        mess = re.sub("\n", '', mess)
        if AdditionalMethods.check_on_bans(mess, ctx.author):
            url = "https://aiproject.ru/api/"
            query = {"ask": mess, "userid": nickname, "key": ""}
            jsonquery = json.encoder.JSONEncoder.encode(self=json.encoder.JSONEncoder(), o=query)
            response = requests.post(url=url, data={"query": jsonquery})
            content = response.content.decode('utf8').replace("'", '"')
            data = json.loads(content)
            AdditionalMethods.add_to_buffer("e", nickname + ", " + AdditionalMethods.parse_response_query(data), ctx.author)



bot = ChatBot()
bot.run()
