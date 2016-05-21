# -*- coding: utf-8 -*-


def get_birthday_num(data):
    '''
    расчет нумерологического числа дня рождения
    '''
    def num(data):
        while True:
            data = reduce(lambda res, x: res+int(x), list(str(data)), 0)
            if data < 10 or data in (11, 22):
                break
        return data
    return num(''.join(data.split('.')))
