import json
import re
import lyricsgenius as lg
from twitchio.ext import commands

channel = 'jesusavgn'
OAUTH = '14y5qalllj1i65rg3m9dip1rpq5ugd'

bot = commands.Bot(
    irc_token=f'oauth:{OAUTH}',
    nick='SLONB0T',
    prefix='!',
    initial_channels=[f'{channel}'])


@bot.event
async def event_ready():
    print('Музыка запущена!')


@bot.event
async def event_command_error(ctx, error):
    pass


@bot.command(name='music')
async def music(ctx):
    nick = ctx.author.display_name
    message = ctx.message.clean_content
    if len(message) == 0:
        await ctx.channel.send(nick + ', введите - !music [строка из песни] [смайл]')
    else:
        mess = message.split(' ')
        emote = ' ' + mess[len(mess) - 1]
        with open('data/SMILES.txt', encoding='utf-8') as g:
            list_emotes = json.loads(g.read())
        if not mess[len(mess) - 1] in list_emotes:
            await ctx.channel.send(nick + ', введите - !music [строка из песни] [смайл]')
        else:
            try:
                song_lyric = ' '.join(mess[1:]).replace(emote, '')
                emote += ' '
                genius = lg.Genius("5Pj7QcUoV5Khbd-Hq5jSve8OzCQILJkY8nWojIIxqH30ItpsmXC7UmCRcgjmTVPY")
                song = genius.search_song(song_lyric)
                text = re.sub(r'[\[].*?[\]]', '', song.lyrics)
                res = [x for x in text.split('\n') if len(x) > 2]
                u = 0
                for stroka in res:
                    if u == 0:
                        for strr in stroka.split(' '):
                            if song_lyric.lower() == stroka.lower():
                                res = res[res.index(stroka):]
                                u = 1
                                break
                            for slovo in song_lyric.lower().split(' '):
                                if slovo == strr.lower() and len(slovo) > 4:
                                    res = res[res.index(stroka):]
                                    u = 1
                                    break
                res = emote.join(res[:5])
                with open('data/osujdau.txt', encoding='utf-8') as f:
                    osu = f.read().split('\n')
                res_prov = re.sub(r'\W+', ' ', res)
                for word in res_prov.split(' '):
                    if word.lower() in osu:
                        res = res.replace(word, '*' * len(word))
                await ctx.channel.send(res[:250] + emote)

            except AttributeError:
                await ctx.channel.send(nick + ', песня не найдена!')
    print('-' * 80)


bot.run()
