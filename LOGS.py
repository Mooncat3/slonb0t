import AdditionalMethods
import requests
import time
from github import Github

with open(file='data/TRASHMASSIVE.txt', mode='r', encoding='utf-8') as q:
    strer = q.read()

g = Github("f0011283768114fac26230cd23b3208ed10d0a54")

repo = g.search_repositories("slonb0t")[0]
repo.create_file("data/TRASHMASSIVE.txt", "Automated Upload from Bot", strer)

time.sleep(300)