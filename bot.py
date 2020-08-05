from irc.bot import SingleServerIRCBot
import re
import random
import datetime
import time

HOST = 'irc.twitch.tv'
PORT = 6667
USERNAME = 'SLONB0T'
PASSWORD = 'oauth:1jfryqh0pt9e4uyvhvdl22hk2v9w7a'
CHANNEL = '#jesusavgn'



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

        iq = random.randrange(55, 180, 1)
        tempp = random.uniform(25, 45)
        temp = round(tempp, 1)
        procent = random.randrange(0, 100, 1)
        ruble = random.randrange(0, 2000, 1)


        if message.find('+test') != -1:
            self.connection.privmsg(event.target, 'и лыбится дурачок. чо ты лыбишься, урод? гавно своё на винтилятор кидает а дети патом бегают как бешеные по улице с белыми волосами ломают всё. из калонак всякое аоаоаоаоа доносица. вас запрещать законами надо, психи')

        if message.find('+help') != -1:
            buffer = nick
            self.connection.privmsg(event.target, buffer + ", Привет, я бот по имени слон catJAM Можешь использовать следующие команды: +test, +me, +do [nickname], +iq, +temp, +love [nickname], +бубу [something], +steal [nickname], +привет [nickname], +try [something], +time, +когда [something], +обнять [nickname] catJAM")
            buffer = ''

        if message.find('@slonb0t') != -1:
            buffer = nick
            self.connection.privmsg(event.target, buffer + ", Привет, я бот по имени слон catJAM Можешь использовать следующие команды: +test, +me, +do [nickname], +iq, +temp, +love [nickname], +бубу [something], +steal [nickname], +привет [nickname], +try [something], +time, +когда [something], +обнять [nickname] catJAM")
            buffer = ''

        if message.find('+iq') != -1:
            buffer = nick
            if iq == 110:
                self.connection.privmsg(event.target, buffer + ", ваш IQ = " + str(iq) + "! Вы Хесус?! PogU")
                buffer = ''
            if iq == 89:
                self.connection.privmsg(event.target, buffer + ", ваш IQ = " + str(iq) + "! Вы Братишкин?! PogU")
                buffer = ''
            else:
                if iq < 110 and iq > 70:
                    self.connection.privmsg(event.target, buffer + ", ваш IQ = " + str(iq) + "! Надо же, у стримера больше IQ чем у вас KeK")
                    buffer = ''
                if iq > 110 and iq < 135:
                    self.connection.privmsg(event.target, buffer + ", ваш IQ = " + str(iq) + "! Ого, а вы не глупый человек ThumbUp")
                    buffer = ''
                if iq < 70:
                    self.connection.privmsg(event.target, buffer + ", ваш IQ = " + str(iq) + "! Чел... сходи книгу почитай WeirdChamp")
                    buffer = ''
                if iq >= 135:
                    self.connection.privmsg(event.target, buffer + ", ваш IQ = " + str(iq) + "! Внимание! В чате гений WAYTOOSMART Clap")
                    buffer = ''

        if message.find('+temp') != -1:
            buffer = nick
            if temp >= 35.7 and temp <= 37:
                self.connection.privmsg(event.target, buffer + ", ваша температура " + str(temp) + " °C! У вас температура в пределах нормы ThumbUp")
                buffer = ''
            else:
                if temp > 37 and temp < 40 or temp < 35.7 and temp >= 32:
                    self.connection.privmsg(event.target, buffer + ", ваша температура " + str(temp) + " °C! Вы больны? coronaS")
                    buffer = ''
                else:
                    if temp > 40 or temp < 32:
                        self.connection.privmsg(event.target, buffer + ", ваша температура " + str(temp) + " °C! Срочно вызывайте скорую! Durka")
                        buffer = ''

        if message.find('+me') != -1:
            buffer = nick
            with open('me.txt', 'r', encoding='utf-8') as b:
                listme = list(b)
                randomm = random.choice(listme)
                randomm = re.sub("\n", '', randomm)
            self.connection.privmsg(event.target, buffer + ' ' + randomm)
            buffer = ''

        if message.find('+do') != -1:
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1:
                self.connection.privmsg(event.target, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                with open('do.txt', 'r', encoding='utf-8') as c:
                    listme = list(c)
                    randomdo = random.choice(listme)
                    randomdo = re.sub("\n", '', randomdo)
                    do = str.replace(message, '+do ', '')
                    do = re.sub("\n", '', do)
                    self.connection.privmsg(event.target, buffer + str(randomdo))
                    #self.connection.privmsg(event.target, buffer + " посадил " + do + " на бутылку YEP")
                    buffer = ''

        if message.find('+бубу') != -1:
            if message.find('.') != -1 or message.find('suicide') != -1:
                self.connection.privmsg(event.target, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                bubu = str.replace(message, '+бубу ', '')
                bubu = re.sub("\n", '', bubu)
                self.connection.privmsg(event.target, "Ну " + str(bubu) + " и " + str(bubu) + " . Чё бубнить-то? ThumbUp")

        if message.find('+love ') != -1:
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1:
                self.connection.privmsg(event.target, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                love = str.replace(message, '+love ', '')
                love = re.sub("\n", '', love)
                self.connection.privmsg(event.target, buffer + " любит " + str(love) + " на " + str(procent) + "%!")
                buffer = ''

        if message.find('+steal ') != -1:
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1:
                self.connection.privmsg(event.target, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                steal = str.replace(message, '+steal ', '')
                steal = re.sub("\n", '', steal)
                self.connection.privmsg(event.target, buffer + " украл у " + str(steal) + " " + str(ruble) + " руб. BOP")
                buffer = ''

        if message.find('+try ') != -1:
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1:
                self.connection.privmsg(event.target, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                tryy = str.replace(message, '+try ', '')
                tryy = re.sub("\n", '', tryy)
                with open('try.txt', 'r', encoding='utf-8') as m:
                    listtry = list(m)
                    tryr = random.choice(listtry)
                    tryr = re.sub("\n", '', tryr)
                self.connection.privmsg(event.target, buffer + " попробовал " + tryy + "... " + tryr)
                buffer = ''

        if message.find('+time') != -1:
            self.connection.privmsg(event.target, "Таксс... PepoG ")
            time.sleep(2)
            data = datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S")
            self.connection.privmsg(event.target, "Чичас " + data + " По МСК Waiting")

        if message.find('+обнять') != -1:
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1:
                self.connection.privmsg(event.target, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                with open('hug.txt', 'r', encoding='utf-8') as j:
                    hugg = list(j)
                    randomhug = random.choice(hugg)
                    randomhug = re.sub("\n", '', randomhug)
                    hug = str.replace(message, '+обнять ', '')
                    hug = re.sub("\n", '', hug)
                    self.connection.privmsg(event.target, buffer + " " + randomhug + " обнимает " + hug + " VoHiYo")

        if message.find('blushW') != -1:
            self.connection.privmsg(event.target, "blushW")

        if message.find('peepoLeave') != -1:
            self.connection.privmsg(event.target, "peepoLeave")

        if message.find('catJAM') != -1:
            self.connection.privmsg(event.target, "catJAM")

        if message.find('ThumbUp') != -1:
            self.connection.privmsg(event.target, "ThumbUp")

        if message.find('+когда') != -1:
            buffer = nick
            with open('kogda.txt', 'r', encoding='utf-8') as m:
                listkogda = list(m)
                kogda = random.choice(listkogda)
                kogda = re.sub("\n", '', kogda)
            self.connection.privmsg(event.target, buffer + ", " + kogda)

        if message.find('+привет') != -1:
            buffer = nick
            if message.find('.') != -1 or message.find('suicide') != -1:
                self.connection.privmsg(event.target, buffer + ", думал забанить меня? WeirdChamp ")
            else:
                with open('privet.txt', 'r', encoding='utf-8') as c:
                    privit = list(c)
                    randommm = random.choice(privit)
                    randommm = re.sub("\n", '', randommm)
                    privet = str.replace(message, '+привет ', '')
                    privet = re.sub("\n", '', privet)
                    self.connection.privmsg(event.target, buffer + " передаёт " + randommm + " привет " + privet + " peepoHey peepoLove")


    @staticmethod
    def _parse_nickname_from_twitch_user_id(user_id):
        return user_id.split('!', 1)[0]


def main():
    my_bot = VBot(HOST, PORT, USERNAME, PASSWORD, CHANNEL)
    my_bot.start()


if __name__ == '__main__':
    main()
