import random

#First create a function that checks for duplicates in a list
def has_duplicates(some_list):
    originals = []
    for i in some_list:
        if i in originals:
            return True
        else:
            originals.append(i)
    return False

#Use duplicate function to check if 2 random days are in list
def birthday_prob(num_students, num_trials):
    '''
    :param num_students: Enter the number of students in the class
    :param num_trials: Enter how many trials to run (try ~10,000)
    :return: Probability that 2 people with a class of n students share a birthday
    '''
    k = 0
    trial_results = []
    while k <= num_trials:
        birthdays = [random.randint(0, 364) for i in range(num_students)]
        trial_results.append(has_duplicates(birthdays))
        k += 1
    Trues = 0
    for i in trial_results:
        if i is True:
            Trues += 1
    return Trues/len(trial_results)

print("2 people sharing a birthday estimate:", birthday_prob(27, 10000))

#To see if 3 people share a birthday
def has_triplicates(some_list):
    originals = []
    duplicates = []
    for i in some_list:
        if i in originals:
            if i in duplicates:
                return True
            else:
                duplicates.append(i)
        else:
            originals.append(i)
    return False

#Use triplicate function to check if 3 random days are in list
def birthday_prob_3(num_students, num_trials):
    '''
    :param num_students: Enter the number of students in the class
    :param num_trials: Enter how many trials to run (try ~10,000)
    :return: Probability that 2 people with a class of n students share a birthday
    '''
    k = 0
    trial_results = []
    while k <= num_trials:
        birthdays = [random.randint(0, 365) for i in range(num_students)]
        trial_results.append(has_triplicates(birthdays))
        k += 1
    Trues = 0
    for i in trial_results:
        if i is True:
            Trues += 1
    return Trues/len(trial_results)

print("3 people sharing a birthday estimate:", birthday_prob_3(27, 10000))