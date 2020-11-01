from selenium import webdriver
import requests
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
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
    print("Бот запущен!")


@bot.command(name='music')
async def music(ctx):
    mess = str(ctx.message.content).split(' ')
    back = ctx.message.content
    print(mess)
    emote = mess[len(mess) - 1]
    song_title = back.replace('!music ', '').replace(emote, '')
    print(emote)
    print(song_title)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://teksty-pesenok.ru/search/?searchid=2236269&text=' + song_title + '&web=0'
    driver.get(url)
    search = driver.find_element_by_xpath('//a[starts-with(@class, "b-serp-item__title-link")]').get_attribute('href')
    print(search)
    r = requests.get(search)
    soup = BeautifulSoup(r.text, 'lxml')
    emote = ' ' + emote + ' '
    try:
        text = soup.find('div', class_='textPesni').get_text().split('\r')
    except:
        text = soup.find('td', style='vertical-align: top; width: 50%;').get_text().split('\n')
    res = emote.join(text[:5])

    print(res)
    await ctx.channel.send(res)


bot.run()
