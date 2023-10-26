def CtoF(c):
    'turn celsius into fahrenhei'
    f=float((9/5)*c+32)
    return f

def FtoC(f):
    'turn fahrenheit into celsius'
    c=float((5/9)*(f-32))
    return c

print("%-15s%-15s|   %-15s%-20s"%('Celsius','Fahrenheit','Fahreenheit','Celsius'))

#c=float(input('please enter celsius'))
#f=float(input('please enter fahrenheit'))
clist=[c for c in range(40,30,-1)]
flist=[f for f in range(120,20,-10)]

       
format="%-15.1f%-15.1f|   %-15.1f%-15.2f"
for i in range(0,10):
 values=(clist[i],CtoF(clist[i]),flist[i],FtoC(flist[i]))
 print(format%values)




