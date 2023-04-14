class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def clone(self):
        pass


x = 3
y = 4
pt = Point(x, y)
pt_clone = Point(clone())


T = input()
R = input()
s = T + R
if s == 'ножницыбумага' or 'каменьножницы' or 'бумагакамень':
    print('Тимур')
elif R == T:
    print('ничья')
else:
    print('Руслан')
