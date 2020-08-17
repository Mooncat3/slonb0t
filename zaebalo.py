@commands.command(name='заебало')
async def zaebalo(self, ctx):
    s = ctx.send
    randpage = random.randrange(1, 1689, 1)
    r = requests.get("https://zaebalo.ru/?page=" + str(randpage))
    soup = BeautifulSoup(r.content, 'html.parser')
    d = soup.find_all('div', align='left')
    p = str(random.choice(d)).replace("</div>", "").replace("<br/>", "").replace("</p>", "").replace("<p>", "").replace('<div align="left">', '').replace("<br>", "").replace("</br>", "")
    while 'пидор' in p or 'негр' in p or len(p) > 500:
        d = soup.find_all('div', align='left')
        p = str(random.choice(d)).replace("</div>", "").replace("<br/>", "").replace("</p>", "").replace("<p>", "").replace('<div align="left">', '').replace("<br>", "").replace("</br>", "")
    await s(p)