 
#bai 1 
class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def say_hi(self):
        print(f"Hi, my name is {self.name}.")

    def tell_position(self):
        print(f"I am a {self.position}.")

john = Employee("John", "Software Engineer")
john.say_hi()
john.tell_position()
#bai 2
import math 
class Rectangle:
    def __init__(self, cd, cr): 
        self.cd = cd
        self.cr = cr

    
    def cv(self):  
        return 2 * (self.cd + self.cr)

    def dt(self):  
        return self.cd * self.cr

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def cv2(self):
        return 2 * math.pi * self.radius

    def dt2(self):
        return math.pi * self.radius ** 2


shape_type = input("Shape (rectangle|circle): ")
if shape_type == "rectangle":
    cd = int(input("Nhập cd :"))
    cr = int(input("Nhập cr :"))
    rectangle = Rectangle(cd, cr)
    print(f"Chu vi hình chữ nhật là {rectangle.cv()}.")
    print(f"Diện tích hình chữ nhật là {rectangle.dt()}.")
elif shape_type == "circle":
    radius = int(input("Nhập radius :"))
    circle = Circle(radius)
    print(f"Chu vi hình tròn là {circle.cv2()}.")
    print(f"Diện tích hình tròn là {circle.dt2()}.")
else:
    print("Invalid shape type")
#bai 3
from datetime import datetime
class CustomDate:
    def __init__(self):
        self.now = datetime.now()

    def get_date(self):
        return self.now.strftime("%d/%m/%Y")

    def get_time(self):
        return self.now.strftime("%H:%M:%S")

now = CustomDate()
print(now.get_date())
print(now.get_time())
#bai 4
from datetime import datetime

class DateHandler:
    
    def format_date(date):
        return date.strftime("%d/%m/%Y")

    def get_days_between(date1, date2):
        return abs((date2 - date1).days)

start_date = datetime(2021, 1, 1)
end_date = datetime(2022, 1, 1)
print("Start:", DateHandler.format_date(start_date))
print("End:", DateHandler.format_date(end_date))
print("Days between:", DateHandler.get_days_between(start_date, end_date))


