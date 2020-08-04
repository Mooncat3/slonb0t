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



            print(username+': '+ respon)




            iq = random.randrange(50, 200, 1)
            tempp = random.uniform(25, 45)
            temp = round(tempp, 1)
            procent = random.randrange(0, 100, 1)
            ruble = random.randrange(0, 2000, 1)


            if respon.find('+test') != -1:
                mess(s, "сидя дома cmonDance грущу чего боюсь cmonDance иду в магаз cmonDance покупаю себе снюс cmonDance и обретаю силы cmonDance я получаю кайф cmonDance снюс моя жизнь снюс is my life cmonDance")


            if respon.find('+help') != -1:
                mess(s, username + ", Привет, я бот по имени слон catJAM Можешь использовать следующие команды: +test, +me, +do [nickname], +iq, +temp, +love [nickname], +бубу [something], +steal [nickname], +привет [nickname], +try [something], +time, +когда [something] catJAM")


            if respon.find('@slonb0t') != -1:
                mess(s, username + ", Привет, я бот по имени слон catJAM Можешь использовать следующие команды: +test, +me, +do [nickname], +iq, +temp, +love [nickname], +бубу [something], +steal [nickname], +привет [nickname], +try [something], +time, +когда [something] catJAM")


            if respon.find('+iq') != -1:
                if iq == 110:
                    mess(s, username + " ваш IQ = " + str(iq) + "! Вы Хесус?! PogU")
                if iq == 89:
                    mess(s, username + " ваш IQ = " + str(iq)+"! Вы Братишкин?! PogU")
                else:
                    if iq < 110 and iq > 70:
                        mess(s, username + " ваш IQ = " + str(iq) + "! Надо же, у стримера больше IQ чем у вас KeK")
                    if iq > 110 and iq < 135:
                        mess(s, username + " ваш IQ = " + str(iq) + "! Ого, а вы не глупый человек ThumbUp")
                    if iq < 70:
                        mess(s, username + " ваш IQ = " + str(iq) + "! Чел... сходи книгу почитай WeirdChamp")
                    if iq >= 135:
                        mess(s, username + " ваш IQ = " + str(iq) + "! Внимание! В чате гений WAYTOOSMART Clap")


            if respon.find('+temp') != -1:
                if temp >= 35.7 and temp <= 37:
                     mess(s, username + " ваша температура " + str(temp) + " °C! У вас температура в пределах нормы ThumbUp")
                else:
                    if temp > 37 and temp < 40 or temp < 35.7 and temp >= 32:
                        mess(s, username + " ваша температура " + str(temp) + " °C! Вы больны? coronaS")
                    else:
                        if temp > 40 or temp < 32:
                            mess(s, username + " ваша температура " + str(temp) + " °C! Срочно вызывайте скорую! Durka")


            if respon.find('+me') != -1:
                with open('me.txt', 'r', encoding='utf-8') as b:
                    listme = list(b)
                    randomm = random.choice(listme)
                    randomm = re.sub("\n", '', randomm)
                mess(s, username + ' ' + randomm)


            if respon.find('+do') != -1:
                with open('do.txt', 'r', encoding='utf-8') as c:
                    listme = list(c)
                    randomdo = random.choice(listme)
                    randomdo = re.sub("\n", '', randomdo)
                #randomdo = respon[respon.index("+do") + len("+do") + 1:len(respon)]
                do = str.replace(respon, '+do ', '')
                do = re.sub("\n", '', do)
                #mess(s, user + randomdo)
                mess(s, username + " садит " + str(do) + " на бутылку YEP")


            if respon.find('+бубу') != -1:
                bubu = str.replace(respon, '+бубу ', '')
                bubu = re.sub("\n", '', bubu)
                mess(s, "Ну " + str(bubu) + " и " + str(bubu) +". Чё бубнить-то? ThumbUp")


            if respon.find('+love ') != -1:
                love = str.replace(respon, '+love ', '')
                love = re.sub("\n", '', love)
                mess(s, username + " любит " + str(love) + " на " + str(procent) + "%!")


            if respon.find('+steal ') != -1:
                steal = str.replace(respon, '+steal ', '')
                steal = re.sub("\n", '', steal)
                mess(s, username + " украл у " + str(steal) + " " + str(ruble) + " руб. BOP")


            if respon.find('+try ') != -1:
                tryy = str.replace(respon, '+try ', '')
                tryy = re.sub("\n", '', tryy)
                with open('try.txt', 'r', encoding='utf-8') as m:
                    listtry = list(m)
                    tryr = random.choice(listtry)
                    tryr = re.sub("\n", '', tryr)
                mess(s, username + " попробовал " + str(tryy) + "... " + str(tryr))


            if respon.find('+time') != -1:
                mess(s, "Таксс... PepoG ")
                time.sleep(2)
                data = datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S")
                mess(s, "Чичас " + str(data) + " По МСК Waiting")

                
                
            if respon.find('blushW') != -1:
                mess(s, "blushW")
                
                
            if respon.find('peepoLeave') != -1:
                mess(s, "peepoLeave")


            if respon.find('catJAM') != -1:
                mess(s, "catJAM")


            if respon.find('ThumbUp') != -1:
                mess(s, "ThumbUp")


            if respon.find('+когда') != -1:
                with open('kogda.txt', 'r', encoding='utf-8') as m:
                    listkogda = list(m)
                    kogda = random.choice(listkogda)
                    kogda = re.sub("\n", '', kogda)
                mess(s,username + ", " + kogda)


            if respon.find('+привет') != -1:
                with open('privet.txt', 'r', encoding='utf-8') as c:
                    privit = list(c)
                    randommm = random.choice(privit)
                    randommm = re.sub("\n", '', randommm)
                    privet = str.replace(respon, '+привет ', '')
                    privet = re.sub("\n", '', privet)
                    mess(s, username + " передаёт " + str(randommm) + " привет " + str(privet) + " peepoHey peepoLove")

print("Бот " + NICK + " запущен на канале "+str(CHAN)+"!")
if __name__ == "__main__":
    main()