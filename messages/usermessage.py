from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from cook import COOKIES, PREFS
import time

chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("disable-infobars")
chrome_options.add_experimental_option("prefs", PREFS)
driver = webdriver.Chrome(options=chrome_options)

nickname = 'justririll'

url = 'https://www.twitch.tv/popout/jesusavgn/viewercard/' + nickname

driver.get(url)
driver.add_cookie(COOKIES[0])
driver.get(url)
print('Сайт загружен...')
time.sleep(5)

actions = ActionChains(driver)
driver.find_element_by_xpath('//span[starts-with(@class, "text-fragment")]').click()
element = driver.find_element_by_class_name('simplebar-scrollbar')
time.sleep(0.5)
print('Выполняется сканирование сообщений...')
actions.key_down(Keys.HOME).perform()
while element.is_displayed():
    actions.key_down(Keys.HOME).perform()
actions.key_up(Keys.HOME).perform()
soup = BeautifulSoup(str(driver.page_source), 'lxml')
d = soup.find_all('div', class_='tw-pd-x-1 tw-pd-y-05')
print("Пользователь " + nickname + " написал " + str(len(d)) + " сообщений!")
driver.quit()
input()
