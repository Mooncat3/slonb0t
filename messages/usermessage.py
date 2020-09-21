import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from cook import COOKIES, PREFS
import time

nickname = ''

url = "https://api.streamelements.com/kappa/v2/chatstats/jesusavgn/stats"
r = requests.get(url)
json_r = r.json()['chatters']

listnames = []
for i in range(0, 100):
    name = json_r[i]['name']
    listnames.append(name)

if nickname.lower() in listnames:
    print("Данный пользователь уже находится в топе 100 чаттеров!")

else:

    print("Идёт сканирование сообщений пользователя " + nickname + "...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs", PREFS)
    driver = webdriver.Chrome(options=chrome_options)

    url = 'https://www.twitch.tv/popout/jesusavgn/viewercard/' + nickname

    driver.get(url)
    driver.add_cookie(COOKIES[0])
    driver.get(url)
    time.sleep(4)

    try:
        count = driver.find_element_by_xpath('//p[starts-with(@class, "tw-c-text-link")]').text
        if count != "999+":
            print(f"Пользователь {nickname} написал {count} сообщений!")
            driver.quit()

        else:
            actions = ActionChains(driver)
            driver.find_element_by_xpath('//span[starts-with(@class, "text-fragment")]').click()
            element = driver.find_element_by_class_name('simplebar-scrollbar')

            while element.is_displayed():
                actions.key_down(Keys.HOME).perform()

            mess = str(len(driver.find_elements_by_xpath('//span[starts-with(@class, "text-fragment")]')))

            print(f"Пользователь {nickname} написал {mess} сообщений!")
            driver.quit()

    except NoSuchElementException:

        print("Не удалось узнать кол-во сообщений данного пользователя PepoG")
        driver.quit()
