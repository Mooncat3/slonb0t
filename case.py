import requests
from bs4 import BeautifulSoup
import random
import re

randstr = random.randint(1, 179)
r = requests.get('https://market.csgo.com/?s=name&r=&q=&p=' + str(randstr) + '&rs=1;5000&h=&fst=0')
soup = BeautifulSoup(r.content, 'html.parser')
d = soup.find_all('a', class_='item')
skin = str(random.choice(d)).partition(';"></div>')[2]
skinorig = re.sub('<div class="price">', '', skin)
skinorig = re.sub("\n", '', skinorig)
skin = skinorig.partition(';">')[2].replace('</div></a>', '')
price = skinorig.rpartition('<s')[0]
print("Вам выпало: " + skin)
print("Цена: " + price + "₽")
input()
