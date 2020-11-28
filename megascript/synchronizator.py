import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from cook import PREFS, COOKIES
import time
import json



#Екарны бабай, закидывай cook.py и chromedriver.exe со скриптом Pepechill

data = requests.get(f"http://tmi.twitch.tv/group/user/jesusavgn/chatters").json()

chatters = []
for k in data['chatters'].keys():
        chatters += data['chatters'][k]

end_count = len(chatters)

timestart = time.time()

for user in chatters:

    should_pass = False

    answer = json.loads(requests.get(f"https://sl0n.herokuapp.com/stats/jesusavgn?nickname={user}", headers={"Authorization": "y5IArL6S&%%G(69G"}).content.decode("utf-8"))

    if answer['type'] == 'success':
        if 'count_state' in answer['answer'].keys():
            if answer['answer']['count_state'] > 1:
                should_pass = True

    r = requests.get("https://api.streamelements.com/kappa/v2/chatstats/jesusavgn/stats")
    json_r = r.json()['chatters']

    listnames = {}
    for i in range(0, 100):
        listnames[json_r[i]['name']] = json_r[i]['amount']

    if should_pass:
        print(f"//------------- Данный пользователь уже синхронизирован! {user} -------------------//")
    elif user in listnames.keys():
        print(f"//------------- Данный пользователь ЛОХ! {user} {listnames[user]} -------------------//")
        print(requests.post("https://sl0n.herokuapp.com/stats/jesusavgn",
                            data={'type': 'clear', 'nickname': user},
                            headers={"Authorization": "y5IArL6S&%%G(69G"}).content)
        print(
            requests.post("https://sl0n.herokuapp.com/stats/jesusavgn",
                          data={'type': 'add', 'nickname': user, 'count': listnames[user]},
                          headers={"Authorization": "y5IArL6S&%%G(69G"}).content)
    else:
        print(f"//------------- Идёт сканирование сообщений пользователя {user} -------------------//")
        print(requests.post("https://sl0n.herokuapp.com/stats/jesusavgn",
                            data={'type': 'clear', 'nickname': user},
                            headers={"Authorization": "y5IArL6S&%%G(69G"}).content)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option("prefs", PREFS)
        driver = webdriver.Chrome(options=chrome_options)
        url = 'https://www.twitch.tv/popout/jesusavgn/viewercard/' + user
        driver.get(url)
        driver.add_cookie(COOKIES[0])
        driver.get(url)
        try:
            WebDriverWait(driver, timeout=6).until(ec.visibility_of_element_located((By.CLASS_NAME, "tw-c-text-link")))
            mess = driver.find_element_by_xpath('//p[starts-with(@class, "tw-c-text-link tw-font-size-5 tw-strong")]').text
            if mess == '999+':
                WebDriverWait(driver, timeout=3).until(ec.visibility_of_element_located((By.CLASS_NAME, "text-fragment")))
                driver.find_element_by_xpath('//span[starts-with(@class, "text-fragment")]').click()
                elem = driver.find_element_by_class_name('simplebar-scrollbar')
                while elem.is_displayed():
                    ActionChains(driver).key_down(Keys.HOME).perform()
                mess = len(driver.find_elements_by_xpath('//span[starts-with(@class, "text-fragment")]'))
            print(f"Пользователь {user} написал {str(mess)} сообщений!")
            print(requests.post("https://sl0n.herokuapp.com/stats/jesusavgn",
                              data={'type': 'add', 'nickname': user, 'count': mess},
                              headers={"Authorization": "y5IArL6S&%%G(69G"}).content)
        except TimeoutException:
            print(f"Не удалось узнать кол-во сообщений {user}")
        driver.quit()
print(f"//------------- СКАНИРОВАНИЕ ЗАВЕРШЕНО -------------------//")
