import itertools

def one_hundred():
    '''
    A function that combines "123456789" in various ways using basic operators and evaluates synthesized equation
    :return: number of combinations that equal 100
    '''
    operators = ["+", "-", "*", "/", ""]
    operator_list = list(itertools.product(operators, repeat=8))
    combo_counter = 0
    for i in range(len(operator_list)):
        equation = "1{}2{}3{}4{}5{}6{}7{}8{}9".format(*operator_list[i])
        evaluation = eval(equation)
        if evaluation == 100:
            combo_counter += 1
    print("There are {} ways to make these numbers equal 100".format(combo_counter))

one_hundred()


#TODO make it more general so you can put in a list of numbers








