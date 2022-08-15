class Budgeting:
    def __init__(self, name):
        # settings
        self.name = name
        self.ledger = []
        self.balance = 0
        self.withdrawals = 0
        self.deposits = 0

    def __str__(self):
        title = self.name
        total = str(self.get_balance())
        output = title.center(30, "*") + "\n"
        for row in self.ledger:
            description = row.get("description")[:23]
            amount = str("{:.2f}".format(row.get("amount")))[:7]
            output += description.ljust(23) + amount.rjust(7) + "\n"
        output += "Total: " + total
        return output

    # deposit method
    def deposit(self, amount, description=""):
        self.deposits += amount
        self.ledger.append({"amount": amount, "description": description})

    # withdraw method
    def withdraw(self, amount, description=""):
        self.withdrawals += amount
        self.ledger.append({"amount": -amount, "description": description})

    # get balance method
    def get_balance(self):
        self.balance = 0
        for row in self.ledger:
            amount = row.get("amount")
            self.balance += amount
        return self.balance


def create_spend_chart(categories):
    # display settings
    title = "Percentage spent by category" + "\n"
    output = title
    percentages = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    # total spent
    total_spent = 0
    for category in categories:
        category.get_withdrawals()
        total_spent += category.withdrawals

    # percentages
    def get_categ_perc(x):
        return round((categories[x].get_withdrawals() * 100) / total_spent)

    # names
    def get_categ_name(x):
        return categories[x].name

    # get max name length
    def get_range_len():
        name_len = []
        for x in range(len(categories)):
            name_len.append(len(get_categ_name(x)))
        return max(name_len)

    # drawing the chart
    chart = ""
    for i in range(len(percentages)):
        perc = str(percentages[10 - i]).rjust(3)
        chart += f"{perc}|"
        for x in range(len(categories)):
            if get_categ_perc(x) >= percentages[10 - i]:
                chart += " o "
            else:
                chart += "   "
        chart += "\n"
    output += chart
    line = "---" * len(categories) + "\n"
    output += line.rjust(4 + len(categories) * 3)
    names = ""
    for i in range(get_range_len()):
        for x in range(len(categories)):
            try:
                names += " " + get_categ_name(x)[i] + " "
            except IndexError:
                names += "   "
        names = str(names + "\n")
    output += names
    # print(names)
    return output
