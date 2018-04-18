#Create a function that returns a list of Happy cubes
def cube_happy(n, loopers = [0]):
    '''
    :param n: A Number to check whether it is a happy cube
    :param loopers: A list of numbers that create an infinite loop and should be avoided
    :return: If a loop forms, that number will be output, otherwise True
    '''
    repeats = loopers
    if n <= 0:
        raise ValueError("Input must be a positive value!")
    k = 500 #Used if no loopers given
    split = list(str(n))
    ints = [j ** 3 for j in [int(i) for i in split]]
    sum_cubes = sum(ints)
    if n != sum_cubes and sum_cubes not in repeats:
        while k != 0:
            split = list(str(sum_cubes))
            ints = [j ** 3 for j in [int(i) for i in split]]
            sum_cubes = sum(ints)
            k -= 1
    if sum_cubes == n:
        return True
    else:
        return sum_cubes

#Quickly make a list of numbers that generate a loop
loops = set()
for i in range(1, 1001):
    if cube_happy(i) is not True:
        loops.add(cube_happy(i))

print(loops)

# Find all happy cubes from 1-1000
cube_happy_numbers = []
for i in range(1, 1001):
    if cube_happy(i, loopers=loops) is True:
        cube_happy_numbers.append(i)

print("List of cube happy numbers:", cube_happy_numbers)
