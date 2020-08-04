import socket
import re
import random
import string
import datetime
import time

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "SLONB0T"
PASS = "oauth:1jfryqh0pt9e4uyvhvdl22hk2v9w7a"
CHAN = "jesusavgn"
#CHAN = "mooncat3"



def mess(sock, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(CHAN, message).encode())



def main():
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(CHAN).encode("utf-8"))
    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

    while True:
        response = s.recv(4096).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = chat_message.sub("", response)
            respo = response[response.find(":") + 1 :]
            respon = respo[respo.find(":") + 1:]



            #print(username+': '+ respon)




            iq = random.randrange(50, 200, 1)
            tempp = random.uniform(25, 45)
            temp = round(tempp, 1)
            procent = random.randrange(0, 100, 1)
            ruble = random.randrange(0, 2000, 1)


            if respon.find('+test') != -1:
                mess(s, "сидя дома cmonDance грущу чего боюсь cmonDance иду в магаз cmonDance покупаю себе снюс cmonDance и обретаю силы cmonDance я получаю кайф cmonDance снюс моя жизнь снюс is my life cmonDance")


            if respon.find('+help') != -1:
                buffer = username
                mess(s, buffer + ", Привет, я бот по имени слон catJAM Можешь использовать следующие команды: +test, +me, +do [nickname], +iq, +temp, +love [nickname], +бубу [something], +steal [nickname], +привет [nickname], +try [something], +time, +когда [something], +hug [nickname] catJAM")
                buffer = ''


            if respon.find('@slonb0t') != -1:
                buffer = username
                mess(s, buffer + ", Привет, я бот по имени слон catJAM Можешь использовать следующие команды: +test, +me, +do [nickname], +iq, +temp, +love [nickname], +бубу [something], +steal [nickname], +привет [nickname], +try [something], +time, +когда [something], +hug [nickname] catJAM")
                buffer = ''


            if respon.find('+iq') != -1:
                buffer = username
                if iq == 110:
                    mess(s, buffer + " ваш IQ = " + str(iq) + "! Вы Хесус?! PogU")
                    buffer = ''
                if iq == 89:
                    mess(s, buffer + " ваш IQ = " + str(iq)+"! Вы Братишкин?! PogU")
                    buffer = ''
                else:
                    if iq < 110 and iq > 70:
                        mess(s, buffer + " ваш IQ = " + str(iq) + "! Надо же, у стримера больше IQ чем у вас KeK")
                        buffer = ''
                    if iq > 110 and iq < 135:
                        mess(s, buffer + " ваш IQ = " + str(iq) + "! Ого, а вы не глупый человек ThumbUp")
                        buffer = ''
                    if iq < 70:
                        mess(s, buffer + " ваш IQ = " + str(iq) + "! Чел... сходи книгу почитай WeirdChamp")
                        buffer = ''
                    if iq >= 135:
                        mess(s, buffer + " ваш IQ = " + str(iq) + "! Внимание! В чате гений WAYTOOSMART Clap")
                        buffer = ''


            if respon.find('+temp') != -1:
                buffer = username
                if temp >= 35.7 and temp <= 37:
                     mess(s, buffer + " ваша температура " + str(temp) + " °C! У вас температура в пределах нормы ThumbUp")
                     buffer = ''
                else:
                    if temp > 37 and temp < 40 or temp < 35.7 and temp >= 32:
                        mess(s, buffer + " ваша температура " + str(temp) + " °C! Вы больны? coronaS")
                        buffer = ''
                    else:
                        if temp > 40 or temp < 32:
                            mess(s, buffer + " ваша температура " + str(temp) + " °C! Срочно вызывайте скорую! Durka")
                            buffer = ''


            if respon.find('+me') != -1:
                buffer = username
                with open('me.txt', 'r', encoding='utf-8') as b:
                    listme = list(b)
                    randomm = random.choice(listme)
                    randomm = re.sub("\n", '', randomm)
                mess(s, buffer + ' ' + randomm)
                buffer = ''


            if respon.find('+do') != -1:
                buffer = username
                if respon.find('http') != -1 or respon.find('www') != -1 or respon.find('!') != -1 or respon.find('\.') != -1 or respon.find('suicide') != -1:
                    mess(s, buffer + ", думал забанить меня? WeirdChamp ")
                else:
                    with open('do.txt', 'r', encoding='utf-8') as c:
                        listme = list(c)
                        randomdo = random.choice(listme)
                        randomdo = re.sub("\n", '', randomdo)
                        #randomdo = respon[respon.index("+do") + len("+do") + 1:len(respon)]
                        do = str.replace(respon, '+do ', '')
                        do = re.sub("\n", '', do)
                        #mess(s, user + randomdo)
                        mess(s, buffer + " садит " + str(do) + " на бутылку YEP")
                        buffer = ''


            if respon.find('+бубу') != -1:
                if respon.find('http') != -1 or respon.find('www') != -1 or respon.find('!') != -1 or respon.find('\.') != -1 or respon.find('suicide') != -1:
                    mess(s, buffer + ", думал забанить меня? WeirdChamp ")
                else:
                    bubu = str.replace(respon, '+бубу ', '')
                    bubu = re.sub("\n", '', bubu)
                    mess(s, "Ну " + str(bubu) + " и " + str(bubu) +". Чё бубнить-то? ThumbUp")


            if respon.find('+love ') != -1:
                buffer = username
                if respon.find('http') != -1 or respon.find('www') != -1 or respon.find('!') != -1 or respon.find('\.') != -1 or respon.find('suicide') != -1:
                    mess(s, buffer + ", думал забанить меня? WeirdChamp ")
                else:
                    love = str.replace(respon, '+love ', '')
                    love = re.sub("\n", '', love)
                    mess(s, buffer + " любит " + str(love) + " на " + str(procent) + "%!")
                    buffer = ''


            if respon.find('+steal ') != -1:
                buffer = username
                if respon.find('http') != -1 or respon.find('www') != -1 or respon.find('!') != -1 or respon.find('\.') != -1 or respon.find('suicide') != -1:
                    mess(s, buffer + ", думал забанить меня? WeirdChamp ")
                else:
                    steal = str.replace(respon, '+steal ', '')
                    steal = re.sub("\n", '', steal)
                    mess(s, buffer + " украл у " + str(steal) + " " + str(ruble) + " руб. BOP")
                    buffer = ''


            if respon.find('+try ') != -1:
                buffer = username
                if respon.find('http') != -1 or respon.find('www') != -1 or respon.find('!') != -1 or respon.find('\.') != -1 or respon.find('suicide') != -1:
                    mess(s, buffer + ", думал забанить меня? WeirdChamp ")
                else:
                    tryy = str.replace(respon, '+try ', '')
                    tryy = re.sub("\n", '', tryy)
                    with open('try.txt', 'r', encoding='utf-8') as m:
                        listtry = list(m)
                        tryr = random.choice(listtry)
                        tryr = re.sub("\n", '', tryr)
                    mess(s, buffer + " попробовал " + str(tryy) + "... " + str(tryr))
                    buffer = ''


            if respon.find('+time') != -1:
                mess(s, "Таксс... PepoG ")
                time.sleep(2)
                data = datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S")
                mess(s, "Чичас " + str(data) + " По МСК Waiting")

            if respon.find('+hug') != -1:
                buffer = username
                if respon.find('http') != -1 or respon.find('www') != -1 or respon.find('!') != -1 or respon.find('\.') != -1 or respon.find('suicide') != -1:
                    mess(s, buffer + ", думал забанить меня? WeirdChamp ")
                else:
                    with open('hug.txt', 'r', encoding='utf-8') as j:
                        hugg = list(j)
                        randomhug = random.choice(hugg)
                        randomhug = re.sub("\n", '', randomhug)
                        hug = str.replace(respon, '+hug ', '')
                        hug = re.sub("\n", '', hug)
                        mess(s, buffer + " " + str(randomhug) + " обнимает " + str(hug) + " VoHiYo")
                
                
                
                
            if respon.find('blushW') != -1:
                mess(s, "blushW")
                
                
            if respon.find('peepoLeave') != -1:
                mess(s, "peepoLeave")


            if respon.find('catJAM') != -1:
                mess(s, "catJAM")


            if respon.find('ThumbUp') != -1:
                mess(s, "ThumbUp")


            if respon.find('+когда') != -1:
                buffer = username
                with open('kogda.txt', 'r', encoding='utf-8') as m:
                    listkogda = list(m)
                    kogda = random.choice(listkogda)
                    kogda = re.sub("\n", '', kogda)
                mess(s, buffer + ", " + kogda)


            if respon.find('+привет') != -1:
                buffer = username
                if respon.find('http') != -1 or respon.find('www') != -1 or respon.find('!') != -1 or respon.find('\.') != -1 or respon.find('suicide') != -1:
                    mess(s, buffer + ", думал забанить меня? WeirdChamp ")
                else:
                    with open('privet.txt', 'r', encoding='utf-8') as c:
                        privit = list(c)
                        randommm = random.choice(privit)
                        randommm = re.sub("\n", '', randommm)
                        privet = str.replace(respon, '+привет ', '')
                        privet = re.sub("\n", '', privet)
                        mess(s, buffer + " передаёт " + str(randommm) + " привет " + str(privet) + " peepoHey peepoLove")

print("Бот " + NICK + " запущен на канале "+str(CHAN)+"!")
if __name__ == "__main__":
    main()
