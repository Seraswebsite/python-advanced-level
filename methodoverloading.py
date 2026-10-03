class calculator:
    def add(self, a, b, c = None):
        if c != None:
            print(f"Sum of 3 number:{a + b + c}")
        else:
            print(f"Sum of 2 number:{a+b}")

my_cal = calculator()
my_cal.add(10,20)
my_cal.add(10,20,50)            