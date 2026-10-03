class Greeter:

    def say_hello(self, name1, name2=None):

        if name2 != None:
            print(f"Hello {name1} and {name2}!")
        else:
            print(f"Hello {name1}!")


my_greeter = Greeter()

my_greeter.say_hello("Samarihi")
my_greeter.say_hello("Samarihi", "Sara")