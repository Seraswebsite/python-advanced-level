class Manager:
    def get_bonus(self):
        return "Manager bonus is 5000 TK."


class Developer:
    def get_bonus(self):
        return "Developer bonus is 3000 TK."


def show_bonus(employee_object):
    print(employee_object.get_bonus())


manager = Manager()
developer = Developer()

show_bonus(manager)
show_bonus(developer)