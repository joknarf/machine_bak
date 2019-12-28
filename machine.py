from enum import Enum

class Rack:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price
        self.quantity = 0

class Coin(Enum):
    NICKEL = 5
    DIME = 10
    QUARTER = 25
    DOLLAR = 100

class Machine:
    def __init__(self, racks, coin_count=0):
        self.racks = {}
        self.coins = {
            Coin.DOLLAR: coin_count,
            Coin.QUARTER: coin_count,
            Coin.DIME: coin_count,
            Coin.NICKEL: coin_count,
        }
        for rack in racks:
            self.racks[rack.code] = rack
        self.amount = 0
        self.coins_list = list(self.coins.keys()) # need ordered list

    def refill(self, code, quantity):
        self.racks[code].quantity += quantity

    def insert(self, coin):
        self.coins[coin] += 1
        self.amount += coin.value

    # Recursive calls to find right coins combination to give change
    def __calc_change(self, change, coins, val=0, coins_i=0):
        if val == change:
            return coins
        if val > change:
            return None
        for i in range(coins_i, len(coins)):
            coin_type = self.coins_list[i]
            if coins[coin_type] == 0:
                continue
            ccoins = coins.copy()
            ccoins[coin_type] -= 1
            ccoins = self.__calc_change(change, ccoins, val+coin_type.value, i)
            if ccoins:
                return ccoins
        return None

    def __give_change(self, change):
        new_coins = self.__calc_change(change, self.coins)
        if new_coins:
            back_coins = []
            for key, val in self.coins.items():
                nbc = val - new_coins[key]
                if nbc > 0:
                    back_coins.append(f'{nbc} {key.name}')
            print(f'Change: {change} ({", ".join(back_coins)})')
            self.coins = new_coins
            self.amount = 0
            return True
        return False


    def press(self, code):
        if self.amount >= self.racks[code].price:
            if self.racks[code].quantity > 0:
                change = self.amount - self.racks[code].price
                if self.__give_change(change):
                    self.racks[code].quantity -= 1
                else:
                    print("no change available")
                    self.__give_change(self.amount)
            else:
                print("product not available")
                self.__give_change(self.amount)
        else:
            print("not enough money")
