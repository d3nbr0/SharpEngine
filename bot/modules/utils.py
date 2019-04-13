import random


def digit_number(number):
    return '{0:,}'.format(number).replace(',', '.')


def shuffle(array):
    new_arr = array[:]
    random.shuffle(new_arr)
    return new_arr


def decline(number, titles):
    cases = [2, 0, 1, 1, 1, 2]
    return titles[2 if (number % 100 > 4) and (number % 100 < 20) else cases[number % 10 if number % 10 < 5 else 5]]
