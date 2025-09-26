n = int(input('Enter number of elements in list (more than 2): '))
List = []
for i in range(n):
    List.append(int(input('Enter element: ')))

print('Your list:')
print(List)

# find two max elements
Max1 = List[0]
Max2 = List[1]
for i in range(2, n):
    if List[i] > Max1:
        if Max1 > Max2:
            Max2 = Max1
        Max1 = List[i]
    else:
        if List[i] > Max2:
            if Max2 > Max1:
                Max1 = Max2
            Max2 = List[i]

print(Max1, Max2)
    
