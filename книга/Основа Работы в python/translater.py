def translate(TList, word, lang):
    if lang == 'А':
        n = 0
        nreturn = 1
    else:
        n = 1
        nreturn = 0

    numwords = len(TList)
    i = 0
    EndofTList = False
    while word != TList[i][n] and not EndofTList:
        i += 1
        if i == numwords:
            EndofTList = True
            return 'Перевод не найден'
    if i < numwords:
        return TList[i][nreturn]
            

Translate = [['house', 'дом'],
             ['mouse','мышка'],
             ['window', 'окно'],
             ['mother', 'мама'],
             ['car', 'автомобиль'],
             ['sky', 'небо'],
             ['sun', 'солнце'],
             ['city', 'город'],
             ['school', 'школа'],
             ['ball', 'мяч']]


print('---Вас приветствует англо-русский переводчик---')
print('Если вы хотите переводить с английского на русский введите - А')
print('Если вы хотите переводить с русского на английский введите - Р')
lang = input()
while lang != 'А' and lang != 'Р':
    lang = input('Введите либо - А, либо - Р на русской раскладке: ')

Work = True
while Work:
    word = input('Введите слово: ')
    translateword = translate(Translate, word, lang)
    print('Перевод: ', translateword)

    print('Хотите продолжить? Если да, введите - "Y"')
    a = input()
    if a != 'Y':
        Work = False
