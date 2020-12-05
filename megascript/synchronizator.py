import requests
import datetime
import json
import time


Client_ID = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
OAUTH = 'l4tt0z3a94edvjo3kbs0c3s4qimpsp'
url = 'https://gql.twitch.tv/gql'
head = {'Authorization': f'OAuth {OAUTH}', 'Client-ID': Client_ID}
head_2 = {'Authorization': f'Bearer {OAUTH}', 'Client-ID': Client_ID}
hash_name = '2c484f8a5ff63f06732707c8ca989083e46b2aa81a03b02e7ac7b9aa9fcba9a2'
cursor = ''
ii = 0
while True:
    time_start = time.time()
    data_2 = requests.get(f'https://api.twitch.tv/helix/users/follows?to_id=34711476&first=100&after={cursor}', headers=head_2).json()
    cursor = data_2['pagination']['cursor']
    chatters = [user['from_name'] for user in data_2['data']]
    for user in chatters:
        should_pass = False
        answer = requests.get(f"https://sl0n.herokuapp.com/stats/jesusavgn?nickname={user}", headers={"Authorization": "y5IArL6S&%%G(69G"}).json()
        if answer['type'] == 'success':
            if 'count_state' in answer['answer'].keys():
                if answer['answer']['count_state'] > 1:
                    should_pass = True

        r = requests.get("https://api.streamelements.com/kappa/v2/chatstats/jesusavgn/stats")
        json_r = r.json()['chatters']

        listnames = {}
        for i in range(0, 100):
            listnames[json_r[i]['name']] = json_r[i]['amount']

        if should_pass:
            print(f"//-------- Данный пользователь уже синхронизирован! {user} --------//")
        elif user in listnames.keys():
            requests.post("https://sl0n.herokuapp.com/stats/jesusavgn",
                            data={'type': 'clear', 'nickname': user},
                            headers={"Authorization": "y5IArL6S&%%G(69G"})
            requests.post("https://sl0n.herokuapp.com/stats/jesusavgn",
                            data={'type': 'add', 'nickname': user, 'count': listnames[user]},
                            headers={"Authorization": "y5IArL6S&%%G(69G"})
        else:
            try:
                print(f"//-------- Сканирование сообщений {user} --------//")
                requests.post("https://sl0n.herokuapp.com/stats/jesusavgn",
                                data={'type': 'clear', 'nickname': user},
                                headers={"Authorization": "y5IArL6S&%%G(69G"})
                a = []
                url_2 = 'https://api.twitch.tv/helix/users?login=' + user
                try:
                    sender = requests.get(url_2, headers=head_2).json()['data'][0]['id']
                except:
                    sender = 0
                start = datetime.datetime.today()
                data_loop = start.strftime('%Y-%m-%dT%H:%M:%SZ|0')
                while True:
                    try:
                        json_msg = [{"operationName":"ViewerCardModLogsMessagesBySender","variables":{"senderID":sender,"channelLogin":"jesusavgn","cursor":data_loop,"includeAutoModCaughtMessages":True},"extensions":{"persistedQuery":{"version":1,"sha256Hash":hash_name}}}]
                        r = requests.post(url, headers=head, json=json_msg)
                        r_json = r.json()[0]['data']['channel']['modLogs']['messagesBySender']['edges']
                        if len(r_json) < 2:
                            break
                        for b in r_json:
                            try:
                                b['node']['sentAt']
                                a.append(b['cursor'])
                            except:
                                pass
                        data_loop = a[-1]
                    except Exception as e:
                        print(e)
                        break
                mess_count = len(set(a))
                requests.post("https://sl0n.herokuapp.com/stats/jesusavgn",
                                data={'type': 'add', 'nickname': user, 'count': mess_count},
                                headers={"Authorization": "y5IArL6S&%%G(69G"})
                print(f'Пользователь {user} написал {mess_count} сообщений')
            except Exception as e:
                print(e)
    ii += 100
    print(f"//---------------- ПРОСКАНИРОВАНО: {ii} | {time.time()-time_start} сек. ----------------//")
