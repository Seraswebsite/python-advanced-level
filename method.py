class animal:
    def make_sound(self):
        print("Animal makes differnt sound")

class Dog(animal):
    def make_sound(self):
        print("Dog says: Woof woof")

class Cat(animal):
    def make_sound(self):
        print("Cat says: Meow Meow")

my_dog = Dog()
my_dog.make_sound()        

my_cat = Cat()
my_cat.make_sound() 