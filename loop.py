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

