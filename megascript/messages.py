import requests
from datetime import datetime

nickname = ''

Client_ID = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
OAUTH = 'l4tt0z3a94edvjo3kbs0c3s4qimpsp'
url = 'https://gql.twitch.tv/gql'
head = {'Authorization': f'OAuth {OAUTH}', 'Client-ID': Client_ID}
head_2 = {'Authorization': f'Bearer {OAUTH}', 'Client-ID': Client_ID}
a = []
url_2 = 'https://api.twitch.tv/helix/users?login=' + nickname
try:
    sender = requests.get(url_2, headers=head_2).json()['data'][0]['id']
except:
    sender = 0
start = datetime.today()
data_loop = start.strftime('%Y-%m-%dT%H:%M:%S.0Z')
while True:
    try:
        json_msg = [{"operationName":"ViewerCardModLogsMessagesBySender","variables":{"senderID":sender,"channelLogin":"jesusavgn","cursor":data_loop+"|12600c60-246e-4cc0-8b7b-0380aa0e5329","includeAutoModCaughtMessages":True},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"2c484f8a5ff63f06732707c8ca989083e46b2aa81a03b02e7ac7b9aa9fcba9a2"}}}]
        r = requests.post(url, headers=head, json=json_msg)
        r_json = r.json()[0]['data']['channel']['modLogs']['messagesBySender']['edges']
        if len(r_json) < 2:
            break
        for b in r_json:
            try:
                a.append(b['node']['sentAt'])
            except:
                pass
        if a[-1] == a[-2]:
            break
        data_loop = a[-1]
        print(len(set(a)))
    except:
        break
mess_count = len(set(a))
print(f'Пользователь {nickname} написал {mess_count} сообщений')
input()
