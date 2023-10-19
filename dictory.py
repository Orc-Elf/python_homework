
text="The teacher said that, that that that that student used was right."
text=text.lower()
#print(text)
text=text.replace(
words=text.split()
#print(word)

dict={}

for word in words:
 if word in dict.keys():
    dict[word]+=1
 else dict[word]=1

list1=list(dict.items())
list1.sorted()
print('Printing(in alphabetical order of key)')

