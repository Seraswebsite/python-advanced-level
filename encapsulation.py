class BankAccount:
    def __init__(self, owner, pin, balance):
        self.owner = owner
        self._pin = pin          # protected
        self.__balance = balance # private

    def get_balance(self):
        return self.__balance
                
                                     
my_account = BankAccount("Rahim", "123", "23453321")

print(f"Account Owner: {my_account.owner}")
print(f"Pin: {my_account._pin}")
print(f"Balance: {my_account.get_balance()} TK")