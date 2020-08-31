from abc import ABC
from twitchioc.ext import commands
import json
import AdditionalMethods
import re
import requests
import config


class ChatBot(commands.Bot, ABC):

    def __init__(self):
        super().__init__(irc_token=f'oauth:{config.OAUTH}',
                         client_id=config.CLIENT_ID, nick=config.BOT, prefix='@', initial_channels=config.CHANNELS)

    async def event_ready(self):
        print(f'Ready {str(self.__class__.__name__)} | {self.nick} on {self.initial_channels}')
        
    async def event_command_error(ctx, error):
        return

    @commands.command(name='SLONB0T')
    async def privet(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        mess = str.replace(message, '@SLONB0T ', '')
        mess = re.sub("\n", '', mess)
        url = "https://aiproject.ru/api/"
        query = {"ask": mess, "userid": nickname, "key": ""}
        jsonquery = json.encoder.JSONEncoder.encode(self=json.encoder.JSONEncoder(), o=query)
        response = requests.post(url=url, data={"query": jsonquery})
        content = response.content.decode('utf8').replace("'", '"')
        data = json.loads(content)
        await AdditionalMethods.add_to_buffer("e", nickname + ", " + AdditionalMethods.parse_response_query(data), ctx.author, "SLONB0T")

    @commands.command(name="slonb0t,")
    async def privet1(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        mess = str.replace(message, '@slonb0t, ', '')
        mess = re.sub("\n", '', mess)
        url = "https://aiproject.ru/api/"
        query = {"ask": mess, "userid": nickname, "key": ""}
        jsonquery = json.encoder.JSONEncoder.encode(self=json.encoder.JSONEncoder(), o=query)
        response = requests.post(url=url, data={"query": jsonquery})
        content = response.content.decode('utf8').replace("'", '"')
        data = json.loads(content)
        await AdditionalMethods.add_to_buffer("e", nickname + ", " + AdditionalMethods.parse_response_query(data), ctx.author, "slonb0t,")
        
    @commands.command(name="slonb0t")
    async def privet1(self, ctx):
        message = ctx.message.content
        nickname = ctx.author.name
        mess = str.replace(message, '@slonb0t ', '')
        mess = re.sub("\n", '', mess)
        url = "https://aiproject.ru/api/"
        query = {"ask": mess, "userid": nickname, "key": ""}
        jsonquery = json.encoder.JSONEncoder.encode(self=json.encoder.JSONEncoder(), o=query)
        response = requests.post(url=url, data={"query": jsonquery})
        content = response.content.decode('utf8').replace("'", '"')
        data = json.loads(content)
        await AdditionalMethods.add_to_buffer("e", nickname + ", " + AdditionalMethods.parse_response_query(data), ctx.author, "slonb0t")    
 

bot = ChatBot()
bot.run()
