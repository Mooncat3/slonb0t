while True:
    ss = input()
    with open('data/osujdau.txt', 'r', encoding='utf_8') as f:
        l = [line.strip() for line in f]
        if any(x in ss for x in l):
            print('ОСУЖДАЮ')
        else:
            print('НЕ ОСУЖДАЮ')