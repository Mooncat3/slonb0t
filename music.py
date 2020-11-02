import re
from selenium import webdriver
import requests
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from twitchio.ext import commands
from urllib.parse import quote
import random

channel = 'jesusavgn'
OAUTH = '14y5qalllj1i65rg3m9dip1rpq5ugd'

bot = commands.Bot(
    irc_token=f'oauth:{OAUTH}',
    nick='SLONB0T',
    prefix='!',
    initial_channels=[f'{channel}'])


@bot.event
async def event_ready():
    pass


@bot.event
async def event_command_error(ctx, error):
    pass


@bot.command(name='music')
async def music(ctx):
    nick = ctx.author.name
    if ctx.message.content == '!music':
        await ctx.channel.send(nick + ', введите - !music [строка из песни] [смайл]')
    else:
        mess = ctx.message.content.split(' ')
        emote = ' ' + mess[len(mess) - 1]
        song_lyric = ' '.join(mess[1:]).replace(emote, '').lower()
        emote += ' '
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # chrome_options.add_argument('--user-data-dir=data')
        driver = webdriver.Chrome(options=chrome_options)
        url = 'https://teksty-pesenok.ru/search/?searchid=2236269&text=' + quote(song_lyric)
        driver.get(url)
        est = driver.find_element_by_xpath('//yass-div[starts-with(@class, "b-head__found")]').text
        if est == 'найдёт всё. Со временем':
            await ctx.channel.send(nick + ', такой песни не найдено!')
            driver.close()
        else:
            try:
                search = driver.find_element_by_xpath(
                    '//a[starts-with(@class,"b-serp-item__title-link")]').get_attribute(
                    'href')
                driver.close()
                print(search)
                r = requests.get(search)
                soup = BeautifulSoup(r.text, 'lxml')
                ist = '\nИсточник teksty-pesenok.ru'
                try:
                    text = soup.find('div', class_='textPesni').get_text().replace(ist, '')
                except AttributeError:
                    text = soup.find('td', style='vertical-align: top; width: 50%;').get_text().replace(ist, '')

                    if text.find('\n\n') != -1:
                        text = text.split('\n')

                text = re.sub(r'\n[\[].*?[\]]', '', '\n' + str(''.join(text)))
                res = [x for x in text.split('\r\n') if len(x) > 2]
                if len(res) == 1:
                    res = [x for x in text.split('\n') if len(x) > 2]
                u = 0
                for stroka in res:
                    if u == 0:
                        for strr in stroka.split(' '):
                            if song_lyric == stroka.lower():
                                res = res[res.index(stroka):]
                                u = 1
                                break
                            for slovo in song_lyric.split(' '):
                                if slovo == strr.lower() and len(slovo) > 3:
                                    res = res[res.index(stroka):]
                                    u = 1
                                    break
                print(res)
                res = emote.join(res[:random.randint(4, 5)])
                with open('data/osujdau.txt', encoding='utf-8') as f:
                    osu = f.read().split('\n')
                res_prov = re.sub(r'\W+', ' ', res)
                for word in res_prov.split(' '):
                    if word.lower() in osu:
                        res = res.replace(word, '*' * len(word))

                await ctx.channel.send(res[:200] + emote)
            except NoSuchElementException:
                await ctx.channel.send(nick + ', такой песни не найдено!')
    print('-' * 50)


bot.run()
