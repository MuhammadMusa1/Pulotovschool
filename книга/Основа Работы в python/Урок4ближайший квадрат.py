n = int(input())
x = 1
while x**2 < n:
    x = x +1

if (n - (x - 1)**2) <= (x**2 - n):
    print(x-1)
else:
    print(x)
