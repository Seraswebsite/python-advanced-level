class Dog:
    def make_sound(self):
        return "Woof Woof"

class Cat:
    def make_sound(self):
        return "Meow"

def animal_party(animal_object):
    print(animal_object.make_sound())
my_dog = Dog()
my_cat = Cat()
print("Dog says:")        
animal_party(my_dog) 
print("cat says:")
animal_party(my_cat)   