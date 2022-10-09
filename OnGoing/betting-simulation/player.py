# slot machine player
class Player:
    def __init__(self):
        self.balance = 0
        self.winnings = 0

    def deposit(self, amount):
        self.balance += amount
