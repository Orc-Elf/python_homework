def convert(num):
    try:
        num = int(num)
        if not 0 <= num <= 2000:
            raise ValueError("Please put number between 0 and 2000")

        one = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
        two = ['', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen',
               'nineteen']
        three = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

        def trans(n):
            if 0 <= n <= 10:
                return one[n]
            elif 10 < n < 20:
                return two[n - 10]
            elif 20 <= n < 100:
                return f"{three[n // 10]}-{one[n % 10]}" if n % 10 != 0 else three[n // 10]
            elif 100 <= n < 1000:
                return f"{one[n // 100]} hundred and {trans(n % 100)}" if n % 100 != 0 else f"{one[n // 100]} hundred"
            else:
                return f"one thousand {trans(n % 1000)}" if n % 1000 != 0 else "one thousand"

        return trans(num)

        return trans(number)

    except Exception as e:
        return str(e)


number = input("Put the number that you want to translate here: ")
print(f"Here is the result: {convert(number)}")
