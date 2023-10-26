from math import sqrt

def isPrime(num):
    flag=True
    for i in range(2,int(sqrt(num))+1):
        if num%i==0:
            flag=False
            break
    if flag:
        return True
    else:
        return False

for i in range(1,1000):
    if isPrime(i):
        if isPrime(i+2):
            print('(',i,',',(i+2),')')

    
