import pickle
import re
from random import randint
from random import shuffle


def error_message():
    data = pickle.load(open('storage.dat', 'rb'))
    message = ''
    if data['min_error'] is True or data['max_error'] is True:
        message += "Min - Max Error\n"
    if data['deci_error'] is True:
        message += " Decimal Error"
    return message


def custom_min(min_):
    data = pickle.load(open('storage.dat', 'rb'))
    result = False
    try:
        if (re.match(r'^[0-9]+$', min_) and
                not re.match(r'^0[0-9]+', min_) and
                int(min_) < data['max_data']):
            result = True
    except TypeError:
        result = False
    if result:
        data['min_error'] = False
        data['max_error'] = False
        pickle.dump(data, open('storage.dat', 'wb'))
        return True
    elif not result:
        try:
            data['min_data'] = int(min_)
        except ValueError:
            data['min_data'] = min_
        data['min_error'] = True
        pickle.dump(data, open('storage.dat', 'wb'))
        return False


def custom_max(max_):
    data = pickle.load(open('storage.dat', 'rb'))
    result = False
    try:
        if (re.match(r'^[0-9]+$', max_) and
                not re.match(r'^0[0-9]+', max_) and
                int(max_) > data['min_data']):
            result = True
    except TypeError:
        result = False
    if result:
        data['max_error'] = False
        data['min_error'] = False
        pickle.dump(data, open('storage.dat', 'wb'))
        return True
    elif not result:
        try:
            data['max_data'] = int(max_)
        except ValueError:
            data['max_data'] = max_
        data['max_error'] = True
        pickle.dump(data, open('storage.dat', 'wb'))
        return False


def custom_deci(deci):
    data = pickle.load(open('storage.dat', 'rb'))
    result = False
    if deci is not None:
        if (re.match(r'^[0-9]+$', deci) and
                not re.match(r'^0[0-9]+', deci)):
            result = True
    if result:
        data['deci_error'] = False
        pickle.dump(data, open('storage.dat', 'wb'))
        return True
    elif not result:
        data['deci_error'] = True
        pickle.dump(data, open('storage.dat', 'wb'))
        return False


def create_deci(deci_places):
    for digits in range(deci_places):
        if digits == 0:
            num = '.'
        num += str(randint(0, 9))
    return num


def create_neg(num):
    chance = randint(1, 2)
    return -num if chance == 1 else num


def show_problem(num1, num2, num3, num4, type_):
    data = pickle.load(open('storage.dat', 'rb'))
    if type_ == '+':
        return '   ' + str(num1) + num3 + '\n+ ' + str(num2) + num4
    if type_ == '-':
        if data['neg_data'] is True:
            return '   ' + str(num1) + num3 + '\n- ' + str(num2) + num4
        else:
            if (num1 - num2) >= 0:
                return '   ' + str(num1) + num3 + '\n- ' + str(num2) + num4
            else:
                return '   ' + str(num2) + num3 + '\n- ' + str(num1) + num4
    if type_ == '*':
        return '   ' + str(num1) + num3 + '\n* ' + str(num2) + num4


def show_division_problem(data_set):
    if data_set['max_data'] > 999999:
        return 'Sorry, try\nlowering the\nMax...'
    num1 = randint(data_set['min_data'], data_set['max_data'])
    num2_list = []
    if num1 == 1 or num1 == 0:
        return '   ' + str(num1) + '\n/ ' + '1'
    else:
        for i in range(data_set['min_data'], int((num1/2) + 1)):
            if i != 0 and i != 1 and num1 % i == 0:
                num2_list.append(i)
        if len(num2_list) <= 1:
            num2 = num1
        else:
            shuffle(num2_list)
            num2 = num2_list[randint(0, len(num2_list) - 1)]
    if data_set['neg_data']:
        num1 = create_neg(num1)
        num2 = create_neg(num2)
    return '   ' + str(num1) + '\n/ ' + str(num2)


def form_problem(data_set, type_):
    if (data_set['min_error'] is True or
            data_set['max_error'] is True or
            data_set['deci_error'] is True):
        return error_message()
    if type_ == '//':
        return show_division_problem(data_set)
    num1 = randint(data_set['min_data'], data_set['max_data'])
    num2 = randint(data_set['min_data'], data_set['max_data'])
    num3, num4 = '', ''
    if data_set['deci_data'] != 0:
        num3 = create_deci(data_set['deci_data'])
        num4 = create_deci(data_set['deci_data'])
    if data_set['neg_data']:
        num1 = create_neg(num1)
        num2 = create_neg(num2)
    return show_problem(num1, num2, num3, num4, type_)


def prepare_data(key=False, min_=None, max_=None,
                 deci=None, neg=None, type_=None):
    if key is True:
        data = dict(
            min_data=0, max_data=100, deci_data=0, neg_data=False,
            min_error=False, max_error=False, deci_error=False)
        pickle.dump(data, open('storage.dat', 'wb'))
    else:
        data = pickle.load(open('storage.dat', 'rb'))
        if min_ is not None:
            data['min_data'] = min_
        if max_ is not None:
            data['max_data'] = max_
        if deci is not None:
            data['deci_data'] = deci
        if neg is not None:
            data['neg_data'] = neg
        pickle.dump(data, open('storage.dat', 'wb'))
    return form_problem(data, type_)


def answer(user_ans, problem):
    if (re.match(r'^-?[0-9]+\.?[0-9]*$', user_ans) and
            not re.match(r'^There', problem)):
        if eval(user_ans) == eval(problem.replace('\n', '')):
            return True
    else:
        return False
