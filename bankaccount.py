class Digital_wallet:
    def __init__ (self,username, wallet_id, money):
        self.username = username
        self.wallet_id = wallet_id
        self.money = money
    
    def get_money(self):
        return self.__money

my_wallet = Digital_wallet("Sera","W1025", "2500")

print(f"Acco Owner:{my_wallet.username}")
print(f"pin:{my_wallet.wallet_id}")
print(f"money:{my_wallet.money}")