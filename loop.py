#question1
num_1=2
den_1=1
num_2=3
den_2=2
sum=num_1/den_1+num_2/den_2

for i in range(1,19):
    num=num_1+num_2
    den=den_1+den_2
    sum+=num/den

    num_1,den_1=num_2,den_2
    num_2,den_2=num,den
    
print(sum)

#question2
str=input("please enter 1232a string")
length=len(str)
list1=list(str)
i=0
while i<=length/2:
    if list1[i]==list1[length-1-i]:
        i+=1
        if i>length/2:
            print("yes")
            break
    else:
       print("no")
       break


#question3
from math import sqrt

count=0
n=2
flag=True
while count<30:
   flag=True
   for i in range(2,int(sqrt(n))+1):
        if n%i==0:
            flag=False
            break
   if flag:
        print(n,end='\t')
        count+=1
        if count%10==0:
            print(end='\n')
   n+=1
