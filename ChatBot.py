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

@bot.command(name='SLONB0T')
async def chat(ctx):
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

@bot.command(name="slonb0t,")
async def chat1(ctx):
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

@bot.command(name="slonb0t")
async def chat2(ctx):
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

    
bot.run()
