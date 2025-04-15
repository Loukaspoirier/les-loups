class Person :
    def__init__(self, name):
        self.name = name
    def __repr__(self):
        return f'Person(name={self.
        name})'
class PersonStorage
    def save(cls,person):
        print(f'Save the {person} to
        the database') 
if__name__=='__main__':
    p = Person('John Doe')
    Person.save(p)   