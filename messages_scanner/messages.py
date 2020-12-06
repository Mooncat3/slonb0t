import requests
import datetime

nickname = ''

Client_ID = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
OAUTH = 'l4tt0z3a94edvjo3kbs0c3s4qimpsp'
url = 'https://api.twitch.tv/gql'
head = {'Authorization': f'OAuth {OAUTH}', 'Client-ID': Client_ID}
head_2 = {'Authorization': f'Bearer {OAUTH}', 'Client-ID': Client_ID}
hash_name = '2c484f8a5ff63f06732707c8ca989083e46b2aa81a03b02e7ac7b9aa9fcba9a2'
url_2 = f'https://api.twitch.tv/helix/users?login={nickname}'
mess_count = 0
try: sender = requests.get(url_2, headers=head_2).json()['data'][0]['id']
except IndexError: sender = 0
data_loop = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ|0')
while True:
    try:
        json_msg = [{"operationName":"ViewerCardModLogsMessagesBySender","variables":{"senderID":sender,"channelLogin":"jesusavgn","cursor":data_loop,"includeAutoModCaughtMessages":True},"extensions":{"persistedQuery":{"version":1,"sha256Hash":hash_name}}}]
        r = requests.post(url, headers=head, json=json_msg).json()[0]['data']['channel']['modLogs']['messagesBySender']['edges']
        if len(r) == 0: break
        a = [b['cursor'] for b in r if 'sentAt' in b['node']]
        data_loop = a[-1]
        mess_count += len(a)
    except KeyError: break
print(f'Пользователь {nickname} написал {mess_count} сообщений | Дата первого сообщения: {data_loop.split("T")[0]}')
