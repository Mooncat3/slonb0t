import datetime
import time
import requests
from cook import PREFS
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait



timestart = time.time()


nickname = ''


url = "https://api.streamelements.com/kappa/v2/chatstats/jesusavgn/stats"
r = requests.get(url)
json_r = r.json()['chatters']
listnames = []

for i in range(0, 100):
    name = json_r[i]['name']
    listnames.append(name)

if nickname.lower() in listnames:
    print("Данный пользователь уже находится в топе 100 чаттеров")
    
else:

    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument('--user-data-dir=data')
    chrome_options.binary_location = 'C://Users//Admin//AppData//Local//Google//Chrome SxS//Application//chrome.exe'
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("prefs", PREFS)
    driver = webdriver.Chrome(options=chrome_options)

    print("Идёт поиск сообщений пользователя " + nickname + " Waiting")

    url = 'https://www.twitch.tv/popout/jesusavgn/viewercard/' + nickname

    driver.get(url)
    #driver.add_cookie(COOKIES[0])
    #driver.get(url)
    WebDriverWait(driver, timeout=10).until(ec.visibility_of_element_located((By.CLASS_NAME, "tw-c-text-link")))

    try:
        count = driver.find_element_by_xpath('//p[starts-with(@class, "tw-c-text-link")]').text
        if count != "999+":
            
            date = str(datetime.timedelta(seconds=round(time.time() - timestart)))
            print(f"{ctx.author.name}, пользователь {nickname} написал {count} сообщений! (Поиск выполнен за {date})")
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

            print(f"{ctx.author.name}, пользователь {nickname} написал {mess} сообщений! (Поиск выполнен за {date})")
            driver.quit()

    except NoSuchElementException:
        print("Не удалось узнать кол-во сообщений данного пользователя")
        driver.quit()
