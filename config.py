import os
from dotenv import load_dotenv

load_dotenv()

CHAN = os.getenv("CHAN", "JesusAVGN")

BROADCASTER_ID = os.getenv("BROADCASTER_ID", "34711476")
OAUTH = os.getenv("OAUTH")
CLIENT_ID = os.getenv("CLIENT_ID")
BOT = os.getenv("BOT", "SLONB0T")
CHANNELS = [f'{CHAN}']
head = {"Authorization": os.getenv("INTERNAL_API_KEY", "")}
buferchanged = False
istopcliprunning = False
helpUrl = "https://pastebin.com/raw/837UKBqp"
abreviationsUrl = "https://pastebin.com/raw/h546CMvM"
api_url = "https://slon-api.herokuapp.com"
