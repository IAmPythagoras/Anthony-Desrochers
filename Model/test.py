def allo(x):
    print(x)

def hey(x):
    print('hey'+str(x))

x = [allo, hey]


class test:

    def __init__(self, name : str):
        self.name = name

    def tw(self):
        print(self.name)

class test2(test):

    def __init__(self, name, name2):
        super().__init__(name)
        self.name2 = name2

    def t(self):
        print(self.name+self.name2)

x = test("a")
y = test2("b","c")

y.t()

x.tw()




