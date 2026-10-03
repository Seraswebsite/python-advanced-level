class Counter:
    def __init__(self, value):
        self.value = value

    def __bool__(self):
        return self.value > 0


def test(counter):
    if counter:
        print("Counter = True")
    else:
        print("Counter = False")


counter1 = Counter(3)
test(counter1)