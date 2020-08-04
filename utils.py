import config
import urllib.request
import urllib.response
import nturl2path
import json
import time
import _thread
from time import sleep


def mess(sock, mess):
    sock.send(("PRIVMSG #" + config.CHAN + " :" + mess+ "\r\n").encode("utf-8"))



def fillOptionList():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/jesusavgn/chatters"
            request = urllib.request.Request(url,headers={"accept": "*/*"})
            response = urllib.request.urlopen(request).read()
            if response.find("502 bad gateway") == -1:
                config.oplist.clear()
                data = json.loads(response)
                for p in data["chatters"]["moderators"]:
                    config.oplist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    config.oplist[p] = "global_mod"
                for p in data["chatters"]["admins"]:
                    config.oplist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    config.oplist[p] = "staff"
                for p in data["chatters"]["viewers"]:
                    config.oplist[p] = "viewer"
        except:
            "ERROR"
        sleep(5)



def inOp(user):
    return user in config.oplist