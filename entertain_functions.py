import random

d = 'entertain_files'

search = [x for x in open(f'{d}/search.txt', encoding='utf-8').read().split('\n') if len(x) > 1]
things = [x for x in open(f'{d}/things.txt', encoding='utf-8').read().split('\n') if len(x) > 1]
stories = [x for x in open(f'{d}/stories.txt', encoding='utf-8').read().split('\n') if len(x) > 1]
me_classic = [x for x in open(f'{d}/meme.txt', encoding='utf-8').read().split('\n') if len(x) > 1]
clothes = [x for x in open(f'{d}/clothes.txt', encoding='utf-8').read().split('\n') if len(x) > 1]
first_names = [x for x in open(f'{d}/first_names.txt', encoding='utf-8').read().split('\n') if len(x) > 1]
do_classic = [x for x in open(f'{d}/do.txt', encoding='utf-8').read().split('\n') if len(x) > 1]
social = [x for x in open(f'{d}/social.txt', encoding='utf-8').read().split('\n') if len(x) > 1]
passwords = [x for x in open(f'{d}/passwords.txt', encoding='utf-8').read().split('\n') if len(x) > 1]
furniture = [x for x in open(f'{d}/furniture.txt', encoding='utf-8').read().split('\n') if len(x) > 1]
body = [x for x in open(f'{d}/body.txt', encoding='utf-8').read().split('\n') if len(x) > 1]
feels = [x for x in open(f'{d}/feels.txt', encoding='utf-8').read().split('\n') if len(x) > 1]
fruits = [x for x in open(f'{d}/fruits.txt', encoding='utf-8').read().split('\n') if len(x) > 1]


def me(nickname, names):
    currency = ['доллар', 'евро']
    symbols = ['$', '₽']
    stst = ['украл', 'решил украсть', 'спёр', 'отобрал', 'решил забрать себе', 'мечтает украсть', 'хочет украсть',
            'похищает']
    curr = random.choice(symbols)
    currency_rand = random.choice(currency)
    thing = random.choice(things)
    answer = random.choice(me_classic).format(nickname)
    name = random.choice(names)
    v = random.uniform(0, 100)
    kol = round(random.uniform(1, 5000), 1)
    if 0 < v <= 17:
        rand_num = random.randint(0, 100)
        if 0 < rand_num <= 95:
            answer = random.choice(search).format(nickname, random.choice(things))
        else:
            answer = random.choice(search).format(nickname, name)
    if 17 < v <= 17.5:
        kol = round(random.uniform(90, 250), 1)
        answer = f"Однажды {nickname} приснился сон, что {currency_rand} теперь стоит {kol} ₽! Ужасный сон WutFace"
    if 17.5 < v <= 18:
        kol = round(random.uniform(0, 40), 1)
        answer = f"Однажды {nickname} приснился сон, что {currency_rand} теперь стоит {kol} ₽! Вот это сон Kreygasm"
    if 18 < v <= 35:
        answer = random.choice(stories).format(nickname, name, thing)
    if 35 < v <= 79:
        answer = random.choice(me_classic).format(nickname)
    if 79 < v <= 80:
        answer = f'{nickname} умрёт через {random.randint(1, 30)} дней roflanPominy'
    if 80 < v <= 81:
        answer = f'У {nickname} - {random.randint(80, 200)} IQ WAYTOOSMART Clap'
    if 81 < v <= 88:
        answer = f'{nickname} {random.choice(stst)} у {name} {thing} BOP'
    if 88 < v <= 89:
        answer = f'{nickname} {random.choice(stst)} у {name} {kol} {curr} BOP'
    if 89 < v <= 92:
        answer = f'{nickname} хвастается {random.choice(clothes)} за {kol} {curr} 💸 peepoCool'
    if 92 < v <= 93:
        answer = f'{nickname} выиграл в лотерее {kol} {curr} Поздравляем!'
    if 93 < v <= 93.5:
        random_date = f'{random.randint(1, 30)}.{random.randint(1, 12)}.{random.randint(2021, 2030)}'
        answer = f'{nickname} сегодня прошёл тест на дату смерти. monkaW Дата смерти {nickname} - {random_date} ' \
                 f'roflanPominy'
    if 93.5 < v <= 96:
        name2 = random.choice(names)
        answer = f'{nickname} решил украсть у {name} {thing} , но в чате пробежал {name2} и засёк ' \
                 f'преступление monkaFLASH {nickname} теперь за решёткой BOP'
    if 96 < v <= 98:
        age = random.randint(1, 100)
        answer = f'{nickname} скрывает свой возраст. Но я знаю, что {nickname} уже {age} blushW'
    if 98 < v <= 100:
        first_name = random.choice(first_names)
        answer = f'{nickname} скрывает своё имя. Но я знаю, что {nickname} на самом деле зовут {first_name} monkaX'
    return answer


def do(nickname, mess, names):
    symbols = ['$', '₽']
    games = ['карты', 'города', 'кости', 'крестики-нолики', 'нарды']
    steal_list = ['украл', 'решил украсть', 'спёр', 'отобрал', 'решил забрать себе', 'мечтает украсть', 'хочет украсть',
                  'похищает', 'крадёт']
    ride = ['помчались', 'поехали', "пошли пешком", "поехали на велосипеде", "побежали"]
    curr = random.choice(symbols)
    games_rand = random.choice(games)
    thing = random.choice(things)
    answer = random.choice(do_classic).format(nickname, mess, random.choice(ride))
    name = random.choice(names)
    kol = round(random.uniform(0, 4500), 1)
    v = random.uniform(0, 100)
    if 20 < v <= 21:
        answer = f'{nickname} играл в {games_rand} с {mess} и проиграл {thing} Sadge'
    if 21 < v <= 22:
        answer = f'{nickname} играл в {games_rand} с {mess} и выиграл {thing} PogChamp'
    if 22 < v <= 24:
        answer = f'{nickname} занял у {mess} {kol} {curr}'
    if 24 < v <= 25:
        answer = f'{nickname} и {mess} спокойно сидели вместе. Но вдруг на них свалился {name} blushW'
    if 25 < v <= 55:
        answer = random.choice(stories).format(nickname, mess, thing)
    if 55 < v <= 56:
        answer = random.choice(search).format(nickname, mess)
    if 56 < v <= 56.5:
        first_name = random.choice(first_names)
        answer = f'{nickname} накурился с {mess}. А на утро {nickname} решает, что его имя - {first_name} 🥴'
    if 56.5 < v <= 58:
        answer = f'{nickname} {random.choice(steal_list)} у {mess} {thing} BOP'
    if 58 < v <= 59:
        gift = ["подарил", "дарит", "решил подарить", "отдаёт", "решил отдать", "отдал на срок"]
        answer = f'{nickname} {random.choice(gift)} {mess} {thing}'
    if 59 < v <= 60:
        answer = f'{nickname} хвастается для {mess} {random.choice(clothes)} peepoCool'
    if 60 < v <= 60.5:
        pointing = ["указывает", "показывает", "просит посмотреть"]
        answer = f'{nickname} {random.choice(pointing)} {mess} на {thing}'
    if 60.5 < v <= 61:
        result_pass = random.choice(passwords) + random.choice(passwords) + random.choice(passwords)
        answer = f'{nickname} взломал {random.choice(social)} {mess}. Пароль: {result_pass}'
    if 61 < v <= 61.5:
        answer = f'{nickname} и {mess} {random.choice(ride)} на круизное путешествие. Но вдруг они встретили {name},' \
                 f' который {random.choice(steal_list)} у них {thing} KEKWait BOP'
    if 61.5 < v <= 63:
        answer = f'{nickname} похищает {mess} и требует выкуп суммой {kol} {curr}'
    if 63 < v <= 77:
        answer = random.choice(search).format(nickname, mess)
    if 77 < v <= 79:
        answer = f'{nickname} приклеивает {mess} к {random.choice(furniture)}'
    if 79 < v <= 81:
        answer = f'{nickname} {random.choice(feels)} шутит про {random.choice(body)} {mess}'
    if 81 < v <= 83:
        nick_win = random.choice([nickname, mess])
        answer = f'{nickname} и {mess} устроили битву подушками! Победу одерживает {nick_win}'
    if 83 < v <= 84:
        answer = f'{nickname} потерял {thing}, но {mess} нашёл и отдал {thing} {nickname} peepoFlower'
    if 84 < v <= 85:
        answer = f'{nickname} и {mess} играли в орёл и решку. Победу одержал {random.choice([nickname, mess])}' \
                 f' PepoCheer'
    if 85 < v <= 87:
        answer = f'{nickname} спокойно сидел с {mess} пока тот не начал тыкать в окно. {nickname} обернулся и увидел' \
                 f', что {mess} тыкал в {thing}'
    if 87 < v <= 89:
        answer = f'{nickname} кушает фрукты и дарит {random.choice(fruits)} {mess} pukEat'
    if 89 < v <= 90:
        answer = f'Однажды {nickname} нашёл {thing}. Оказывается, что {thing} потерял {mess} Thonk'
    return answer


def steal(nickname, mess):
    v = random.uniform(0, 100)
    kol = round(random.uniform(0, 4500), 1)
    symbols = ['$', '₽']
    st = ["ничего не украл у {}", "ничего не смог украсть у {}", 'пытался украсть что-либо у {}, но не вышло']
    st_2 = ['украл', 'решил украсть', 'спёр', 'отобрал', 'решил забрать себе', 'мечтает украсть', 'хочет украсть',
            'похищает']
    thing = random.choice(things)
    if 0 < v <= 60:
        v_2 = random.uniform(0, 100)
        if 0 < v_2 <= 85:
            v_3 = random.uniform(0, 100)
            if 0 < v_3 <= 90:
                answer = f'{nickname} {random.choice(st_2)} у {mess} {thing} BOP'
            else:
                answer = f'{nickname} пытался своровать у {mess} {thing} , но, внезапно {mess}' \
                         f' сам украл у {nickname} {random.choice(things)} blushW'
        else:
            answer = f'{nickname} украл у {mess} {kol} {random.choice(symbols)} BOP'
    else:
        answer = f'{nickname} {random.choice(st).format(mess)} KEKW 👉 Lohich'
    return answer
