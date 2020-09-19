from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from cook import COOKIES
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

nickname = 'yebak_beznadezhniy'

url = 'https://www.twitch.tv/popout/jesusavgn/viewercard/' + nickname

driver.get(url)
driver.add_cookie(COOKIES[0])
driver.get(url)
print('Сайт загружен...')
time.sleep(5)

actions = ActionChains(driver)
element = driver.find_element_by_xpath('//span[starts-with(@class, "text-fragment")]')
element.click()
time.sleep(0.5)
print('Выполняется сканирование сообщений...')
for i in range(0, 1000):
    actions.key_down(Keys.HOME).perform()
    actions.key_up(Keys.HOME).perform()
    time.sleep(0.01)

soup = BeautifulSoup(str(driver.page_source), 'lxml')
d = soup.find_all('div', class_='tw-pd-x-1 tw-pd-y-05')
print("Пользователь " + nickname + " написал " + str(len(d)) + " сообщений!")
driver.quit()
input()
