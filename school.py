class School:
    
    def __init__(self, name):
        self.__name = name # dunder

    @property
    def name(self):
        print('call name property')
        return self.__name

    def get_name(self):
        return self.__name

def use_school():
    hexagone = School('hexagone')
    print(__name__, hexagone, hexagone.get_name())   

hexagone = School('hexagone')
print(__name__, hexagone, hexagone.name)
sqy = School('sqy')
sqy.students = ['student1', 19] # [] {} () set()
print(sqy.students)
#print(hexagone.students)
