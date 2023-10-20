def sorted_print_a(d):
    print("Printing (in alphabetical order of key)")

    for key, value in sorted(d.items(), key=lambda x: x[0]):
        print(f"{key}\t\t{value}")


def sorted_print_b(d):
    print("Printing (in ascending order of key)")

    for key, value in sorted(d.items(), key=lambda x: x[1]):
        print(f"{key}\t\t{value}")


def init_dic(d, se):
    words = se.lower().replace(",", " ").replace(".", " ").split()

    for word in words:
        if word not in d.keys():
            d[word] = d.get(word, 0) + 1
        else:
            d[word] += 1


dic = {}
sentence = input("Put your sentence here.\n")

init_dic(dic, sentence)

print("\nResult:")

sorted_print_a(dic)
print("\n")
sorted_print_b(dic)
