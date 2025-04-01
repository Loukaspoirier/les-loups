from abc import ABC, abstractmethod

class School(ABC):
    
    def __init__(self, name):
        self.__name = name # dunder

    @property
    def name(self):
        print('call name property')
        return self.__name

    def get_name(self):
        return self.__name

    @abstractmethod
    def subscribe(self):
        pass

class Hexagone(School):

    def __init__(self, teacher = None):
        super().__init__('hexagone')

    def subscribe(self):
        print('subscribe new student')

class Sqy(School):
    def __init__(self, teacher = None):
        super().__init__('sqy')

    def subscribe(self):
        print('subscribe new student')


def use_school():
    hexagone = School('hexagone')
    print(__name__, hexagone, hexagone.get_name())   

hexagone = Hexagone()
print(__name__, hexagone, hexagone.name)
sqy = Sqy('sqy')
sqy.students = ['student1', 19] # [] {} () set()
print(sqy.students)
#print(hexagone.students)
