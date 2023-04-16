
T = input()
R = input()
s = T + R
if s == 'ножницыбумага' or 'каменьножницы' or 'бумагакамень':
    print('Тимур')
elif R == T:
    print('ничья')
else:
    print('Руслан')
