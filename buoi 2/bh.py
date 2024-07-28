class Hello : 
    def __init__(self,name):
        self.name = name
    def hello(self): 
        print(f"Hey {self.name}")

name = input("your name : ")
nothing = Hello(name)
nothing.hello()
