class Smartphone:
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price


class GamingPhone(Smartphone):
    def __init__(self, brand, price, cooling_system):
        super().__init__(brand, price)
        self.cooling_system = cooling_system


my_phone = GamingPhone("ASUS ROG", 85000, "Vapor Chamber")

print("Brand:", my_phone.brand)
print("Price:", my_phone.price)
print("Cooling System:", my_phone.cooling_system)