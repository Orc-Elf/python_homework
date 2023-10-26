import math


def isprime(number):
    if number <= 1:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True


twin_prime = []
for number in range(1, 1000, 2):
    if isprime(number) and isprime(number + 2):
        twin_prime.append(number)
        twin_prime.append(number + 2)

count_t = 0
while count_t < len(twin_prime):
    print(f"({twin_prime[count_t]}, {twin_prime[count_t + 1]})\n")
    count_t += 2
