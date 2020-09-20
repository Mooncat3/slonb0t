import requests
from twitchio.ext import commands
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from cook import COOKIES, PREFS
import time
import datetime

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


@bot.event
async def event_command_error(ctx, error):
    pass


@bot.command(name='сколько')
async def skolko(ctx):
    timee = time.time()
    if ctx.content == "!сколько":
        nickname = ctx.author.name
    else:
        nickname = ctx.content.replace("!сколько ", "").replace("@", "")
    url = "https://api.streamelements.com/kappa/v2/chatstats/jesusavgn/stats"
    r = requests.get(url)
    json_r = r.json()['chatters']
    listnames = []
    i = 0
    while i < 100:
        name = json_r[i]['name']
        listnames.append(name)
        i += 1
    if nickname.lower() in listnames:
        await ctx.channel.send(ctx.author.name + ", данный пользователь уже находится в топе 100 чаттеров")
    else:
        await ctx.channel.send(ctx.author.name + ", идёт сканирование сообщений пользователя " + nickname + " Waiting")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_experimental_option("prefs", PREFS)
        driver = webdriver.Chrome(options=chrome_options)

        url = 'https://www.twitch.tv/popout/jesusavgn/viewercard/' + nickname

        driver.get(url)
        driver.add_cookie(COOKIES[0])
        driver.get(url)
        time.sleep(4)
        
        try:
            soup = BeautifulSoup(str(driver.page_source), 'lxml')
            count = soup.find('p', class_='tw-c-text-link tw-font-size-5 tw-strong').get_text()
            if count != "999+":
                await ctx.channel.send(f"{ctx.author.name}, пользователь {nickname} написал {count} сообщений! (с 01.06.2017)")
                driver.quit()
            else:
                actions = ActionChains(driver)
                driver.find_element_by_xpath('//span[starts-with(@class, "text-fragment")]').click()
                element = driver.find_element_by_class_name('simplebar-scrollbar')
                time.sleep(0.5)
                actions.key_down(Keys.HOME).perform()
                while element.is_displayed():
                    actions.key_down(Keys.HOME).perform()
                actions.key_up(Keys.HOME).perform()
                soup = BeautifulSoup(str(driver.page_source), 'lxml')
                d = soup.find_all('div', class_='tw-pd-x-1 tw-pd-y-05')
                data = str(datetime.timedelta(seconds=round(time.time() - timee)))
                print(f"{ctx.author.name}, пользователь {nickname} написал {str(len(d))} сообщений!")
                await ctx.channel.send(f"{ctx.author.name}, пользователь {nickname} написал {str(len(d))} сообщений! (с 01.06.2017) (Поиск выполнен за {data})")
                driver.quit()
        except:
            await ctx.channel.send(ctx.author.name + ", не удалось узнать кол-во сообщений данного пользователя PepoG")
            driver.quit()


bot.run()
