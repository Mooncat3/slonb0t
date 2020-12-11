from twitchioc.ext import commands
import json
from abc import ABC
import AdditionalMethods
import re
import asyncio
import requests
import config


class ChatBot(commands.Bot, ABC):
    def __init__(self):
        super().__init__(irc_token=f'oauth:{config.OAUTH}', client_id=config.CLIENT_ID, nick=config.BOT, prefix='@', initial_channels=config.CHANNELS)

    async def event_ready(self):
        print(f'Ready ChatBot | {config.BOT} on {config.CHANNELS[0]}')
    
    async def event_command_error(self, ctx, error):
        pass
    
    async def event_message(self, message):
        nickname = message.author.name
        with open('data/blacklist.txt', encoding='utf-8') as f:
            blacklist = [x for x in f.read().split('\n') if len(x) > 1]
        if nickname in blacklist and not AdditionalMethods.vip(message.author.is_mod, nickname):
            return
        await self.handle_commands(message)
        
    @commands.command(name='SLONB0T', aliases=["slonb0t,", "slonb0t"])
    async def chat(self, ctx):
        message = ctx.message.clean_content
        nickname = ctx.author.name
        message = re.sub(r'[a-zA-Z]', '', message)
        url = "https://aiproject.ru/api/"
        query = {"ask": message, "userid": nickname, "key": ""}
        jsonquery = json.encoder.JSONEncoder.encode(self=json.encoder.JSONEncoder(), o=query)
        r = json.loads(requests.post(url, data={"query": query}).content.decode('utf8'))
        AdditionalMethods.add_to_buffer("e", ctx.author.display_name + ", " + AdditionalMethods.parse_response_query(r), ctx.author, "SLONB0T")

bot = ChatBot()
bot.run()
