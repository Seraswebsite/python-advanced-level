from abc import ABC,abstractmethod
class Animal(ABC):
    @abstractmethod
    def sound(self):
        pass

class Dog (Animal):
    def sound(self):
        print("Dogs Say Woof Woof")
class Cat (Animal):
    def sound(self):
        print("Cats Say Meow Meow")
dog=Dog()
dog.sound()
cat=Cat()
cat.sound()