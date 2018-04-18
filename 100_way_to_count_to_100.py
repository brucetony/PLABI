import itertools

def one_hundred():
    pass

#Make a list of lists which contains all permutations of operators
operator_list = []
for i in range(1, 9):
    operator_list.append([list(subset) for subset in itertools.combinations_with_replacement("+-*/", i)])


#Make list with every combination of numbers
nums_list = []
nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
for i in range(len(nums)):
    j = len(nums)
    while i < j:
        nums_list.append(''.join(nums[i:j]))
        j -= 1

nums_list.sort()
print(nums_list)

#Make list of lists of numbers that only have 1-9
# combos_list = [list(combo) for combo in itertools.combinations(nums_list, 9)]
# for i in range(len(nums_list)):
#     if list(nums_list[i])[0] == "1":
#         combo = [nums_list[i]]
#         while int(list(combo[-1])[-1]) != 9:
#             for test in nums_list[i+1:]:
#                 if list(combo[-1])[-1] < list(test)[0]:
#                     combo.append(test)
#         combos_list.append((combo))


