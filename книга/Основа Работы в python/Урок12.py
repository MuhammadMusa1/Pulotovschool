def decode(code, w):
    res = ''
    for elem in code:
        if elem[1] == w:
            res = elem[0]
    return res
        
code = [['а', '0000'],
        ['п', '0001'],
        ['к', '0010'],
        ['т', '0011'],
        ['е', '0100'],
        ['о', '0101'],
        ['у', '0110'],
        ['в', '0111'],
        ['м', '1000'],
        ['р', '1001'],
        [' ', '1010']]

message = input()

result = ''
word = ''
i = 0
for sign in message:
    word = word + sign
    i = i + 1
    if i == 4:
        result = result + decode(code, word)
        i = 0
        word = ''
print(result)
