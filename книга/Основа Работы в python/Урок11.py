Set = {5, 6, 13, 14}

ListCont = []
L = []
cont = 0
while cont != 10:
    name = input('Enter your name: ')
    age = int(input('Enter your age: '))
    if age in Set:
        L.append(name)
        L.append(age)
        ListCont.append(L)
        L = []
        cont += 1

print('List of contestant: ')
for i in range(10):
    print(ListCont[i][0].ljust(10, ' '), ListCont[i][1])


        
