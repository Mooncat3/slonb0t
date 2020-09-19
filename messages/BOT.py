from twitchio.ext import commands
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from cook import COOKIES
import time

channel = 'danantur'
OAUTH = '14y5qalllj1i65rg3m9dip1rpq5ugd'

bot = commands.Bot(
    irc_token=f'oauth:{OAUTH}',
    nick='SLONB0T',
    prefix='!',
    initial_channels=[f'{channel}'])


@bot.event
async def event_ready():
    print("Бот запущен!")


@bot.event
async def event_command_error(ctx, error):
    pass


@bot.command(name='сколько')
async def skolko(ctx):
    if ctx.content == "!сколько":
        nickname = ctx.author.name
    else:
        nickname = ctx.content.replace("!сколько ", "")
    await ctx.channel.send(
        ctx.author.name + ", идёт сканирование сообщений пользователя " + nickname + "... Обычно это занимает до 10 "
                                                                                     "минут")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    url = 'https://www.twitch.tv/popout/jesusavgn/viewercard/' + nickname

    driver.get(url)
    driver.add_cookie(COOKIES[0])
    driver.get(url)
    time.sleep(4)
    try:
        actions = ActionChains(driver)
        element = driver.find_element_by_xpath('//span[starts-with(@class, "text-fragment")]')
        element.click()
        time.sleep(0.5)
        for i in range(0, 1000):
            actions.key_down(Keys.HOME).perform()
            print(round(i/10))

        actions.key_up(Keys.HOME).perform()
        soup = BeautifulSoup(str(driver.page_source), 'lxml')
        d = soup.find_all('div', class_='tw-pd-x-1 tw-pd-y-05')
        await ctx.channel.send(
            ctx.author.name + ", пользователь " + nickname + " написал " + str(len(d)) + " сообщений!")
    except:
        await ctx.channel.send(ctx.author.name + ", пользователь не найден")
    driver.quit()


bot.run()
