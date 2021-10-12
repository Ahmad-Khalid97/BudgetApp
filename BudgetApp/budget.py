class Category:

    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, *description):
        d = {'amount': amount}
        if len(description) == 0:
            description = ""
            d['description'] = description
        else:
            d['description'] = description[0]
        self.ledger.append(d)

    def withdraw(self, amount, *description):
        d = {}
        if len(self.ledger) != 0:
            if self.check_funds(amount):
                d['amount'] = - amount
                if len(description) == 0:
                    description = ""
                    d['description'] = description
                else:
                    d['description'] = description[0]
                self.ledger.append(d)
                return True
            else:
                return False

    def get_balance(self):
        balance = 0
        if len(self.ledger) != 0:
            for i in range(len(self.ledger)):
                balance += self.ledger[i]['amount']
        return balance

    def transfer(self, amount, budget_category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {budget_category.category}')
            budget_category.deposit(amount, f'Transfer from {self.category}')
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount <= self.get_balance():
            return True
        else:
            return False

    def __str__(self):
        category_list = ''
        if len(self.ledger) != 0:
            category_list = '*' * ((30 - len(self.category)) // 2) + self.category + '*' * (
                    (30 - len(self.category)) // 2) + '\n'
            if len(category_list) == 30:
                category_list = category_list[:29] + '*' + category_list[29:]
            for i in range(len(self.ledger)):
                if self.ledger[i]['description'] != '':
                    category_list += (self.ledger[i]['description'])[:23]
                amount_value = str(float(self.ledger[i]['amount']))
                if amount_value.endswith('.0'):
                    amount_value += '0'
                category_list += amount_value.rjust(30 - len((self.ledger[i]['description'])[:23])) + '\n'
            category_list += 'Total: ' + str(self.get_balance())
        return category_list


def create_spend_chart(categories):
    result = "Percentage spent by category\n"
    category_withdrawals = 0
    category_withdrawals_list = []
    total_withdrawals = 0
    for category in categories:
        if len(category.ledger) != 0:
            for i in range(len(category.ledger)):
                if category.ledger[i]['amount'] < 0:
                    category_withdrawals += category.ledger[i]['amount']
                    total_withdrawals += category.ledger[i]['amount']
        category_withdrawals_list.append(category_withdrawals)
        category_withdrawals = 0
    percentages = [(category_withdrawals_list[i] / total_withdrawals) // 0.01 for i in range(len(category_withdrawals_list))]
    for x in range(100, -10, -10):
        result += str(x).rjust(3, " ") + "|"
        for y in percentages:
            if y >= x:
                result += ' o '
            else:
                result += '   '
        result += ' \n'
    result += '    ' + '-' * ((len(categories)*3)+1) + '\n'
    max_length = max(len(category.category) for category in categories)
    for x in range(max_length):
        result += '    '
        for y in categories:
            if x < len(y.category):
                result += ' ' + y.category[x] + ' '
            else:
                result += '   '
        result += ' \n'
    return result.rstrip() + '  '
