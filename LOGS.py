import AdditionalMethods
from bs4 import BeautifulSoup
import requests
import time

with open(file='data/TRASHMASSIVE.txt', mode='r', encoding='utf-8') as q:
    strer = q.read()
paste = AdditionalMethods.createPaste(strer, "loges", "php", "1", "10M")
urlPaste = AdditionalMethods.sendPaste(paste)

teg = urlPaste[21:]

r = requests.get('https://pastebin.com/raw/' + str(teg))
soup = BeautifulSoup(r.content, 'lxml')
d = soup.get_text()

with open(file='data/TRASHMASSIVE.txt', mode='w', encoding='utf-8') as e:
    e.write(str(d))

time.sleep(7200)
