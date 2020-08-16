import socket
import config
import sys
import json
import time



def go_for_message():
    id = int(sys.argv[1])
    s = socket.socket()
    s.connect(("irc.twitch.tv", 6667))
    outputPassMsg = "PASS oauth:" + config.OAUTH + "\r\n"
    s.send(outputPassMsg.encode('utf-8'))

    outputNickMsg = "NICK " + config.BOT + "\r\n"
    s.send(outputNickMsg.encode('utf-8'))

    outputChanMsg = "JOIN #" + config.CHAN + " \r\n"  # Change this to your channel name
    s.send(outputChanMsg.encode('utf-8'))

    with open(file='data/sendmess.txt', mode='r', encoding='utf-8') as e:
        data = json.loads(e.read())
        time.sleep(data[id]['timeout'])
        mess = data[id]['mes']

    print(mess)

    s.send(("PRIVMSG #{} :{}\r\n").format(config.CHAN, mess).encode("utf-8"))

    outputChanMsg = "PART #" + config.CHAN + " \r\n"
    s.send(outputChanMsg.encode('utf-8'))



go_for_message()