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


@bot.command(name='SLONB0T', aliases=["slonb0t,", "slonb0t"])
async def chat(ctx):
    message = str(ctx.message.clean_content)
    nickname = ctx.author.name
    if not re.search(r'[a-zA-Z]', message) or AdditionalMethods.vip(ctx.author.is_mod, ctx.author.name):
        url = "https://aiproject.ru/api/"
        query = {"ask": message, "userid": nickname, "key": ""}
        jsonquery = json.encoder.JSONEncoder.encode(self=json.encoder.JSONEncoder(), o=query)
        try:
            with requests.sessions.Session() as session:
                response = session.request(method="post", url=url, data={"query": jsonquery}, timeout=3)
            content = response.content.decode('utf8').replace("'", '"')
            data = json.loads(content)
            AdditionalMethods.add_to_buffer("e",
                                            ctx.author.display_name + ", " + AdditionalMethods.parse_response_query(
                                                data),
                                            ctx.author, "SLONB0T")
        except:
            AdditionalMethods.add_to_buffer("e", ctx.author.display_name + ", На данный момент чатбот не доступен "
                                                                           "roflanPominy",
                                            ctx.author, "SLONB0T")
    else:
        AdditionalMethods.add_to_buffer("s", ctx.author.display_name + ", бот может общаться с вами только на русском "
                                                                       "языке", ctx.author, "SLONB0T")


bot.run()
