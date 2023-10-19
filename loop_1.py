import math

def isprime(number):
    if number <= 1:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True


def loop_1():
    n = 2
    m = 1
    value = 0
    for i in range(20):
        n = m + n
        m = m + i
        value = n / m
        value += value
    return value


def loop_2(my_str):
    set_r = my_str[::-1]
    if set_r == my_str:
        print("是回文")
    else:
        print("不是回文")

def loop_3():
    count = 0
    number = 2
    while count<30:
        number += 1
        if isprime(number):
            print(number, end=' ')
            count += 1
            if count % 10 == 0:
                print()


print(loop_1())
str = input("Put your str here:")
loop_2(str)
loop_3()
