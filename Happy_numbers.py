def isHappy(n):
    if n <= 0:
        raise ValueError("Input must be a positive value!")
    while n != 1 and n != 4:
        if not isinstance(n, str):
            str_n = str(n)
        split = list(str_n)
        #In case someone enters a decimal
        if "." in split:
            split.remove(".")
        ints = [j**2 for j in [int(i) for i in split]]
        n = sum(ints)
    if n == 1:
        return True
    else:
        return False

#Make a list of happy between between 1 and 100
happy_numbers = []
for i in range(1, 101):
    if isHappy(i) is True:
        happy_numbers.append(i)
print("List of happy nunbers found with a while loop:", happy_numbers)

def isHappy_recursive(n):
    if n <= 0:
        raise ValueError("Input must be a positive value!")
    if not isinstance(n, str):
        str_n = str(n)
    split = list(str_n)
    #In case someone enters a decimal
    if "." in split:
        split.remove(".")
    ints = [j**2 for j in [int(i) for i in split]]
    num = sum(ints)
    if num == 1:
        return True
    elif num == 4:
        return False
    else:
        return isHappy_recursive(num)

#Make a list of happy between between 1 and 100
happy_numbers = []
for i in range(1, 101):
    if isHappy_recursive(i) is True:
        happy_numbers.append(i)
print("List of happy nunbers found recursively:", happy_numbers)