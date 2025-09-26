a = int(input('Enter first number: '))
b = int(input('Enter second number: '))
sign = input('Enter a sign of operation: ')
if sign == '+':
    print(a, '+', b, '= ', a + b)
elif sign == '-':
    print(a, '-', b, '= ', a - b)
elif sign == '*':
    print(a, '*', b, '= ', a * b)
elif sign == '/':
    print(a, '/', b, '= ', a / b)
else:
    print('unknow operation')
