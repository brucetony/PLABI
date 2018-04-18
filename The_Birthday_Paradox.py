#First create a function that checks for duplicates in a list

def has_duplicates(some_list):
    originals = []
    for i in some_list:
        if i in originals:
            return True
        else:
            originals.append(i)
    return False

def birthday_prob(num_students, num_trials):
    '''
    :param num_students: Enter the number of students in the class
    :param num_trials: Enter how many trials to run (try ~10,000)
    :return: Probability that 2 people with a class of n students share a birthday
    '''
    k = 0
    trial_results = []
    while k <= num_trials:
        birthdays = [random.randint(0, 365) for i in range(num_students)]
        trial_results.append(has_duplicates(birthdays))
        k += 1
    Trues = 0
    for i in trial_results:
        if i is True:
            Trues += 1
    return Trues/len(trial_results)

print("Birthday estimate:", birthday_prob(27, 10000))