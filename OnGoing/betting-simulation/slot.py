import random

# slot machine
class Slot:
    def __init__(self, player):
        self.player = player
        self.balance = self.player.balance
        self.winnings = self.player.winnings
        self.payout = 0

    def pull(self):
        self.payout = 0
        if self.balance > 0:
            self.balance -= 1
            self.payout = 1
            if random.randint(1, 100) == 1:
                self.payout = 100
            elif random.randint(1, 10) == 1:
                self.payout = 10
            self.winnings += self.payout
        return self.payout
