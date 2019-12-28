import unittest
from machine import Machine, Rack, Coin

class MachineTest(unittest.TestCase):
    def test_refill(self):
        rack = Rack("A", "Biscuit", 100)
        machine = Machine([rack])
        machine.refill("A", 10)
        self.assertEqual(machine.racks['A'].quantity, 10)

    def test_buy_biscuit(self):
        rack = Rack("A", "Biscuit", 100)
        machine = Machine([rack])
        machine.refill("A", 1)
        for i in range(4):
            machine.insert(Coin.QUARTER)
        machine.press("A")
        self.assertEqual(machine.racks['A'].quantity, 0)
        self.assertEqual(machine.coins[Coin.QUARTER], 4)

    def test_buy_biscuit_no_quantity(self):
        rack = Rack("A", "Biscuit", 100)
        machine = Machine([rack])
        for i in range(4):
            machine.insert(Coin.QUARTER)
        machine.press("A")
        self.assertEqual(machine.racks['A'].quantity, 0)
        self.assertEqual(machine.coins[Coin.QUARTER], 0)

    def test_buy_biscuit_not_enough_coins(self):
        rack = Rack("A", "Biscuit", 100)
        machine = Machine([rack])
        machine.refill("A", 1)
        for i in range(3):
            machine.insert(Coin.QUARTER)
        machine.press("A")
        self.assertEqual(machine.racks['A'].quantity, 1)
        self.assertEqual(machine.coins[Coin.QUARTER], 3)

    def test_buy_biscuit_too_many_coins(self):
        rack = Rack("A", "Biscuit", 100)
        machine = Machine([rack], 10)
        machine.refill("A", 1)
        for i in range(3):
            machine.insert(Coin.QUARTER)
        for i in range(3):
            machine.insert(Coin.DIME)
        machine.press("A")
        self.assertEqual(machine.racks['A'].quantity, 0)
        self.assertEqual(machine.coins[Coin.QUARTER], 13)
        self.assertEqual(machine.coins[Coin.DIME], 13)
        self.assertEqual(machine.coins[Coin.NICKEL], 9)
        self.assertEqual(machine.amount,0)

    def test_buy_biscuit_too_many_coins2(self):
        # give 25+10x10 => 125
        # buy for 95
        # machine should return 30, and have 95
        rack = Rack("A", "Biscuit", 95)
        machine = Machine([rack], 0)
        machine.refill("A", 1)
        machine.insert(Coin.QUARTER)
        for i in range(10):
            machine.insert(Coin.DIME)
        machine.press("A")
        #print(machine.coins)
        self.assertEqual(machine.racks['A'].quantity, 0)
        self.assertEqual(sum([ k.value*v for k,v in machine.coins.items() ]), 95)

    def test_make_change(self):
        # give 100+2x25+2x10+2x5
        # price 85, 90, 95 => impossible to give back change
        for price in [ 5, 10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180 ]:
            rack = Rack("A", "Biscuit", price)
            machine = Machine([rack], 0)
            machine.refill("A", 1)
            machine.insert(Coin.DOLLAR)
            machine.insert(Coin.QUARTER)
            machine.insert(Coin.QUARTER)
            machine.insert(Coin.DIME)
            machine.insert(Coin.DIME)
            machine.insert(Coin.NICKEL)
            machine.insert(Coin.NICKEL)
            self.assertEqual(machine.amount, 180)
            machine.press("A")
            if price not in [ 85, 90, 95 ]:
                self.assertEqual(sum([ k.value*v for k,v in machine.coins.items() ]), price)
                self.assertEqual(machine.racks['A'].quantity, 0)
            else:
                self.assertEqual(sum([ k.value*v for k,v in machine.coins.items() ]), 0)
                self.assertEqual(machine.racks['A'].quantity, 1)
            self.assertEqual(machine.amount, 0)
           

    def test_make_change_fail(self):
        # give 25+10, buy for 30
        # no change available should not give product and return all money
        machine = Machine([], 0)
        rack = Rack("A", "Biscuit", 30)
        machine = Machine([rack], 0)
        machine.refill("A", 1)
        machine.insert(Coin.QUARTER)
        machine.insert(Coin.DIME)
        machine.press("A")
        #print(machine.coins)
        self.assertEqual(machine.racks['A'].quantity, 1)
        self.assertEqual(sum([ k.value*v for k,v in machine.coins.items() ]), 0)
