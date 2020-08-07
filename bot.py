# -*- coding: utf-8 -*-
from irc.bot import SingleServerIRCBot
from datetime import datetime, timedelta
import threading
import re
import random
import time

HOST = 'irc.twitch.tv'
PORT = 6667
USERNAME = 'SLONB0T'
PASSWORD = 'oauth:1jfryqh0pt9e4uyvhvdl22hk2v9w7a'
CHANNEL = '#jesusavgn'


class VBot(SingleServerIRCBot):
    
    changingInt = 0
    maxInt = 0
    whois = ""
    ischanging = False

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



        if message.strip() == '+паста':
            with open('nadya.txt', 'r', encoding='utf-8') as n:
                nadyaa = list(n)
                randomnadya = random.choice(nadyaa)
                randomnadya = re.sub("\n", '', randomnadya)
                hh = re.sub(r'^(.{230}).*$', '\g<1>...', randomnadya)
                self.connection.privmsg(s, hh)
            print(nick + ': ' + message)

        if message.strip() == '+help':
            buffer = nick
            self.connection.privmsg(s, buffer + ", Привет, я бот по имени слон. Можешь использовать следующие команды (страница 1): +паста, +me, +do [nickname], +iq, +temp, +love [nickname], +бубу [something], +steal [nickname] Чтобы перейти на следующую страницу введите +help1 catJAM")
            buffer = ''
            print(nick + ': ' + message)

        if message.strip() == '+help1':
            buffer = nick
            self.connection.privmsg(s, buffer + ", Привет, я бот по имени слон catJAM Можешь использовать следующие команды (страница 2): +привет [nickname], +try [something], +time, +когда [something], +обнять [nickname], +COCK, +вверх catJAM")
            buffer = ''
            print(nick + ': ' + message)

        if message.strip() == '+iq':
            buffer = nick
            iq = random.randrange(55, 180, 1)
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
            print(nick + ': ' + message)

        if message.strip() == '+temp':
            buffer = nick
            tempp = random.uniform(25, 45)
            temp = round(tempp, 1)
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
            print(nick + ': ' + message)

        if message.strip() == '+me':
            buffer = nick
            with open('me.txt', 'r', encoding='utf-8') as b:
                listme = list(b)
                randomm = random.choice(listme)
                randomm = re.sub("\n", '', randomm)
            self.connection.privmsg(s, randomm.format(buffer))
            buffer = ''
            print(nick + ': ' + message)
            
        if self.ischanging:
            if self.changingInt == self.maxInt and self.changingInt > 0:
                    self.ischanging = False
                    self.changingInt = 0
                    self.maxInt = 0
                    self.connection.privmsg(s, ":point_up_2: @{} - {} PogU ".format(buffer, self.whois))
                    buffer = ''
                else:
                    if self.changingInt == self.maxInt:
                        who = str.replace(message, '+кто ', '')
                        who = re.sub("\n", '', who)
                        self.whois = who
                        self.ischanging = True
                        self.connection.privmsg(s, "хммм, кто же MonkaHmm ....")
                        self.maxInt = random.randint(5, 15)
                        self.changingInt += 1
                    else:
                        self.changingInt += 1
            
        if message.find('+кто ') != -1 and message.index('+кто ') == 0 and message[len('+кто '):len(message)] != "":
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1:
                self.connection.privmsg(s, buffer + ", думал забанить меня? WeirdChamp ")
                buffer = ''
            else:
                if self.changingInt == self.maxInt and self.changingInt > 0:
                    self.ischanging = False
                    self.changingInt = 0
                    self.maxInt = 0
                    self.connection.privmsg(s, ":point_up_2: @{} - {} PogU ".format(buffer, self.whois))
                    buffer = ''
                else:
                    if self.changingInt == self.maxInt:
                        who = str.replace(message, '+кто ', '')
                        who = re.sub("\n", '', who)
                        self.whois = who
                        self.ischanging = True
                        self.connection.privmsg(s, "хммм, кто же MonkaHmm ....")
                        self.maxInt = random.randint(5, 15)
                        self.changingInt += 1
                    else:
                        self.changingInt += 1
            print(nick + ': ' + message)
        else:
            if message.find('+кто') != -1 and message.index('+кто') == 0 and message[len('+кто'):len(message)] == "":
                self.connection.privmsg(s, "И как я должен его обозвать? шизик? WeirdChamp ")

        if message.find('+do ') != -1 and message.index('+do ') == 0 and message[len('+do '):len(message)] != "":
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1:
                self.connection.privmsg(s, buffer + ", думал забанить меня? WeirdChamp ")
                buffer = ''
            else:
                with open('do.txt', 'r', encoding='utf-8') as c:
                    listme = list(c)
                    randomdo = random.choice(listme)
                    randomdo = re.sub("\n", '', randomdo)
                    do = str.replace(message, '+do ', '')
                    do = re.sub("\n", '', do)
                    self.connection.privmsg(s, randomdo.format(buffer, do))
                    buffer = ''
            print(nick + ': ' + message)
        else:
            if message.find('+do') != -1 and message.index('+do') == 0 and message[len('+do'):len(message)] == "":
                self.connection.privmsg(s, "И чё я должен сделать? шизик? WeirdChamp ") 

        if message.find('+бубу ') != -1 and message.index('+бубу ') == 0 and message[len('+бубу '):len(message)] != "":
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1:
                self.connection.privmsg(s, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                bubu = str.replace(message, '+бубу ', '')
                bubu = re.sub("\n", '', bubu)
                self.connection.privmsg(s, "Ну " + str(bubu) + " и " + str(bubu) + " Чё бубнить-то? ThumbUp")
            print(nick + ': ' + message)
        else:
            if message.find('+бубу') != -1 and message.index('+бубу') == 0 and message[len('+бубу'):len(message)] == "":
                self.connection.privmsg(s, "И чё я должен бубу? шизик? WeirdChamp ") 

        if message.find('+love ') != -1 and message.index('+love ') == 0 and message[len('+love '):len(message)] != "":
            buffer = nick
            procent = random.randrange(0, 100, 1)
            if message.find('.') != -1 or message.find('suicide') != -1 or message.find('kill') != -1:
                self.connection.privmsg(s, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                love = str.replace(message, '+love ', '')
                love = re.sub("\n", '', love)
                self.connection.privmsg(s, buffer + " любит " + str(love) + " на " + str(procent) + "%!")
                buffer = ''
            print(nick + ': ' + message)
        else:
            if message.find('+love') != -1 and message.index('+love') == 0 and message[len('+love'):len(message)] == "":
                self.connection.privmsg(s, "И чё я должен бубу? шизик? WeirdChamp ") 

        if message.find('+steal ') != -1 and message.index('+steal ') == 0 and message[len('+steal '):len(message)] != "":
            buffer = nick
            procent = random.randrange(0, 100, 1)
            ruble = random.randrange(0, 2000, 1)
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
            print(nick + ': ' + message)
        else:
            if message.find('+steal') != -1 and message.index('+steal') == 0 and message[len('+steal'):len(message)] == "":
                self.connection.privmsg(s, "И у кого ты крадёшь? шизик? WeirdChamp ") 

        if message.find('+try ') != -1 and message.index('+try ') == 0 and message[len('+try '):len(message)] != "":
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
            print(nick + ': ' + message)
        else:
            if message.find('+try') != -1 and message.index('+try') == 0 and message[len('+try'):len(message)] == "":
                self.connection.privmsg(s, "И чё ты пробуешь? шизик? WeirdChamp ") 

        if message.find('+time') != -1:
            self.connection.privmsg(event.target, "Таксс... PepoG ")
            time.sleep(2)
            self.connection.privmsg(s, datetime.strftime(datetime.now() + timedelta(hours=3), "Чичас %H:%M по МСК Waiting"))
            print(nick + ': ' + message)

        if message.find('+обнять ') != -1 and message.index('+обнять ') == 0 and message[len('+обнять '):len(message)] != "":
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
            print(nick + ': ' + message)
        else:
            if message.find('+обнять') != -1 and message.index('+обнять') == 0 and message[len('+обнять'):len(message)] == "":
                self.connection.privmsg(s, "И чё ты пробуешь обнять? шизик? WeirdChamp ") 

        if message.find('+COCK') != -1:
            buffer = nick
            cock = random.randrange(1, 36, 1)
            self.connection.privmsg(s, buffer + ", твой COCK равен " + str(cock) + " см! YEP")
            buffer = ''
            print(nick + ': ' + message)

        if message.find('+BOOBS') != -1:
            buffer = nick
            boobs = random.randrange(0, 7, 1)
            if boobs == 7:
                self.connection.privmsg(s, buffer + ", твои BOOBS 6+ размера YEP PogU")
            else:
                self.connection.privmsg(s, buffer + ", твои BOOBS " + str(boobs) + " размера YEP")
            buffer = ''
            print(nick + ': ' + message)

        if message.find('blushW') != -1:
            self.connection.privmsg(s, "blushW")
            print(nick + ': ' + message)

        if message.find('peepoLeave') != -1:
            self.connection.privmsg(s, "peepoLeave")
            print(nick + ': ' + message)

        if message.find('мав') != -1:
            self.connection.privmsg(s, "мав")
            print(nick + ': ' + message)

        if message.find('catJAM') != -1:
            self.connection.privmsg(s, "catJAM")
            print(nick + ': ' + message)

        if message.find('ThumbUp') != -1:
            self.connection.privmsg(s, "ThumbUp")
            print(nick + ': ' + message)

        """"
        if message.strip() == '+вверх':
            with open('down.txt', 'r', encoding='utf-8') as n:
                downn = list(n)
                randomdown = random.choice(downn)
                randomdown = re.sub("\n", '', randomdown)
                self.connection.privmsg(s, ":point_up_2: " +str(randomdown))
            print(nick + ': ' + message)


        if message.find('+игры') != -1:
            buffer = nick
            self.connection.privmsg(s, buffer + ", cписок всех мини-игр у бота: +угадать число")
            print(nick + ': ' + message)

        if message.find('+угадать число') != -1:
            self.connection.privmsg(s, "Правила: бот загадывает число от 0 до 20. Ваша задача угадать это число. У вас есть минута. Pog нали!")
            number = random.randrange(0, 20, 1)
            for i in range(600, 0, -1):
                time.sleep(0.1)
                rubles = random.randrange(0, 5000, 1)
                if message.find(str(number)) != -1:
                    buffer = nick
                    print(nick + ': ' + message)
                    self.connection.privmsg(s, buffer + ", поздравляю! Ты победил! Приз " + str(rubles) + " руб. PepoParty ")
                    buffer = ''
            self.connection.privmsg(s, "Чат проиграл, время вышло Sadge ")
            print(nick + ': ' + message)
        """""

        if message.find('+когда ') != -1 and message.index('+когда ') == 0 and message[len('+когда '):len(message)] != "":
            buffer = nick
            with open('kogda.txt', 'r', encoding='utf-8') as m:
                listkogda = list(m)
                koogda = str.replace(message, '+когда ', '')
                koogda = re.sub("\n", '', koogda)
                kogda = random.choice(listkogda)
                kogda = re.sub("\n", '', kogda)
            self.connection.privmsg(s, buffer + ", " + koogda + ' ' + kogda)
            buffer = ''
            print(nick + ': ' + message)
        else:
            if message.find('+когда') != -1 and message.index('+когда') == 0 and message[len('+когда'):len(message)] == "":
                self.connection.privmsg(s, "И чё я должен сделать? шизик? WeirdChamp ") 

        if message.find('+привет ') != -1 and message.index('+привет ') == 0 and message[len('+привет '):len(message)] != "":
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
            print(nick + ': ' + message)
        else:
            if message.find('+привет') != -1 and message.index('+привет') == 0 and message[len('+привет'):len(message)] == "":
                self.connection.privmsg(s, "И кого я должен приветствовать? шизик? WeirdChamp ") 
        time.sleep(0.05)

    @staticmethod
    def _parse_nickname_from_twitch_user_id(user_id):
        return user_id.split('!', 1)[0]


def main():
    my_bot = VBot(HOST, PORT, USERNAME, PASSWORD, CHANNEL)
    my_bot.start()


if __name__ == '__main__':
    main()
