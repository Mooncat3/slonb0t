words = input() #вводимое предложение
with open('data/osujdau.txt', 'r', encoding='utf_8') as f:
    l = [line.strip() for line in f]
    if any(x in words for x in l):
        print('НАЙДЕНО ОСУДИТЕЛЬНОЕ СЛОВО')
    else:
        print('НЕ НАЙДЕНО ОСУДИТЕЛЬНЫХ СЛОВ')
