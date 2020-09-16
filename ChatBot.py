# -*- coding: utf8 -*-	
from twitchioc.ext import commands	
import json	
import AdditionalMethods	
import re	
import requests	
import config	


bot = commands.Bot(	
    irc_token=f'oauth:{config.OAUTH}',	
    client_id=config.CLIENT_ID,	
    nick=config.BOT,	
    prefix='@',	
    initial_channels=config.CHANNELS)	

@bot.event	
async def event_ready():	
    print(f'Ready ChatBot | {config.BOT} on {config.CHANNELS}')	

@bot.event	
async def event_command_error(ctx, error):	
    pass	

@bot.event	
async def event_message(ctx):	
    
    if ctx.content.lower().find('slonb0t') != -1:	
        if ctx.author.name.lower() == "slonb0t":
            pass
    else:
        message = ctx.content	
        nickname = ctx.author.name	
        mess = message.lower().replace("slonb0t","").replace("@","")	
        mess = re.sub("\n", '', mess)	
        url = "https://aiproject.ru/api/"	
        query = {"ask": mess, "userid": nickname, "key": ""}	
        jsonquery = json.encoder.JSONEncoder.encode(self=json.encoder.JSONEncoder(), o=query)	
        try:	
            with requests.sessions.Session() as session:	
                response = session.request(method="post", url=url, data={"query": jsonquery}, timeout=3)	
            content = response.content.decode('utf8').replace("'", '"')	
            data = json.loads(content)	
            AdditionalMethods.add_to_buffer("e", nickname + ", " + AdditionalMethods.parse_response_query(data), ctx.author, "SLONB0T")	
        except:	
            AdditionalMethods.add_to_buffer("e", nickname + ", На данный момент чатбот не доступен roflanPominy", ctx.author, "SLONB0T")	
    await bot.handle_commands(ctx)	


bot.run()
