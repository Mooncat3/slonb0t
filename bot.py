import config
import utils
import socket
import re
import time
from time import sleep
from random import randint


def main():
    s = socket.socket()
    s.connect((config.HOST,config.PORT))
    outputPassMsg = "PASS " + config.PASS + "\r\n"
    s.send(outputPassMsg.encode('utf-8'))

    outputNickMsg = "NICK " + config.NICK + "\r\n"
    s.send(outputNickMsg.encode('utf-8'))

    outputChanMsg = "JOIN #"+config.CHAN+" \r\n"  # Change this to your channel name
    s.send(outputChanMsg.encode('utf-8'))

    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("POND :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = chat_message.sub("",response)
            print(response)

            if message.strip() == "-а":
                utils.mess(s,"хуй на")
            if message.strip() == "кто":
                utils.mess(s, "я")
            if message.strip() == "-нет":
                utils.mess(s,"осуждающий ответ")
            if message.strip() == "-привет":
                utils.mess(s,"@" + username.strip() + " иди нахуй")
            try:
                subject = response[response.index("-сделать")+len("-сделать")+1:len(response)]
                sunject = re.sub("\n", '', subject)
                ran = randint(0, 15)
                if ran == 0:
                    utils.mess(s, "@" + username.strip() + " держит " + sunject  + " в рабстве EZ")
                if ran == 1:
                    utils.mess(s, "@" + username.strip() + " посадил " + sunject + " на бутылку monkaW")
                if ran == 2:
                    utils.mess(s, "@" + username.strip() + " погдалил " + sunject + " PETTHEBASHNYA")
                if ran == 3:
                    utils.mess(s, "@" + username.strip() + " заставляет " + sunject + " смотреть аниме AYAYA")
                if ran == 4:
                    utils.mess(s, "@" + username.strip() + " уговаривает " + sunject + " отвиснуть вместе с ним peepoRIP")
                if ran == 5:
                    utils.mess(s, "@" + username.strip() + " и " + sunject + " вместе занялись страстным SEK$$OM YEP")
                if ran == 6:
                    utils.mess(s, "@" + username.strip() + " рассмешил " + sunject + " так что он умер roflanPominy")
                if ran == 7:
                    utils.mess(s, "@" + username.strip() + " оценил COCK " + sunject + " YEP")
                if ran == 8:
                    utils.mess(s, "@" + username.strip() + " слил голые фотки " + sunject + " SALAMI")
                if ran == 9:
                    utils.mess(s, "@" + username.strip() + " подрочил на " + sunject + " SALAMI , а тот в ответ тоже monkaW")
                if ran == 10:
                    utils.mess(s, "@" + username.strip() + " не был готов к тому, что его изнасилует " + sunject + " monkaW")
                if ran == 11:
                    utils.mess(s, "@" + username.strip() + " доказал всему миру, что " + sunject + " - гей PogU")
                if ran == 12:
                    utils.mess(s, "@" + username.strip() + " обожает " + sunject + " <3")
                if ran == 13:
                    utils.mess(s, "@" + username.strip() + " увидел " + sunject + " и его вырвало (puke)")
                if ran == 14:
                    utils.mess(s, "@" + username.strip() + " вынес " + sunject + " мозги WAYTOODANK")
                if ran == 15:
                    utils.mess(s, "@" + username.strip() + " раздел " + sunject + " PogU")
            except:
                print("а нет")
            if message.strip() == "-время":
                utils.mess(s, "чичас " + str(time.strftime("%H:%M", time.localtime())) + " по МСК Waiting")
            if message.strip() == "-я":
                ran = randint(0, 22)
                if ran == 0:
                    utils.mess(s, "@" + username.strip() + " сходил на крупное мероприятие и заразился короной… roflanPominy")
                if ran == 1:
                    utils.mess(s, "@" + username.strip() + " внезапно произошёл танцевальный приступ и он не может остановиться catJAM")
                if ran == 2:
                    utils.mess(s, "catJAM " + "@" + username.strip() + " сдох как лох catJAM")
                if ran == 3:
                    utils.mess(s, "@" + username.strip() + " насрал в кувшин dedU")
                if ran == 4:
                    utils.mess(s, "@" + username.strip() + " по рофлу прикинулся черешней peepoRIP")
                if ran == 5:
                    utils.mess(s, "@" + username.strip() + " - самый гейский гей в чате KappaPride")
                if ran == 6:
                    utils.mess(s, "@" + username.strip() + " неуважает смерть слона WeirdChamp")
                if ran == 7:
                    utils.mess(s, "@" + username.strip() + " увидел в узком переулке тёмный силуэт monkaW")
                if ran == 8:
                    utils.mess(s, "@" + username.strip() + " поив пiльмiнив peepoPizza")
                if ran == 9:
                    utils.mess(s, "@" + username.strip() + " выйграл миллион долларов PogChamp")
                if ran == 10:
                    utils.mess(s, "@" + username.strip() + " любит котиков peepoShy")
                if ran == 11:
                    utils.mess(s, "У " + "@" + username.strip() + " кто то стоит сзади monkaW")
                if ran == 12:
                    utils.mess(s, "У " + "@" + username.strip() + " спина белая widepeepoHappy")
                if ran == 13:
                    utils.mess(s, "@" + username.strip() + " хочет питсы peepoPizza")
                if ran == 14:
                    utils.mess(s, "Агент госдепа " + "@" + username.strip() + " продолжает собирать под прикрытием информацию о чате HACKERMANS")
                if ran == 15:
                    utils.mess(s, "@" + username.strip() + " мечтает о COCK стримера YEP")
                if ran == 16:
                    utils.mess(s, "@" + username.strip() + " плавал в море и увидел акулу monkaW")
                if ran == 17:
                    utils.mess(s, "@" + username.strip() + " в прошлой жизни был сквирт-мастером pepeWOW")
                if ran == 18:
                    utils.mess(s, "@" + username.strip() + " забанил папича D:")
                if ran == 19:
                    utils.mess(s, "@" + username.strip() + " был засужен за воровство девственности BOP")
                if ran == 20:
                    utils.mess(s, "@" + username.strip() + " - король юмора EZ")
                if ran == 21:
                    utils.mess(s, "@" + username.strip() + " снял тикток PogO и попал в кринж тиктока KeK")
                if ran == 22:
                    utils.mess(s, "@" + username.strip() + " сидит один дома и грустит FeelsRainMan")
        sleep(1)








if __name__ == '__main__':
    main()