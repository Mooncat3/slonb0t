# -*- coding: utf-8 -*-
from irc.bot import SingleServerIRCBot
from datetime import datetime, timedelta
import re
import random
import time

HOST = 'irc.twitch.tv'
PORT = 6667
USERNAME = 'SLONB0T'
PASSWORD = 'oauth:1jfryqh0pt9e4uyvhvdl22hk2v9w7a'
CHANNEL = '#danantur'



class VBot(SingleServerIRCBot):


    def __init__(self, host, port, nickname, password, channel):
        SingleServerIRCBot.__init__(self, [(host, port, password)], nickname, nickname)
        self.channel = channel


    def on_welcome(self, connection, event):
        connection.join(self.channel)
        print("Бот " + USERNAME + " запущен на канале " + CHANNEL + "!")
        



    def on_pubmsg(self, connection, event):
        nick = event.source.nick
        message = event.arguments[0]
        s = event.target


        iq = random.randrange(55, 180, 1)
        tempp = random.uniform(25, 45)
        temp = round(tempp, 1)
        procent = random.randrange(0, 100, 1)
        ruble = random.randrange(0, 2000, 1)
        cock = random.randrange(1, 36, 1)
        boobs = random.randrange(0, 7, 1)
        


        if message.strip() == '+паста':
            with open('nadya.txt', 'r', encoding='utf-8') as n:
                    nadyaa = list(n)
                    randomnadya = random.choice(nadyaa)
                    randomnadya = re.sub("\n", '', randomnadya)
                    hh = re.sub(r'^(.{230}).*$', '\g<1>...', randomnadya)
                    self.connection.privmsg(s, hh)
            print(nick+': '+message)

        if message.strip() == '+help':
            buffer = nick
            self.connection.privmsg(s, buffer + ", Привет, я бот по имени слон. Можешь использовать следующие команды (страница 1): +паста, +me, +do [nickname], +iq, +temp, +love [nickname], +бубу [something], +steal [nickname] Чтобы перейти на следующую страницу введите +help1 catJAM")
            buffer = ''
            print(nick+': '+message)
            
        if message.strip() == '+help1':
            buffer = nick
            self.connection.privmsg(s, buffer + ", Привет, я бот по имени слон catJAM Можешь использовать следующие команды (страница 2): +привет [nickname], +try [something], +time, +когда [something], +обнять [nickname], +COCK catJAM")
            buffer = ''
            print(nick+': '+message)

        if message.find('+iq') != -1:
            buffer = nick
            if iq == 110:
                self.connection.privmsg(s, buffer + ", ваш IQ = " + str(iq) + "! Вы Хесус?! PogU")
                buffer = ''
            if iq == 89:
                self.connection.privmsg(s, buffer + ", ваш IQ = " + str(iq) + "! Вы Братишкин?! PogU")
                buffer = ''
            else:
                if iq < 110 and iq > 70:
                    self.connection.privmsg(s, buffer + ", ваш IQ = " + str(iq) + "! Надо же, у стримера больше IQ чем у вас KeK")
                    buffer = ''
                if iq > 110 and iq < 135:
                    self.connection.privmsg(s, buffer + ", ваш IQ = " + str(iq) + "! Ого, а вы не глупый человек ThumbUp")
                    buffer = ''
                if iq < 70:
                    self.connection.privmsg(s, buffer + ", ваш IQ = " + str(iq) + "! Чел... сходи книгу почитай WeirdChamp")
                    buffer = ''
                if iq >= 135:
                    self.connection.privmsg(s, buffer + ", ваш IQ = " + str(iq) + "! Внимание! В чате гений WAYTOOSMART Clap")
                    buffer = ''
            print(nick+': '+message)

        if message.find('+temp') != -1:
            buffer = nick
            if temp >= 35.7 and temp <= 37:
                self.connection.privmsg(s, buffer + ", ваша температура " + str(temp) + " °C! У вас температура в пределах нормы ThumbUp")
                buffer = ''
            else:
                if temp > 37 and temp < 40 or temp < 35.7 and temp >= 32:
                    self.connection.privmsg(s, buffer + ", ваша температура " + str(temp) + " °C! Вы больны? coronaS")
                    buffer = ''
                else:
                    if temp > 40 or temp < 32:
                        self.connection.privmsg(s, buffer + ", ваша температура " + str(temp) + " °C! Срочно вызывайте скорую! Durka")
                        buffer = ''
            print(nick+': '+message)

        if message.find('+me') != -1:
            buffer = nick
            with open('me.txt', 'r', encoding='utf-8') as b:
                listme = list(b)
                randomm = random.choice(listme)
                randomm = re.sub("\n", '', randomm)
            self.connection.privmsg(s, buffer + ' ' + randomm)
            buffer = ''
            print(nick+': '+message)

        if message.find('+do') != -1:
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1:
                self.connection.privmsg(s, buffer + ", думал забанить меня? WeirdChamp ")
                buffer = ''
            else:
                with open('do.txt', 'r', encoding='utf-8') as c:
                    listme = list(c)
                    randomdo = random.choice(listme)
                    re.sub("\n", '', randomdo)
                    do = str.replace(message, '+do ', '')
                    re.sub("\n", '', do)
                    self.connection.privmsg(s, randomdo.format(buffer,do))
                    buffer = ''
            print(nick+': '+message)

        if message.find('+бубу') != -1:
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1:
                self.connection.privmsg(s, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                bubu = str.replace(message, '+бубу ', '')
                bubu = re.sub("\n", '', bubu)
                self.connection.privmsg(s, "Ну " + str(bubu) + " и " + str(bubu) + " Чё бубнить-то? ThumbUp")
            print(nick+': '+message)

        if message.find('+love ') != -1:
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1:
                self.connection.privmsg(s, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                love = str.replace(message, '+love ', '')
                love = re.sub("\n", '', love)
                self.connection.privmsg(s, buffer + " любит " + str(love) + " на " + str(procent) + "%!")
                buffer = ''
            print(nick+': '+message)

        if message.find('+steal ') != -1:
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1:
                self.connection.privmsg(s, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                steal = str.replace(message, '+steal ', '')
                steal = re.sub("\n", '', steal)
                if procent >= 33:
                    self.connection.privmsg(s, buffer + " украл у " + str(steal) + " " + str(ruble) + " руб. BOP")
                    buffer = ''
                else:
                    self.connection.privmsg(s, buffer + " ничего не украл у " + str(steal) + " KeK Lohich")
                    buffer = ''
            print(nick+': '+message)

        if message.find('+try ') != -1:
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1:
                self.connection.privmsg(s, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                tryy = str.replace(message, '+try ', '')
                tryy = re.sub("\n", '', tryy)
                with open('try.txt', 'r', encoding='utf-8') as m:
                    listtry = list(m)
                    tryr = random.choice(listtry)
                    tryr = re.sub("\n", '', tryr)
                self.connection.privmsg(s, buffer + " попробовал " + tryy + "... " + tryr)
                buffer = ''
            print(nick+': '+message)

        if message.find('+time') != -1:
            self.connection.privmsg(event.target, "Таксс... PepoG ")
            time.sleep(2)
            self.connection.privmsg(s, datetime.strftime(datetime.now()+timedelta(hours=3),"Чичас %H:%M:%S по МСК Waiting"))
            print(nick+': '+message)

        if message.find('+обнять') != -1:
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1:
                self.connection.privmsg(s, buffer + ", думал забанить меня? WeirdChamp ")
                buffer = ''
            else:
                with open('hug.txt', 'r', encoding='utf-8') as j:
                    hugg = list(j)
                    randomhug = random.choice(hugg)
                    randomhug = re.sub("\n", '', randomhug)
                    hug = str.replace(message, '+обнять ', '')
                    hug = re.sub("\n", '', hug)
                    self.connection.privmsg(s, buffer + " " + randomhug + " обнимает " + hug + " VoHiYo")
                    buffer = ''
            print(nick+': '+message)
                    
        if message.find('+COCK') != -1:
            buffer = nick
            self.connection.privmsg(s, buffer + ", твой COCK равен " + str(cock) + " см! YEP")
            buffer = ''
            print(nick+': '+message)
            
        if message.find('+BOOBS') != -1:
            buffer = nick
            if boobs == 7:
                self.connection.privmsg(s, buffer + ", твои BOOBS 6+ размера YEP PogU")
            else:
                self.connection.privmsg(s, buffer + ", твои BOOBS " + str(boobs) + " размера YEP")
            buffer = ''
            print(nick+': '+message)
        
        if message.find('blushW') != -1:
            self.connection.privmsg(s, "blushW")
            print(nick+': '+message)

        if message.find('peepoLeave') != -1:
            self.connection.privmsg(s, "peepoLeave")
            print(nick+': '+message)
            
        if message.find('мав') != -1:
            self.connection.privmsg(s, "мав")
            print(nick+': '+message)

        if message.find('catJAM') != -1:
            self.connection.privmsg(s, "catJAM")
            print(nick+': '+message)

        if message.find('ThumbUp') != -1:
            self.connection.privmsg(s, "ThumbUp")
            print(nick+': '+message)

        if message.find('+когда') != -1:
            buffer = nick
            with open('kogda.txt', 'r', encoding='utf-8') as m:
                listkogda = list(m)
                koogda = str.replace(message, '+когда ', '')
                koogda = re.sub("\n", '', koogda)
                kogda = random.choice(listkogda)
                kogda = re.sub("\n", '', kogda)
            self.connection.privmsg(s, buffer + ", " + koogda + ' ' + kogda)
            buffer = ''
            print(nick+': '+message)

        if message.find('+привет') != -1:
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1:
                self.connection.privmsg(s, buffer + ", думал забанить меня? WeirdChamp ")
                buffer = ''
            else:
                with open('privet.txt', 'r', encoding='utf-8') as c:
                    privit = list(c)
                    randommm = random.choice(privit)
                    randommm = re.sub("\n", '', randommm)
                    privet = str.replace(message, '+привет ', '')
                    privet = re.sub("\n", '', privet)
                    self.connection.privmsg(s, buffer + " передаёт " + randommm + " привет " + privet + " peepoHey peepoLove")
                    buffer = ''
            print(nick+': '+message)
        time.sleep(0.05)
       


    @staticmethod
    def _parse_nickname_from_twitch_user_id(user_id):
        return user_id.split('!', 1)[0]


def main():
    my_bot = VBot(HOST, PORT, USERNAME, PASSWORD, CHANNEL)
    my_bot.start()


if __name__ == '__main__':
    main()
