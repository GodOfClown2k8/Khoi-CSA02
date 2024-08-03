#cau 1 
class Rectangle:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def __str__(self):
        return f"Rectangle object with height = {self.height} and width = {self.width}"

rect = Rectangle(2, 1)
print(rect)
#cau 2
class MathList:
    def __init__(self, values):
        self.values = values

    def __str__(self):
        return str(self.values)

    def __add__(self, num):
        return MathList([x + num for x in self.values])

    def __sub__(self, num):
        return MathList([x - num for x in self.values])

    def __iadd__(self, num):
        self.values = [x + num for x in self.values]
        return self

    def __isub__(self, num):
        self.values = [x - num for x in self.values]
        return self

m_list = MathList([1, 2, 3, 4, 5])
print(m_list)
m_list += 2
print(m_list)
#cau 3
class Square:
    def __init__(self, side_length):
        self.side_length = side_length

    def cal_area(self):
        return self.side_length ** 2


class Cube(Square):
    def cal_area(self):
        return 6 * self.side_length ** 2

    def cal_volume(self):
        return self.side_length ** 3


square = Square(2)
print('Square area:', square.cal_area())

cube = Cube(2)
print('Cube area:', cube.cal_area())
print('Cube volume:', cube.cal_volume())
#cau 4
from datetime import datetime

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def welcome(self):
        print(f"Welcome, {self.username}")

    def check_password(self, password):
        return self.password == password


class SubscribedUser(User):
    def __init__(self, username, password, expiration_date):
        super().__init__(username, password)
        self.expiration_date = expiration_date

    def is_expired(self):
        return datetime.now() > self.expiration_date


user = User('mindx', '12345')
user.welcome()
print(user.check_password('1234'))

s_user = SubscribedUser('s_mindx', '1234', datetime(2021, 1, 1))
s_user.welcome()
print(s_user.check_password('1234'))
print(s_user.is_expired())
