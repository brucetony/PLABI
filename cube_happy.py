def cube_happy(n):
    if n <= 0:
        raise ValueError("Input must be a positive value!")
    k=500
    split = list(str(n))
    ints = [j ** 3 for j in [int(i) for i in split]]
    sum_cubes = sum(ints)
    while n != sum_cubes and k != 0:
        split = list(str(sum_cubes))
        ints = [j**3 for j in [int(i) for i in split]]
        sum_cubes = sum(ints)
        k -= 1
    if sum_cubes == n:
        return True
    else:
        return sum_cubes

# repeats = set()
# for i in range(1, 1001):
#     if cube_happy(i) is not True:
#         repeats.add(cube_happy(i))

def cubey(n):
    repeats = [160, 1, 352, 407, 217, 133, 136, 919, 370, 371, 1459, 244, 55, 153, 250]
    if n <= 0:
        raise ValueError("Input must be a positive value!")
    split = list(str(n))
    ints = [j ** 3 for j in [int(i) for i in split]]
    sum_cubes = sum(ints)
    while n != sum_cubes and sum_cubes not in repeats:
        split = list(str(sum_cubes))
        ints = [j ** 3 for j in [int(i) for i in split]]
        sum_cubes = sum(ints)
    if sum_cubes == n:
        return True
    else:
        return False

cube_happy_numbers = []
for i in range(1, 1001):
    if cubey(i) is True:
        cube_happy_numbers.append(i)

print("List of cube happy numbers:", cube_happy_numbers)
