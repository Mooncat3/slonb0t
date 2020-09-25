import datetime
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from twitchio.ext import commands
from cook import PREFS

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


# @bot.event
# async def event_command_error(ctx, error):
# pass


@bot.command(name='mess')
async def mess(ctx):
    timestart = time.time()
    if ctx.content == "!mess":
        nickname = ctx.author.name
    else:
        nickname = ctx.content.replace("!mess ", "").replace("@", "")
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

        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument('--user-data-dir=data')
        chrome_options.binary_location = 'C://Users//Admin//AppData//Local//Google//Chrome SxS//Application//chrome.exe'
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option("prefs", PREFS)
        driver = webdriver.Chrome(options=chrome_options)

        await ctx.channel.send(ctx.author.name + ", идёт поиск сообщений пользователя " + nickname + " Waiting")

        url = 'https://www.twitch.tv/popout/jesusavgn/viewercard/' + nickname

        driver.get(url)
        #driver.add_cookie(COOKIES[0])
        #driver.get(url)

        WebDriverWait(driver, timeout=10).until(ec.visibility_of_element_located((By.CLASS_NAME, "tw-c-text-link")))

        try:
            count = driver.find_element_by_xpath('//p[starts-with(@class, "tw-c-text-link")]').text
            if count != "999+":
                date = str(datetime.timedelta(seconds=round(time.time() - timestart)))
                await ctx.channel.send(
                    f"{ctx.author.name}, пользователь {nickname} написал {count} сообщений! (Поиск выполнен за {date})")
                driver.quit()

            else:
                WebDriverWait(driver, timeout=10).until(
                    ec.visibility_of_element_located((By.CLASS_NAME, "text-fragment")))
                actions = ActionChains(driver)
                driver.find_element_by_xpath('//span[starts-with(@class, "text-fragment")]').click()
                element = driver.find_element_by_class_name('simplebar-scrollbar')

                while element.is_displayed():
                    actions.key_down(Keys.HOME).perform()

                mess = str(len(driver.find_elements_by_xpath('//span[starts-with(@class, "text-fragment")]')))

                date = str(datetime.timedelta(seconds=round(time.time() - timestart)))

                await ctx.channel.send(
                    f"{ctx.author.name}, пользователь {nickname} написал {mess} сообщений! (Поиск выполнен за {date})")
                driver.quit()

        except NoSuchElementException:

            await ctx.channel.send("Не удалось узнать кол-во сообщений данного пользователя")
            driver.quit()


bot.run()
