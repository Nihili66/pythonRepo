def get_exchange_money(exchange_value, exchange_rate):
    return exchange_value / exchange_rate


def get_change(budget, exchange_value):
    return budget - exchange_value


def get_number_of_bills(exchange_value, bill_value):
    return exchange_value // bill_value


def get_value_of_bills(bill_value, number_of_bills):
    return bill_value * number_of_bills


def get_exchangeable_value(exchange_value, exchange_rate, fee, bill_value):
    actual_exchange_rate = exchange_rate * (1 + (fee / 100))
    exchange_money = get_exchange_money(exchange_value, actual_exchange_rate)
    number_of_bills = get_number_of_bills(exchange_money, bill_value)
    return int(get_value_of_bills(bill_value, number_of_bills))
    # return int(((exchange_value / (exchange_rate + (exchange_rate * fee / 100))) // bill_value) * bill_value)


def non_exchangeable_value(exchange_value, exchange_rate, fee, bill_value):
    actual_exchange_rate = exchange_rate * (1 + (fee / 100))
    exchange_money = get_exchange_money(exchange_value, actual_exchange_rate)
    return int(exchange_money % bill_value)
