import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from megascript.cook import PREFS, COOKIES
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
        chrome_options.add_experimental_option("prefs", PREFS)
        driver = webdriver.Chrome(options=chrome_options)

        url = 'https://www.twitch.tv/popout/jesusavgn/viewercard/' + user

        driver.get(url)
        driver.add_cookie(COOKIES[0])
        driver.get(url)
        time.sleep(4)

        try:
            count = driver.find_element_by_xpath('//p[starts-with(@class, "tw-c-text-link")]').text
            if count != "999+":
                count = int(count)
                print(f"Пользователь {user} написал {count} сообщений!")
                driver.quit()
            else:
                actions = ActionChains(driver)
                driver.find_element_by_xpath('//span[starts-with(@class, "text-fragment")]').click()
                element = driver.find_element_by_class_name('simplebar-scrollbar')

                while element.is_displayed():
                    actions.key_down(Keys.HOME).perform()

                mess = str(len(driver.find_elements_by_xpath('//span[starts-with(@class, "text-fragment")]')))

                count = int(mess)

                print(f"Пользователь {user} написал {mess} сообщений!")
                driver.quit()
            print(
                requests.post("https://sl0n.herokuapp.com/stats/jesusavgn",
                              data={'type': 'add', 'nickname': user, 'count': count},
                              headers={"Authorization": "y5IArL6S&%%G(69G"}).content)
        except Exception as e:
            print(f"Не удалось узнать кол-во сообщений {user} {e}")
            driver.quit()

print(f"//------------- СКАНИРОВАНИЕ ЗАВЕРШЕНО -------------------//")
