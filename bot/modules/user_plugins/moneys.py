import math
import random


money_char = "$"


def reg_moneys(vkid):
    return random.randint(2500, 5000)


def init():
    module.db.check_column("accounts", "balance", "FLOAT NOT NULL")
    module.registration.columns["balance"] = reg_moneys


class Plugin:
    def get_money(self):
        return "{}{}".format(module.utils.digit_number(math.floor(self.balance)), money_char)

    def take_money(self, value):
        if self.balance - value >= 0:
            self.add('balance', -value)
        else:
            error('у вас недостаточно долларов ⚠<br>💰 Необходимо: {}$'.format(module.utils.digit_number(math.floor(value - self.balance))))
