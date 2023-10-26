def ctf(cel):
    fah = round(float((9 / 5) * cel + 32), 1)
    return fah


def ftc(fah):
    cel = round(float((5 / 9) * (fah - 32)), 2)
    return cel


clist = [ctf(cel) for cel in range(30, 40)]  # 使用列表推导式生成温度列表
flist = [ftc(fah) for fah in range(120, 110, -1)]

print(f"Celsius\tFahrenheit\t|\tFahrenheit\tCelsius")

for i in range(10):
    print(f"{i + 30.0}\t{clist[i]}\t\t|\t{120.0 - 10 * i}\t{flist[i]}")
