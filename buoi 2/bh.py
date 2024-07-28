class NhanVien: 
    def __init__(self, name , age):
        self.name = name
        self.age = age
class ChinhThuc(NhanVien):
    def __init__(self,name,age,basic_salary,multiplier_salary):
        super().__init__(name,age)
        self.basic_salary = basic_salary
        self.multiplier_salary = multiplier_salary
    def calculate_salary(self) : 
        return self.basic_salary + self.multiplier_salary 
John = ChinhThuc("John",19,6000,1.5)
class ThoiVu(NhanVien): 
    def __init__(self,name,age,hourly_rate,hours_worked):
        super().__init__(name,age)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
    def calc_salary(self) : 
        return self.hourly_rate * self.hours_worked
Phil = ThoiVu("Phil",20,2,8)
class Department: 
    def __init__(self, room_name):
        self.room_name = room_name
        self.employees = []
    def add_employee(self, employee):
        self.employees.append(employee)
    def remove_employee(self,employee):
        self.employees.remove(employee)
    def list_employee(self):
        for employee in self.employees:
            print(employee.name)
employee1 = NhanVien("john",20)
employee2 = NhanVien("huy",19)
department = Department("Chi nhánh Bình Thạnh")
department.add_employee(employee1)
department.add_employee(employee2)
department.remove_employee(employee1)
department.list_employee()


